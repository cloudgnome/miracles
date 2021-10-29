from main.list.model import ModelAdmin
from catalog.models import Page
from main.forms import PageForm

class PageAdmin(ModelAdmin):
    model = Page
    form = PageForm
    head = (('id','id'),('Название','name'))
    head_search = (('по id','id'),('по названию','description__name__icontains'))
    list_display = ('id','__str__')