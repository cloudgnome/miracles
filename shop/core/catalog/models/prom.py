# -*- coding: utf-8 -*-
from django.db import models
from catalog.models import Category

class Prom(models.Model):
    name = models.CharField(max_length=255,verbose_name="Имя")
    prom_id = models.CharField(max_length=255,verbose_name="prom_id")
    link = models.CharField(max_length=255,verbose_name="Ссылка",null=True)
    percent = models.FloatField(verbose_name='Наценка',default=0.1)
    full_store = models.BooleanField(default=0,verbose_name="Все товары?")

    @property
    def full(self):
        return '<div class="bool %s"></div>' % str(self.full_store).lower()

    def __str__(self):
        return self.prom_id

    class Meta:
        verbose_name = "Prom"
        verbose_name_plural = "Prom"

class Prom_Category(models.Model):
    prom = models.ForeignKey(Prom,related_name="categories", on_delete=models.CASCADE)
    category = models.ForeignKey(Category,related_name="proms", on_delete=models.CASCADE)
    prom_category_id = models.PositiveIntegerField()

    def remove_duplicates(self):
        for pc in self.objects.all():
            i = 0
            for p in self.objects.filter(prom_category_id=pc.prom_category_id):
                if i == 0:
                    i+=1
                    continue
                p.delete()
                i+=1

    def __str__(self):
        return str(self.prom_category_id)

    class Meta:
        verbose_name = "ID Категории Prom"
        verbose_name_plural = "ID Категории Prom"
