# -*- coding: utf-8 -*-
from django.db import models
from redactor.fields import RedactorField
from django.utils.html import strip_tags
from transliterate import slugify
from catalog.models import Slugify,Description,Product

class ArticleDescription(Description):
    class Meta:
        db_table = 'article_description'
        unique_together = (('language','name'),('language','title'),('language','meta_description'))

class Article(Slugify):
    slug = models.CharField(max_length=255,verbose_name="URL",blank=True,unique=True)
    description = models.ManyToManyField(ArticleDescription,related_name="obj")
    active = models.BooleanField(default=0,verbose_name="Активна")
    last_modified = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product)

    def text(self,lang):
        try:
            return self.description.get(language__code=lang).text
        except:
            if self.description.first():
                return self.description.first().text
            else:
                return ''

    def short_description(self):
        return strip_tags(self.description)[0:500]

    def __str__(self):
        return self.description.first()

    class Meta:
        verbose_name = 'Полезные статьи'
        verbose_name_plural = 'Полезные статьи'