# -*- coding: utf-8 -*-
from django.db import models
from .product import Product
from django.utils import timezone
from PIL import Image, ImageEnhance
from settings import CACHE_URL,NO_IMAGE_PLACEHOLDER,WATERMARK
import os
from random import choice
from string import ascii_letters
from re import sub
from transliterate import slugify

try:
    from settings import WOTERMARK_SIZE, WOTERMARK_OPACITY
except:
    WOTERMARK_SIZE = None
    WOTERMARK_OPACITY = 0.3

class AbstractGallery(models.Model):
    product = models.ForeignKey(Product, related_name = 'gallery', on_delete=models.CASCADE)
    image = models.ImageField(max_length=255,upload_to='products/%Y/%m/%d', blank=True,verbose_name='Картинка')
    position = models.PositiveIntegerField(default=0,verbose_name='Порядоковый номер',blank=True)
    last_modified = models.DateTimeField(auto_now_add=True)
    size = {'list_thumb':260,'mobile_list_thumb':180,'admin_thumb':120,'cart_thumb':100,'mini_thumb':85,
            'large_thumb':800,'preview_thumb':288,'home_thumb':400,
            'checkout_thumb':50,'big_thumb':800,'gallery_thumb':300,'hd_thumb':1280}

    def url(self):
        return self.image.url

    def __str__(self):
        return self.preview_thumb

    def __getattr__(self,name):
        if name in self.size:
            try:
                thumb = Thumb.objects.get(image_id=self.pk,size=self.size[name])
                if thumb.url and os.path.isfile(CACHE_URL + thumb.url):
                    return thumb.url
                elif thumb.url:
                    try:
                        return self.thumbnail(self.size[name],path = thumb.url)
                    except Exception as e:
                        print(e)
            except Thumb.MultipleObjectsReturned:
                thumb = Thumb.objects.filter(image_id=self.pk,size=self.size[name]).first()
                if thumb.url and os.path.isfile(CACHE_URL + thumb.url):
                    return thumb.url
                elif thumb.url:
                    try:
                        return self.thumbnail(self.size[name],path = thumb.url)
                    except Exception as e:
                        print(e)
            except Thumb.DoesNotExist:
                pass
            try:
                return self.thumbnail(self.size[name])
            except Exception as e:
                print(e)

            return NO_IMAGE_PLACEHOLDER

        return super().__getattr__(name)

    def thumbnail(self,size,path = None):
        image = Image.open(self.image)

        if image.mode in ('RGBA','LA'):
            image.load()
            bg = Image.new('RGB',(image.size[0],image.size[1]),(255,255,255))
        else:
            bg = None

        if size > 270:
            image = self.watermarked(image)

        if bg:
            bg.paste(image,mask=image.split()[-1])
            image = bg
        else:
            image = image.convert('RGB')

        image.thumbnail([size,size])

        path = path or self.path(size)

        try:
            image.save(CACHE_URL[:-1] + path,'JPEG',quality=80)
        except FileNotFoundError:
            path = self.path(size)
            image.save(CACHE_URL[:-1] + path,'JPEG',quality=80)

        thumb = Thumb.objects.create(url = path,image=self,size=size)
        return thumb.url

    def path(self,size):
        name = '%s-%sx%s' % (self.product.slug,size,size)
        if self.position and self.position > 1:
            name = name + '-' + str(self.position)
        path = '/images/%s/%s/' % (name[0],name[1])
        root = CACHE_URL + path

        if not os.path.isdir(root):
            try:
                os.makedirs(root,mode=0o777)
            except FileExistsError:
                pass
        return path + name + '.jpg'

    def watermarked(self, image):
        opacity = WOTERMARK_OPACITY
        watermark = Image.open(WATERMARK)
        watermark = watermark.convert('RGBA')
        if WOTERMARK_SIZE:
            watermark.thumbnail([WOTERMARK_SIZE,WOTERMARK_SIZE])

        alpha = watermark.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        watermark.putalpha(alpha)
        square = Image.new('RGBA', image.size, (0,0,0,0))
        if WOTERMARK_SIZE:
            size = WOTERMARK_SIZE
        else:
            size = int((image.size[0] / 2) - (watermark.size[0] / 2))
        square.paste(watermark, (size,size))
        return Image.composite(square,  image,  square)

    def save(self,*args,**kwargs):
        self.last_modified = timezone.now()
        if not self.position:
            self.last()

        super().save(*args,**kwargs)

    def last(self):
        positions = sorted({i.id:i.position for i in Product.objects.get(id=self.product_id).gallery.all()}.items(), key=lambda x: (x[1] is None, x[1]), reverse=True)
        if positions and positions[0][1]:
            self.position = positions[0][1] + 1
        else:
            self.position = 1

    class Meta:
        abstract = True

class Gallery(AbstractGallery):
    class Meta:
        verbose_name = 'Изображения'
        verbose_name_plural = 'Изображения'
        ordering = ['position']

class Thumb(models.Model):
    url = models.CharField(max_length=255)
    image = models.ForeignKey(Gallery,related_name='thumb', on_delete=models.CASCADE)
    size = models.PositiveIntegerField()

    def __str__(self):
        return self.url