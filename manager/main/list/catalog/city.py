from main.list.model import ModelAdmin
from catalog.models import City
from main.forms import CityForm

class CityAdmin(ModelAdmin):
    model = City
    form = CityForm
    head = (('id','id'),('Название','name'))
    head_search = (('по id','id'),('по названию','name__icontains'))
    list_display = ('id','__str__')