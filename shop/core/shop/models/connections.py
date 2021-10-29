from django.db import models
from datetime import timedelta
from django.utils import timezone

class Connection(models.Model):
    url = models.CharField(max_length=255,unique=True)
    limit = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    stop_at = models.DateTimeField()

    @property
    def overloaded(self):
        if self.limit > 10:
            return True
        else:
            return False

    def update(self,*args,**kwargs):
        super().save(*args,**kwargs)

    def save(self,*args,**kwargs):
        self.stop_at = timezone.now() + timedelta(minutes=1)

        super().save(*args,**kwargs)