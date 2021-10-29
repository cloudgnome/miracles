# -*- coding=utf-8 -*-
import re
import os
from PIL import Image
from math import ceil
from settings import DOMAIN,BASE_URL,CACHE_URL,STORAGE_CHOICES,OUT_OF_STOCK_MESSAGE,OUT_OF_STOCK_MESSAGE_HTML
from django.db.models import *
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from catalog.models import Value,Tag,Category,Brand,Description,Slugify
from redactor.fields import RedactorField
from django.core.paginator import Paginator

class ProductDescription(Description):
    class Meta:
        db_table = 'product_description'
        unique_together = (('language','name'),('language','title'),('language','meta_description'))

class Product(Slugify):
    model = CharField(max_length=50,verbose_name='Артикул',unique=True)
    slug = CharField(max_length=255,null=True,verbose_name='URL',unique=True)
    big_opt_price = FloatField(default=0,verbose_name='Биг-оптовая цена')
    retail_price = FloatField(default=0,verbose_name='Цена')
    purchase_price = FloatField(default=0,verbose_name='Закупочная цена')
    length = CharField(max_length=50,null=True,verbose_name='Длина')
    width = CharField(max_length=50,null=True,verbose_name='Ширина')
    height = CharField(max_length=50,null=True,verbose_name='Высота')
    is_available = BooleanField(default=0,verbose_name='В наличии')
    description = ManyToManyField(ProductDescription,related_name="obj")
    category = ManyToManyField(Category,verbose_name='Категория',related_name='products')
    brand = ForeignKey(Brand,null=True,verbose_name='Производитель',related_name='product', on_delete=SET_NULL)
    last_modified = DateTimeField(auto_now_add=True)
    price_fixed = BooleanField(default=0,verbose_name='Фикс.')
    featured = ManyToManyField('self',verbose_name='Похожие товары',blank=True)
    storage_choices = STORAGE_CHOICES
    storage = PositiveIntegerField(choices=storage_choices,null=True,verbose_name="Склад",default=1)
    attributes = ManyToManyField(Value,verbose_name="Атрибуты",related_name="products")
    tags = ManyToManyField(Tag,verbose_name="Теги",related_name="products")
    rating = PositiveIntegerField(default=5)
    qty = FloatField(default=0)
    currency_choices = (
        (0,'UAH'),
        (1,'EUR'),
        (2,'USD')
    )
    currency = PositiveIntegerField(choices=currency_choices,default=0)
    counter = CharField(max_length=10,default='шт.')
    is_top = BooleanField(default=0)

    user = False

    def __setattr__(self,field,value):
        if field == 'export_status':
            for export in value:
                if not self.export_status.filter(export__id=export['export_id']).update(load=export['load']):
                    self.export_status.create(export_id=export['export_id'],load=export['load'])

        else:
            super().__setattr__(field,value)

    @property
    def opt_price(self):
        return int(self.big_opt_price)

    @property
    def gallery_list(self):
        if hasattr(self, 'gallery'):
            return [image.hd_thumb for image in self.gallery.all()]

    def feedback_cache(self):
        super().cache()

    def cache(self):
        if not self.pk:
            return

        for category in self.category.all():
            if category.cached:
                category.cache()

        for tag in self.tags.all():
            if tag.cached:
                tag.cache()

        if self.brand and self.brand.cached:
            self.brand.cache()

        if hasattr(self,'offer') or hasattr(self,'special') or self in Product.objects.filter(is_available=True,slug__isnull=False).order_by('-id')[:6]:
            from catalog.models import Page

            for page in Page.objects.filter(customView='Home'):
                page.cache()

        if hasattr(self,'offer'):
            from catalog.models import Page

            for page in Page.objects.filter(customView='Bestsellers'):
                page.cache()

        if hasattr(self,'special'):
            from catalog.models import Page

            for page in Page.objects.filter(customView='Sale'):
                page.cache()

        if self in Product.objects.filter(is_available=True,slug__isnull=False).order_by('-id')[:30]:
            from catalog.models import Page

            for page in Page.objects.filter(customView='New'):
                page.cache()

        super().cache()

    def check_price(self):
        if self.pk and hasattr(self,'export'):
            try:
                oldPrice = Product.objects.values('retail_price').get(pk=self.pk)
            except Product.DoesNotExist:
                return

            if oldPrice != self.retail_price:
                for export in self.export.all():
                    export.price = None
                    export.save()

    def save(self,*args,**kwargs):
        if not self.big_opt_price:
            self.big_opt_price = self.retail_price

        self.check_price()

        for image in self.gallery.all():
            if not image.position:
                image.save()
            for thumb in image.thumb.all():
                thumb.delete()

        super().save(*args,**kwargs)

    @property
    def h1(self):
        return self.names(lang='ua')

    def dict(self):
        data = {
                'id':self.id,
                'name':self.names(lang='ua'),
                'price':self.price,
                'model':self.model,
                'storage':self.storage,
                'imageHeight':self.imageHeight,
                'is_available':self.is_available,
                'retail_price':self.retail_price,
                'big_opt_price':self.big_opt_price
            }

        data['gallery'] = [DOMAIN + self.image.large_thumb]

        if hasattr(self,'special'):
            data['special'] = True
        if hasattr(self,'offer'):
            data['offer'] = True
        if self.id > Product.objects.order_by('-id')[24].id:
            data['latest'] = True

        return data

    @property
    def mobile_description(self):
        description = self.description.first()
        if description:
            return description.text

        return 'Описание еще не добавлено'

    def get_export(self):
        return self.export_status.filter(export__name='Rozetka.ua').first()

    def detail(self):
        data = {
                'id':self.id,
                'name':self.names(lang='ua'),
                'model':self.model,
                'price':self.price,
                'size':self.parameters,
                'storage':self.storage,
                'description':self.mobile_description,
                'imageHeight':self.imageHeight,
                'is_available':self.is_available,
                'retail_price':self.retail_price,
                'brand':self.brand.names(lang='ua') if self.brand else '',
                'country':self.brand.country if self.brand else '',
                'big_opt_price':self.big_opt_price,'url':'%s/%s' % (DOMAIN,self.slug)
            }

        data['gallery'] = [DOMAIN + image.large_thumb for image in self.gallery.order_by('position')]

        if hasattr(self,'special'):
            data['special'] = True
        if hasattr(self,'offer'):
            data['offer'] = True
        if self.id > Product.objects.order_by('-id')[24].id:
            data['latest'] = True

        return data

    @property
    def imageHeight(self):
        try:
            thumb = self.image.thumb.get(size=600).url
            return Image.open(CACHE_URL + thumb).height
        except:
            return 600

    def __lt__(self,other):
        return self.created_at < other.last_modified

    @property
    def admin_image(self):
        return "<img src='%s'>" % self.image.admin_thumb

    def storage_icon(self):
        return '<img src="/static/icon/{0}.jpg" alt="{0}">'.format(self.get_storage_display())

    @property
    def brand_name(self):
        if self.brand:
            return self.brand.names(lang='ru').strip()
        else:
            return ''

    @property
    def available(self):
        return '<div class="clickable bool %s"></div>' % str(self.is_available).lower()

    @property
    def meta_image(self):
        gallery = self.gallery.first()
        if gallery:
            return gallery.preview_thumb
        else:
            return '/media/data/no_image_new.jpg'

    def cart_name(self):
        return ' '.join(self.names(lang='ua').split(' ')[0:2])

    @property
    def text_availability(self):
        if self.is_available:
            if self.storage == 1:
                return _('Есть в наличии')
            else:
                return OUT_OF_STOCK_MESSAGE
        else:
            return _('Нет в наличии')

    @property
    def availability(self):
        if self.is_available:
            if self.storage == 1:
                return _('<span>Есть в наличии</span>')
            else:
                return OUT_OF_STOCK_MESSAGE_HTML
        else:
            return _('<span class="notaval">Нет в наличии</span>')

    @property
    def product_availability(self):
        if self.is_available:
            if self.storage == 1:
                return _('<span><i class="far fa-check-circle"></i>Есть в наличии</span>')
            else:
                return OUT_OF_STOCK_MESSAGE_HTML
        else:
            return _('<span class="notaval"><i class="fas fa-exclamation-circle"></i>Нет в наличии</span>')

    @property
    def google_availability(self):
        if self.is_available:
            if self.storage == 1:
                return 'in stock'
            else:
                return 'out of stock'
        else:
            return 'preorder'

    @property
    def price(self):
        if self.user:
            if hasattr(self, 'special') and self.special.price < self.big_opt_price:
                return self.special.price
            else:
                return int(self.big_opt_price)
        elif hasattr(self, 'special'):
            return self.special.price
        else:
            if self.retail_price:
                return int(self.retail_price)

    @property
    def parameters(self):
        attrs = ''
        if not self.length and not self.width and not self.height:
            return ''
        if self.length and self.length != '0':
            attrs = attrs + self.length

        if self.width and self.width != '0':
            attrs = attrs + ' x ' + self.width

        if self.height and self.height != '0':
            attrs = attrs + ' x ' + self.height

        return attrs

    def breadcrumbs(self,lang):
        try:
            category = self.category.filter(parent__isnull=False).first()
            if not category:
                category = self.category.first()
            breadcrumbs = category.breadcrumbs(lang=lang,product = True)
        except:
            breadcrumbs = ()
        return breadcrumbs

    def category_name(self):
        return str(self.category.first())

    def google_category_name(self):
        try:
            return self.category.first().description.get(language__code='ru').name
        except:
            return ''

