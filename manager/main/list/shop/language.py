from main.list.model import ModelAdmin
from shop.models import Language
from main.forms import LanguageForm

class LanguageAdmin(ModelAdmin):
    model = Language
    form = LanguageForm
    head = (('id','id'),('Название','name'),('Код','code'),())
    head_search = (('по id','id'),('по названию','name'),('по коду','code__icontains'),())
    list_display = ('id','name','code','admin_image')
    editTemplate = 'main/edit.html'