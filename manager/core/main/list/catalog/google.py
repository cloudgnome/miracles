from main.list.model import ModelAdmin
from main.models import GoogleFeed
from django.db.models import Q
from main.forms import GoogleFeedForm

class GoogleFeedAdmin(ModelAdmin):
    listView = 'GoogleFeedList'
    model = GoogleFeed
    form = GoogleFeedForm
    head = (('product_id','product_id'),('Название','product'),('',''),('Артикул',''),('Цена',''),('',''),('Производитель',''),('Склад',''))
    head_search = (('по id','product_id'),('по названию','product__description__name__icontains'),('',''),('',''),('по цене','product__price'),('',''),('',''),('',''))
    list_display = ('product_id','__str__','product.admin_image','product.model','product.price','product.available','product.brand','product.get_storage_display')
    editTemplate = 'main/edit.html'