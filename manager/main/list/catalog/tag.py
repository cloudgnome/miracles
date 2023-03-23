from main.list.model import ModelAdmin
from catalog.models import Tag
from django.db.models import Q
from main.forms import TagForm

class TagAdmin(ModelAdmin):
    model = Tag
    form = TagForm
    head = (('id','id'),('Название','name'))
    head_search = (('по id','id'),('по названию','description__name__icontains'))
    list_display = ('id','__str__')