from django.db import models
from catalog.models import Product,Page,Brand,Category,AbstractGallery,EmptyImage
from shop.models import Language
from django.utils import timezone
from math import ceil
from django.utils.translation import ugettext_lazy as _
from bs4 import BeautifulSoup

from tasks import prices,stock,google_merchant,facebook_merchant,np

try:
    from tasks import clone_stock
except:
    pass

try:
    from tasks import rozetka
except:
    pass

try:
    from tasks import hotline
except:
    pass

try:
    from tasks import currency_prices
except:
    pass

class Task(models.Model):
    name = models.CharField(max_length=255,null=True,unique=True)
    status_choices = (
        (1,_('В обробці')),
        (2,_('Виконано'))
    )
    status = models.PositiveIntegerField(choices=status_choices,default=2)
    link = models.CharField(max_length=255,null=True)
    function = models.CharField(max_length=255,null=True)

    def apply_async(self):
        return eval(self.function).apply_async((self.id,))

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

class Export(models.Model):
    name = models.CharField(max_length=255)
    task = models.ForeignKey(Task,on_delete=models.SET_NULL,null=True)
    has_meta = models.BooleanField(default=False)

    @property
    def dict(self):
        return {'id':self.id,'name':self.name}

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

class ExportStatus(models.Model):
    @property
    def default_price(self):
        return ceil(self.product.price * 1.2)

    product = models.ForeignKey(Product,related_name="export_status",on_delete=models.CASCADE)
    export = models.ForeignKey(Export,default=1,null=True,on_delete=models.SET_NULL)
    load = models.BooleanField(default=0)
    price = models.PositiveIntegerField(default=0)

    def save(self,*args,**kwargs):
        if not self.price:
            self.price = self.default_price
        super().save(*args,**kwargs)

    def __str__(self):
        return self.product.name

    class Meta:
        unique_together = ('product','export')

class ExportMeta(models.Model):
    @property
    def default_name(self):
        try:
            return self.export.product.description.values('name').filter(language__code='ua').first().get('name')
        except:
            return ''

    name = models.CharField(max_length=255,default='')
    text = models.CharField(max_length=10000)
    json_text = models.CharField(max_length=10000,null=True)
    export = models.OneToOneField(ExportStatus,related_name='meta',on_delete=models.CASCADE)

    def clean(text):
        if not text:
            return ''
        return BeautifulSoup(text,features="lxml").get_text()

    def save(self,*args,**kwargs):
        self.text = ExportMeta.clean(self.text)

        if not self.name:
            self.name = self.default_name

        super().save(*args,**kwargs)

class Site(models.Model):
    name = models.CharField(max_length=20)
    database = models.CharField(max_length=20)
    url = models.CharField(max_length=20)
    active = models.BooleanField(default=1)

    def __str__(self):
        return self.name

class GoogleFeed(models.Model):
    product = models.OneToOneField(Product,on_delete=models.CASCADE)

    def __str__(self):
        return self.product.__str__()

class Price(models.Model):
    frm = models.PositiveIntegerField()
    to = models.PositiveIntegerField()

    def __str__(self):
        return "%s - %s" % (self.frm,self.to)

class Percent(models.Model):
    price = models.ForeignKey(Price,null=True,on_delete=models.CASCADE)
    percent = models.FloatField(verbose_name='Процентная наценка')
    additional = models.PositiveIntegerField(null=True,default=0)

