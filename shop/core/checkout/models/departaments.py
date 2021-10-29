from django.db import models
from django.utils import timezone

__all__ = ['City','Departament']

choices = (
        (1,'np'),
        (2,'d')
    )
class City(models.Model):
    address_ua = models.CharField(max_length=255,null=True)
    address_ru = models.CharField(max_length=255)
    type = models.PositiveIntegerField(choices=choices,default=1)
    last_modified = models.DateTimeField(auto_now_add=True)

    def dict(self):
        return {'id':self.id,'address':self.address_ru,'type':self.type}

    def __str__(self):
        return self.address_ru

    def address(self,language):
        try:
            address = getattr(self,'address_%s' % language)
            return address if address else self.address_ru
        except:
            return self.address_ru

    def save(self):
        self.last_modified = timezone.now()

        super().save()

    class Meta:
        ordering = ['address_ru']

class Departament(models.Model):
    address_ua = models.CharField(max_length=255,null=True)
    address_ru = models.CharField(max_length=255)
    city = models.ForeignKey(City, related_name = 'departaments', on_delete=models.CASCADE)
    number = models.PositiveIntegerField(null=True)
    type = models.PositiveIntegerField(choices=choices,default=1)
    last_modified = models.DateTimeField(auto_now_add=True)

    def address(self,language):
        try:
            address = getattr(self,'address_%s' % language)
            return address if address else self.address_ru
        except:
            return self.address_ru

    def dict(self):
        return {'id':self.id,'address':self.address_ru,'type':self.type,'city':self.city.id}

    def __str__(self):
        return self.address_ru

    def save(self):
        self.last_modified = timezone.now()

        super().save()
