from django.db.models import ManyToManyField,CharField,Model,ImageField,DateTimeField,ForeignKey,SET_NULL
from redactor.fields import RedactorField
from catalog.models import Slugify,Description

class TagDescription(Description):
    class Meta:
        db_table = 'tag_description'
        unique_together = (('language','name'),('language','title'),('language','meta_description'))

class Tag(Slugify):
    slug = CharField(max_length=255,null=True,verbose_name='URL',unique=True)
    description = ManyToManyField(TagDescription,related_name="obj")
    image = ImageField(upload_to='data/tag/', blank=True, null=True,verbose_name='Картинка')
    last_modified = DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Теги'
        verbose_name_plural = 'Теги'