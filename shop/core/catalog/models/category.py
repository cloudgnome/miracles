#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from re import sub
from PIL import Image
from mptt import register
from mptt.models import MPTTModel, TreeForeignKey
from django.db.models import CASCADE
from catalog.models import Slugify,Description,Page
from string import ascii_letters
from django.db.models import *
from settings import MEDIA_ROOT,CACHE_URL,DOMAIN,BASE_DIR,STATIC_ROOT
from redactor.fields import RedactorField
from random import choice
from shop.models import Language
from django.utils.translation import ugettext_lazy as _
import urllib.parse

from shop.models import Static

# version = Static.objects.first()
# if not version:
#     version = Static.objects.create()

# CSS_BUILD = version.css

from subprocess import Popen, PIPE

class CategoryDescription(Description):
    class Meta:
        db_table = 'category_description'
        unique_together = (('language','name'),('language','title'),('language','meta_description'))

class Category(MPTTModel,Slugify):
    slug = CharField(max_length=255,null=True,verbose_name='URL',unique=True)
    description = ManyToManyField(CategoryDescription,related_name="obj")
    parent = TreeForeignKey('self', blank=True, null=True, verbose_name="Родитель",related_name="child", on_delete=CASCADE)
    image = ImageField(upload_to='data/category/', blank=True, null=True,verbose_name='Картинка')
    last_modified = DateTimeField(auto_now_add=True)
    active = BooleanField(default=1,verbose_name='Активна')
    bgcolor = CharField(max_length=20,null=True)

    def cache(self):
        super().cache()

        for device in ['mobile','desktop']:
            for lang in Language.objects.all():
                pattern = '{CACHE_URL}cache/html/{device}/{lang}/static/categories.html'.format(device=device,lang=lang,CACHE_URL=CACHE_URL)
                if os.path.isfile(pattern):
                    os.remove(pattern)

            # proc = Popen(['/home/core/shop/{DOMAIN}/ffs.sh'.format(DOMAIN=DOMAIN)], stdin=PIPE, stdout=PIPE, stderr=PIPE)
            # output, error = proc.communicate()
            # with open('process.log','wb') as f:
            #     f.write(output + error)

    def menu_thumb(self,size=70):
        try:
            path = MEDIA_ROOT + urllib.parse.unquote(self.image.url).replace('/media/','')
        except ValueError:
            return None
        img = Image.open(path)
        img.thumbnail([size,size])

        return img

    @property
    def icon(self):
        return self.image_url(size=100)

    @property
    def productsCount(self):
        count = self.products.count()
        for child in self.child.all():
            count += child.products.count()

        return count

    def save(self,*args,**kwargs):
        if self.active:
            for thumb in self.thumb.all():
                thumb.delete()

        if self.id:
            for product in self.products.all():
                product.cache()

        for lang in Language.objects.all():
            for device in ['desktop','mobile']:
                catfile = '{cache}cache/html/{device}/{lang}/static/categories.html'.format(cache=CACHE_URL,device=device,lang=lang.code)
                if os.path.isfile(catfile):
                    os.remove(catfile)

        super().save(*args,**kwargs)

    def image_url(self,size=230):
        try:
            image = Category_Thumb.objects.get(category_id=self.pk,size=size)
        except Category_Thumb.MultipleObjectsReturned:
            image = Category_Thumb.objects.filter(category_id=self.pk,size=size).first()
        except:
            image = None

        if image:
            if os.path.isfile(CACHE_URL + image.url):
                return image.url
            else:
                image.delete()

        try:
            return self.thumbnail(size)
        except:
            pass

        return '/media/data/no_image_new.jpg'

    def thumbnail(self,size):
        image = Image.open(self.image)
        image.thumbnail([size,size])

        path = self.path(size)

        try:
            image = image.convert('RGBA')
            image.save(CACHE_URL + path,'PNG')
        except:
            image = image.convert('RGB')
            image.save(CACHE_URL + path,'JPEG')

        thumb = Category_Thumb.objects.create(url = '/' + path,category=self,size=size)
        return thumb.url

    def path(self,size):
        name = sub("[^a-zA-Z0-9А-Яа-я]","",self.image.name.split('/')[-1])
        path = 'images/%s/%s%s/' % (name,size,name[1])
        root = CACHE_URL + path
        if not os.path.isdir(root):
            try:
                os.makedirs(root)
            except FileExistsError:
                pass
        for i in range(0,32):
            path += choice(ascii_letters)
        return path + '.jpg'

    def similars(self):
        return Category.objects.filter(parent=self.parent).exclude(id=self.id)

    def get_ancestorsf(self,parent,categories):
        if parent.parent and parent.parent.parent:
            categories += (parent.parent,)
            return self.get_ancestorsf(parent.parent,categories)

        return reversed(categories)

    def ancestors(self):
        categories = ()

        if self.parent and self.parent.parent:
            categories += (self.parent,)
            return self.get_ancestorsf(self.parent,categories)

        return reversed(categories)

    def get_root(self,parent):
        if parent.parent:
            return self.get_root(parent.parent)

        return parent

    @property
    def root(self):
        if self.parent:
            return self.get_root(self.parent)
        else:
            return _('Категории товаров')

    def ancestors_breadcrumbs(self, parent, breadcrumbs, lang):
        breadcrumbs = breadcrumbs + ((parent.names(lang),parent.slugy(lang)),)
        if parent.parent:
            return self.ancestors_breadcrumbs(parent.parent, breadcrumbs, lang)
        else:
            return breadcrumbs

    def breadcrumbs(self,lang,product = False):
        if self.parent is None:
            if product:
                return ((self.names(lang),self.slugy(lang)),)
            else:
                return
        else:
            if product:
                breadcrumbs = ((self.names(lang),self.slugy(lang)),)
                breadcrumbs = self.ancestors_breadcrumbs(self.parent, breadcrumbs, lang)
            else:
                breadcrumbs = self.ancestors_breadcrumbs(self.parent, (), lang)
            return reversed(breadcrumbs)

    class Meta:
        unique_together = ('slug', 'parent')
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'

class Category_Thumb(Model):
    category = ForeignKey(Category,related_name='thumb', on_delete=CASCADE)
    url = CharField(max_length=255)
    size = PositiveIntegerField()

    def __str__(self):
        return self.url

register(Category)

class TigresCategory(Model):
    url = CharField(max_length=255,verbose_name='URL')
    category = ForeignKey(Category,verbose_name="Катигория",null=True, on_delete=CASCADE)

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = 'Tigres Категории для парсинга'
        verbose_name_plural = 'Tigres Категории для парсинга'