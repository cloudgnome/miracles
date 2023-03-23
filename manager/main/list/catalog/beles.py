from main.list.model import ModelAdmin
from beles.models import Beles,Category
from main.forms import BelesForm,BelesCategoryForm

class BelesAdmin(ModelAdmin):
    model = Beles
    form = BelesForm
    head = (('id','id'),('Название','name'),('',''),('Категория','category__name'),('Артикул','model'),('Цена зак','purchase_price'),('Пров.','checked'))
    head_search = (('по id','id'),('по названию','name__icontains'),(),('категория','beles_category__name__icontains'),('по артикулу','model__icontains'),('цена','purchase_price'),())
    list_display = ('id','name','image_url','category_name','model','purchase_price','is_checked')

class BelesCategoryAdmin(ModelAdmin):
    model = Category
    form = BelesCategoryForm