#####PROM.UA
    def get_category(self):
        try:
            return self.category.first()
        except:
            return ''

    def prom_category(self):
        try:
            return self.category.first()
        except:
            return ''

    def prom_images(self):
        images = self.gallery.all()
        s = ''
        if images:
            for image in images:
                try:
                    s += 'https://%s%s,' % (BASE_URL,image.image.url)
                except ValueError:
                    print('No file %s' % image.id)
                    image.delete()

        return s

    def prom_price(self):
        if self.is_available:
            return self.retail_price
        else:
            return ''

    def prom_percent_price(self,percent):
        if self.is_available:
            return ceil(self.retail_price + (self.retail_price * percent))
        else:
            return ''

    def prom_stock(self):
        if self.is_available:
            return '+'
        else:
            return '-'

    def prom_special(self):
        if hasattr(self,'special'):
            return self.retail_price - self.special.price
        else:
            return ''
#####END PROM.UA

    async def save_async(self,*args,**kwargs):
        print('saving')
        self.save(*args,**kwargs)
        print('saved')

    @property
    def image(self):
        gallery = self.gallery.order_by('position').first()
        return gallery if gallery else EmptyImage()

    def __str__(self):
        try:
            return self.description.first().__str__()
        except:
            return ''

    class Meta:
        ordering = ['-is_available','-last_modified','-is_top']
        verbose_name = 'Товары'
        verbose_name_plural = 'Товары'

class EmptyImage:
    def __getattr__(self,name):
        return '/media/data/no_image_new.jpg'

    def __str__(self):
        return '/media/data/no_image_new.jpg'

class Add_Model(Model):
    product = ForeignKey(Product,related_name='add_model', on_delete=CASCADE)
    model = CharField(max_length=255,verbose_name='Доп. Артикул')

    def __str__(self):
        return self.model

    class Meta:
        verbose_name = 'Доп. Артикул'
        verbose_name_plural = 'Доп. Артикул'