# -*- coding: utf-8 -*-
from django.db import models
from .product import Product

class Feedback(models.Model):
    product = models.ForeignKey(Product, related_name='feedback', on_delete=models.CASCADE)
    author = models.CharField(max_length=255,verbose_name='Автор')
    text = models.CharField(max_length=1500,verbose_name='Текст')
    active = models.BooleanField(default=True,verbose_name='Активен')
    parent = models.ForeignKey("self",blank=True,null=True,verbose_name='Родитель', related_name='children', on_delete=models.CASCADE)
    last_modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-id',]
        verbose_name = 'Отзывы'
        verbose_name_plural = 'Отзывы'