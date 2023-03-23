from main.list.model import ModelAdmin
from catalog.models import Prom
from main.forms import PromForm

class PromAdmin(ModelAdmin):
    model = Prom
    form = PromForm
    head = (('id','id'),('Название','name'),('PromID','prom_id'),('',''),('Процент','percent'),('Все товары','full_store'))
    head_search = (('по id','id'),('по названию','name'),('по PromID','prom_id__contains'),(),('процент','percent'),())
    list_display = ('id','name','prom_id','link','percent','full')
    editTemplate = 'main/edit.html'