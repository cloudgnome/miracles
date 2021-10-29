from django.db import models

class Sms(models.Model):
    text = models.CharField(max_length=1000)
    type = models.CharField(max_length=20)

    @property
    def name(self):
        return self.type