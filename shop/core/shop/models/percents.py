from django.db import models
from shop.models import Site

class Percents(models.Model):
    site = models.CharField(max_length=255,verbose_name='Сайт')
    before_twenty = models.FloatField(default=3, verbose_name="до 20")
    twenty_thirty = models.FloatField(default=2, verbose_name="20-30")
    thirty_fifty = models.FloatField(default=1.7, verbose_name="30-50")
    fifty_hundred = models.FloatField(default=1.5, verbose_name="50-100")
    hundred_threehundred = models.FloatField(default=1.4, verbose_name="100-300")
    threehundred_fivehundred = models.FloatField(default=1.25, verbose_name="300-500")
    fivehundred_onethousand = models.FloatField(default=1.2, verbose_name="500-1000")
    onethousand_twothousand = models.FloatField(default=1.15, verbose_name="1000-2000")
    default = models.FloatField(default=1.1,verbose_name="более 2к")

    class Meta:
        verbose_name = 'Наценка'
        verbose_name_plural = 'Наценка'

    def __str__(self):
        return "Наценка %s" % self.site.domain