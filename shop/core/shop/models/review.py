#-*- coding:utf-8 -*-
from django.db import models

class Review(models.Model):
    parent = models.ForeignKey('self', null=True, related_name='child', on_delete=models.CASCADE)
    author = models.CharField(max_length=255, verbose_name='Автар')
    title = models.CharField(max_length=255,verbose_name="Заголовок")
    description = models.CharField(max_length=2000)
    active = models.BooleanField(default=0,verbose_name="Активен")
    created_at = models.DateTimeField(verbose_name="Дата добавления",auto_now_add=True)
    
    @property
    def db(self):
        return self._state.db

    @property
    def activity(self):
        return '<div class="bool %s"></div>' % str(self.active).lower()

    def is_child(self):
        return True if self.parent else False

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Отзывы'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']