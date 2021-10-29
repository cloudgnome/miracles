#-*- coding:utf-8 -*-
from django.db import models
from shop.models import Settings

class Phones(models.Model):
    number = models.CharField(max_length=20,verbose_name='Номер телефона')
    setting = models.ForeignKey(Settings, on_delete=models.CASCADE, related_name='phones')

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = 'Номер телефона'
        verbose_name_plural = 'Номер телефона'