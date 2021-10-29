#-*- coding:utf-8 -*-
from django.db import models

class Slider(models.Model):
    path = models.CharField(max_length=255,verbose_name="URL")
    image = models.ImageField(max_length=255,upload_to='data/slider/',verbose_name='Изображение')
    position = models.PositiveIntegerField(verbose_name='Порядковый номер')
    name = models.CharField(max_length=255)
    
    @property
    def db(self):
        return self._state.db

    def __str__(self):
        return "слайдер %s для %s" % (self.image,self.path)
    def __unicode__(self):
        return "слайдер %s для %s" % (self.image,self.path)

    class Meta:
        verbose_name = 'Слайдер'
        verbose_name_plural = 'Слайдер'
        ordering = ['position']

    @property
    def image_preview(self):
        if self.image:
            return u'<img id="slider-preview" src="/media/%s">' % self.image
        else:
            return 'Нет картинки'

    def image_path(self):
        if self.image:
            return "/media/%s" % self.image
        else:
            return 'Нет картинки'

    def position_html(self):
        return "<div class='position'>%s</div>" % self.position
    position_html.short_description = 'Порядковый номер'
    position_html.allow_tags = True