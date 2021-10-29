# -*- coding: utf-8 -*-
from django.db import models
from redactor.fields import RedactorField
from catalog.models import Slugify,Description

class BrandDescription(Description):
    class Meta:
        db_table = 'brand_description'
        unique_together = (('language','name'),('language','title'),('language','meta_description'))

class Brand(Slugify):
    country = models.CharField(max_length=255,verbose_name='Страна производитель')
    active = models.BooleanField(default=False,verbose_name="Сделать ссылкой?")
    slug = models.CharField(max_length=255,verbose_name='URL',unique=True)
    description = models.ManyToManyField(BrandDescription,related_name="obj")
    image = models.ImageField(upload_to='brand/',null=True,blank=True,verbose_name='Картинка')

    def icon(self):
        if self.image:
            return '<img src="{}" alt="{}">'.format(self.image,self.name)
        else:
            return ''

    def __str__(self):
        try:
            return self.description.first().name
        except:
            return ''

    class Meta:
        verbose_name = 'Производители'
        verbose_name_plural = 'Производители'