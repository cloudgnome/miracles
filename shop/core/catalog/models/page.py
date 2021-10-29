#-*- coding:utf-8 -*-
from django.db import models
from redactor.fields import RedactorField
from django.utils import timezone
from bs4 import BeautifulSoup as parser
from catalog.models import Slugify,Description,Slug

class PageDescription(Description):
    class Meta:
        db_table = 'page_description'
        unique_together = (('language','name'),('language','title'),('language','meta_description'))

class Page(Slugify):
    slug = models.CharField(max_length=255,verbose_name='URL',null=True)
    description = models.ManyToManyField(PageDescription,related_name="obj")
    last_modified = models.DateTimeField(auto_now_add=True)
    customView = models.CharField(max_length=20,default='Page')
    position_choices = (
            (1, 'header_menu'),
            (2, 'footer_menu'),
        )
    position = models.PositiveIntegerField(choices=position_choices,null=True)

    class Meta:
        verbose_name = 'Простые страницы'
        verbose_name_plural = 'Простые страницы'
        ordering = ['-id']