from django.db import models
from shop.models import Language
from redactor.fields import RedactorField
from django.utils.translation import ugettext_lazy as _
from settings import BASE_URL
from django.utils import timezone
from settings import COMPANY_NAME, PHONES

__all__ = ['Description']

class Description(models.Model):
    language = models.ForeignKey(Language, on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=255,verbose_name='Name')
    text = RedactorField(null=True,verbose_name='Описание',
        redactor_options={'lang': 'ru'},upload_to='tmp/igroteka/',allow_file_upload=False,allow_image_upload=True)
    json_text = models.CharField(max_length=10000,null=True)
    title = models.CharField(max_length=255,null=True)
    meta_description = models.CharField(max_length=255,null=True)
    meta_keywords = models.CharField(max_length=255,null=True)
    last_modified = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        verbose_name = 'Description'
        verbose_name_plural = 'Description'

    def save(self,*args,**kwargs):
        self.last_modified = timezone.now()

        if self.pk:
            from main.models import Meta

            template = Meta.objects.filter(language=self.language,model=list(dict(Meta.model_choices).values()).index(self.obj.model.__name__)).first()
            if template:
                self.title = self.title or template.title.format(**{'obj':self,'COMPANY_NAME':COMPANY_NAME})
                self.meta_description = self.meta_description or template.meta_description.format(**{'obj':self,'COMPANY_NAME':COMPANY_NAME,'PHONES':' '.join(PHONES)})[:255]
                self.meta_keywords = self.meta_keywords or template.meta_keywords.format(**{'obj':self,'COMPANY_NAME':COMPANY_NAME,'PHONES':' '.join(PHONES)})[:255]

        super().save(*args,**kwargs)

    def __str__(self):
        return self.name or ''

    def __repr__(self):
        return self.__str__()