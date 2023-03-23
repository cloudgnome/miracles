from main.list.model import ModelAdmin
from user.models import Callback
from main.forms import CallbackForm
from django.db.models import Q

class CallbackAdmin(ModelAdmin):
    model = Callback
    form = CallbackForm
    head = (('id','id'),('Телефон','phone'),('Дата','date_add'))

    list_display = ('id','phone','date_add.strftime("%H:%M %d-%m-%Y")')

    def get_filters(self,value):
        return Q(phone__contains=value)