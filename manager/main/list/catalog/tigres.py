from main.list.model import ModelAdmin
from catalog.models import TigresCategory
from django.db.models import Q
from main.forms import TigresCategoryForm,TigresForm
from main.models import Tigres
from main.list.catalog import ProductAdmin

class TigresCategoryAdmin(ModelAdmin):
    model = TigresCategory
    form = TigresCategoryForm
    head = (('id','id'),('Категория','url'),('Игротека','category'))
    head_search = (('по id','id'),('по названию','url__icontains'),('по названию','category__description__name__icontains'))
    list_display = ('id','url','category')
    editTemplate = 'main/edit.html'

class TigresAdmin(ProductAdmin):
    listView = 'List'
    model = Tigres
    form = TigresForm
    head = (('id','id'),('Имя','name'),('Артикул','model'),('Картина','image__image'))
    head_search = (('по id','id'),('по названию','name__icontains'),('по артикулу','model__icontains'),('',''))
    list_display = ('id','name','model','admin_image')

    def context(self,item):
        return {'href':'/edit/product/%s' % item.id,'id':item.id,'view':'Product'}