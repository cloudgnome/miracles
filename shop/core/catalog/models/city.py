#-*- coding:utf-8 -*-
from django.db import models
from redactor.fields import RedactorField
from django.utils import timezone
from bs4 import BeautifulSoup as parser
from catalog.models import Slugify,Description

class CityDescription(Description):
    class Meta:
        db_table = 'city_description'
        unique_together = (('language','name'),('language','title'),('language','meta_description'))

class City(Slugify):
    slug = models.CharField(max_length=255,verbose_name='URL',unique=True)
    description = models.ManyToManyField(CityDescription,related_name="obj")
    last_modified = models.DateTimeField(auto_now_add=True)
    view = 'Home'

    class Meta:
        verbose_name = 'Города'
        verbose_name_plural = 'Города'