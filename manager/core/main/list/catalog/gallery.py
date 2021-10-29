from main.list.model import ModelAdmin
from catalog.models import Gallery

class GalleryAdmin(ModelAdmin):
    model = Gallery
    head = (('id','id'),('Название','name'))
    head_search = (('по id','id'),('по названию','name__icontains'))
    list_display = ('id','name')