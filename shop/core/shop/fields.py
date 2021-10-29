from django.db import models

class JSONField(models.CharField):
    description = "JSON Field"

    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return value.split(',')