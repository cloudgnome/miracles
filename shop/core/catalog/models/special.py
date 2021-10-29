# -*- coding: utf-8 -*-
from django.db import models
from .product import Product
from decimal import Decimal
from math import ceil

class Popular(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name='Товар',
        unique = True,
    )
    def dict(self):
        return self.product.dict()

    # def save(self,*args,**kwargs):
    #     super().save(*args,**kwargs)
    #     from catalog.models import Page

    #     for page in Page.objects.filter(view='Home'):
    #         page.cache()

    @property
    def id(self):
        return self.product.id

    def __str__(self):
        return self.product.name;

    class Meta:
        verbose_name = 'Популярные'
        verbose_name_plural = 'Популярные'

class Special(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name='Товар',
        unique = True,
    )
    price = models.PositiveIntegerField(default=0,verbose_name='Спец.Цена')
    percent = models.PositiveIntegerField(default=0)

    def save(self,*args,**kwargs):
        if self.price < self.product.retail_price:
            self.percent = ceil(100 - ((self.price * 100) / self.product.retail_price))
        super().save(*args,**kwargs)
        self.product.cache()

    @property
    def price_currency(self):
        return '%s грн.' % self.price

    @property
    def db(self):
        return self._state.db

    def __str__(self):
        return self.product.__str__();

    class Meta:
        verbose_name = 'Акции'
        verbose_name_plural = 'Акции'

class Offer(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name='Товар',
        unique = True,
    )
    def dict(self):
        return self.product.dict()

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        from catalog.models import Page

        for page in Page.objects.filter(view='Home'):
            page.cache()

    @property
    def id(self):
        return self.product.id

    def __str__(self):
        return self.product.name;

    class Meta:
        verbose_name = 'Рекомендуемые'
        verbose_name_plural = 'Рекомендуемые'