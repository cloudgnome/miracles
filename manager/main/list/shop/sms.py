from main.list.model import ModelAdmin
from shop.models import Sms
from main.forms import SmsForm

class SmsAdmin(ModelAdmin):
    model = Sms
    form = SmsForm
    head = (('id','id'),('текст','text'),('тип','type'))
    head_search = (('по id','id'),('по тексту','text__icontains'),('по типу','type__icontains'))
    list_display = ('id','text','type')
    editTemplate = 'main/edit.html'