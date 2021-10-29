from django.db.models import Model,CharField,IntegerField,BooleanField
import re,os
from glob import glob
from settings import CACHE_URL
from shop.models import Redirect,Language
from django.utils import timezone
from googletrans import Translator
from google.cloud import translate_v2

class Slug(Model):
    slug = CharField(max_length=255,unique=True)
    view = CharField(max_length=20)
    model = CharField(max_length=20,null=True)
    model_id = IntegerField()

    def __iter__(self):
        return self.slug

    def __getitem__(self,key):
        return self.slug[key]

    def __str__(self):
        return self.slug

class Slugify(Model):
    cached = BooleanField(default=False)
    customView = None

    def autocomplete_dict(self):
        return {
            'id':self.id,
            'name':self.names(lang='ua'),
        }

    @property
    def view(self):
        return self.customView or self.modelName

    @property
    def modelName(self):
        return self.__class__.__name__

    def __str__(self):
        return str(self.description.all().first()) or ''

    @property
    def title(self):
        return self.__str__()

    @property
    def meta_description(self):
        return self.__str__()

    @property
    def meta_keywords(self):
        return self.__str__()

    def names(self,lang):
        try:
            return self.description.get(language__code=lang).name
        except:
            try:
                return self.description.all().first().name
            except:
                try:
                    return self.name
                except:
                    return ''

    def slugy(self,lang):
        if lang == 'ua':
            return '/ua/%s' % self.slug
        return '/%s' % self.slug

    def add_redirect(self,old,new):
        if old != new:
            try:
                Redirect.objects.get(old_path=old,new_path=new)
            except Redirect.DoesNotExist:
                Redirect.objects.create(old_path=old,new_path=new)

            Slug.objects.filter(slug=old).delete()

    def check_slug(self):
        if self.pk:
            try:
                slug = Slug.objects.get(model_id=self.pk,model=self.modelName,view=self.view)
                if self.slug != slug.slug:
                    self.add_redirect(slug.slug, self.slug)
            except Slug.MultipleObjectsReturned:
                old = Slug.objects.filter(model_id=self.pk,model=self.modelName,view=self.view).exclude(slug=self.slug).first()
                Slug.objects.filter(model_id=self.pk,model=self.modelName,view=self.view).delete()
                Slug.objects.create(model_id=self.pk,model=self.modelName,view=self.view,slug=self.slug)
                if old:
                    self.add_redirect(old, self.slug)
            except Slug.DoesNotExist:
                return

    def update_slug(self):
        try:
            slug = Slug.objects.get(slug=self.slug,model=self.modelName,model_id=self.id)
            if slug.view != self.view:
                slug.view = self.view
                slug.save()
        except Slug.DoesNotExist:
            if self.view == 'Main' and not self.slug:
                Slug.objects.filter(slug=self.slug).delete()

            Slug.objects.create(slug=self.slug,model=self.modelName,view=self.view,model_id=self.id)

    def save(self,*args,**kwargs):
        self.cached = False
        self.check_slug()
        self.last_modified = timezone.now()

        super().save(*args,**kwargs)

        self.update_slug()
        self.cache()

    def cache(self,verbose = False):
        from catalog.models import Page
        for device in ['mobile','desktop']:
            for lang in Language.objects.all():
                lang = lang.code

                if isinstance(self,Page):
                    pattern = '{CACHE_URL}cache/html/{device}/{lang}/static/'.format(device=device,lang=lang,CACHE_URL=CACHE_URL)
                else:
                    if not self.slug:
                        return
                    if len(self.slug) > 4:
                        pattern = '{CACHE_URL}cache/html/{device}/{lang}/{slug[3]}/{slug[4]}/'.format(device=device,lang=lang,slug=str(self.slug).replace('/',''),CACHE_URL=CACHE_URL)
                    elif len(self.slug) > 2:
                        pattern = '{CACHE_URL}cache/html/{device}/{lang}/{slug[1]}/{slug[2]}/'.format(device=device,lang=lang,slug=str(self.slug).replace('/',''),CACHE_URL=CACHE_URL)
                    else:
                        pattern = '{CACHE_URL}cache/html/{device}/{lang}/m/a/'.format(device=device,lang=lang,slug=str(self.slug).replace('/',''),CACHE_URL=CACHE_URL)

                if self.slug:
                    pattern += str(self.slug).replace('/','') + '*'
                else:
                    pattern += 'index*'

                if verbose:
                    print(pattern)
                for f in glob(pattern):
                    if verbose:
                        print(f)
                    if os.path.isfile(f):
                        os.remove(f)

        try:
            self.description.order_by('last_modified').last().save()
        except:
            self.last_modified = timezone.now()
        self.cached = False
        super().save()

    def delete(self,*args,**kwargs):
        self.cache()

        db = 'default'

        try:
            if self.slug:
                slug = Slug.objects.using(db).filter(model=self.modelName,model_id=self.id).delete()
        except Slug.DoesNotExist:
            pass

        for d in self.description.all():
            d.delete()

        super().delete(*args,**kwargs)

    def update(self,*args,**kwargs):
        super().save(*args,**kwargs)

    @property
    def get_url(self):
        return self.slug

    def date(self):
        try:
            return str(self.description.all().first().last_modified.date())
        except:
            return str(self.last_modified.date())

    def image_url(self):
        try:
            return self.image.url
        except:
            return '/media/igroteka/logo.jpg'

    @property
    def meta_image(self):
        try:
            return self.image.url
        except:
            return '/media/igroteka/logo.jpg'

    def __repr__(self):
        return self.__str__()

    @property
    def name(self):
        return self.__str__()

    @property
    def get_description(self):
        try:
            return self.description.first().text
        except:
            return ''

    def translate(self,src='uk',dst='ru'):
        # translator = Translator()
        translator = translate_v2.client.Client()
        src = self.description.get(language__ISOcode=src)

        name = translator.translate(src.name,source_language=src.language.ISOcode,target_language=dst)

        print(name.get('translatedText'))

        language = Language.objects.get(ISOcode=dst)

        try:
            dst = self.description.get(language=language)
        except:
            dst = self.description.create(language=language)

        dst.name = name.get('translatedText')
        dst.save()
        self.description.add(dst)

    def template_meta(self):
        for d in self.description.all():
            d.title = ''
            d.meta_description = ''
            d.meta_keywords = ''

            d.save()

    class Meta:
        abstract = True