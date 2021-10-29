from django.db import models

class Currency(models.Model):
    type_choices = (
        (0,'UAH'),
        (1,'EUR'),
        (2,'USD')
    )
    type = models.PositiveIntegerField(choices=type_choices,default=0,unique=True)
    value = models.FloatField()