class AbstractStorage(models.Model):
    templates = {
        'ru':{
            'Product':{
                'title_template':"{obj.name} оптом и в розницу Игротека",
                'meta_keywords_template':"{obj.name}, {obj.name} купить,{obj.name} цена,{obj.name} оптом,{obj.name} описание",
                'meta_description_template':"{obj.name}. {item.text_availability}. Доставка по всей Украине. Гарантия, сервис, отзывы. Постоянным клиентам Скидки"
            }
            ,
            'Category':{
                'title_template':"{obj.name} оптом и в розницу Харьков, Киев и вся Украина",
                'meta_keywords_template':"{obj.name} купить, {obj.name} цена, {obj.name}",
                'meta_description_template':"{obj.name} доставка по Харькову и всей Украине. Время обработки заказов с 9 до 18."
            },
            'Brand':{
                'title_template':"Товары {obj.name} купить в магазине Игротека. Оптом и в розницу, широкий выбор. Отзывы, гарантия, сервис",
                'meta_keywords_template':"{obj.name} купить, {obj.name} оптом, {obj.name} купить оптом",
                'meta_description_template':"Товары производителя {obj.name} в магазине Игротека. Широкий выбор, низкие цены, оптом и в розницу."
            }
        },
        'ua':{
            'Product':{
                'title_template':"{obj.name} оптом і в роздріб Ігротека",
                'meta_keywords_template':"{obj.name}, {obj.name} купити,{obj.name} ціна,{obj.name} оптом,{obj.name} опис",
                'meta_description_template':"{obj.name}. {item.text_availability}. Доставка по всій Україні. Гарантія, сервіс, відгуки. Постійним клиєнтам Знижки"
            },
            'Category':{
                'title_template':"{obj.name} оптом и в роздріб Харків, Київ і вся Україна",
                'meta_keywords_template':"{obj.name} купити, {obj.name} ціна, {obj.name}",
                'meta_description_template':"{obj.name} доставка по Харкову і усій Україні. Час відпрацювання замовлень з 9 до 18."
            },
            'Brand':{
                'title_template':"Товари {obj.name} купити в магазині Ігротека. Оптом і в роздріб, широкий вибір. Відгуки, гарантія, сервіс",
                'meta_keywords_template':"{obj.name} купити, {obj.name} оптом, {obj.name} придбати оптом",
                'meta_description_template':"Товари виробника {obj.name} в магазині Ігротека. Широкий вибір, низькі ціни, оптом і в роздріб."
            }
        }
    }

    @property
    def view(self):
        return self.__class__.__name__

    @property
    def modelName(self):
        return self.__class__.__name__

    def names(self,lang):
        return self.name

    name = models.CharField(max_length=255,verbose_name='Имя')
    model = models.CharField(max_length=50,verbose_name='Артикул')
    active = models.BooleanField(default=1,verbose_name='Актив')

    def __str__(self):
        return self.name

    class Meta:
        abstract = True

    @property
    def is_active(self):
        return '<div class="bool %s"></div>' % str(self.active).lower()

class Storage(AbstractStorage):
    slug = None

    class Meta:
        verbose_name = 'Новые товары'
        verbose_name_plural = 'Новые товары'
        ordering = ['-active']

class Tigres(AbstractStorage):
    retail_price = models.PositiveIntegerField()
    big_opt_price = models.PositiveIntegerField()
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,related_name='tigres_product',null=True,on_delete=models.CASCADE)

    @property
    def image(self):
        gallery = self.gallery.first()
        return gallery if gallery else None

    @property
    def admin_image(self):
        if self.image:
            return "<img src='/media/%s'>" % self.image.image
        else:
            return "<img src='/media/data/no_image_new.jpg'>"

    class Meta:
        verbose_name = 'Тигрес'
        verbose_name_plural = 'Тигрес'
        ordering = ['-active']

class TigresGallery(AbstractGallery):
    product = models.ForeignKey(Tigres,related_name="gallery",on_delete=models.CASCADE)

    def save(self,*args,**kwargs):
        self.last_modified = timezone.now()

        models.Model.save(self,*args,**kwargs)

    class Meta:
        verbose_name = 'Картины Тигрес'
        verbose_name_plural = 'Картины Тигрес'

class Meta(models.Model):
    language = models.ForeignKey(Language,null=True,on_delete=models.SET_NULL)
    model_choices = (
        (0,'Product'),
        (1,'Category'),
        (2,'Brand'),
        (3,'Tag'),
        (4,'Page'),
        (5,'Article'),
        (6,'City'),
        (7,'Storage'),
    )
    model = models.IntegerField(choices=model_choices)
    title = models.CharField(max_length=100)
    meta_description = models.CharField(max_length=255)
    meta_keywords = models.CharField(max_length=255)

    class Meta:
        unique_together = ('language','model')