from main.list.model import ModelAdmin
from shop.models import Slider
from main.forms import SliderForm

class SliderAdmin(ModelAdmin):
    model = Slider
    form = SliderForm
    head = (('id','id'),('Название','name'),('URL','path'),('Картина',''))
    list_display = ('id','name','path','image_preview')
    editTemplate = 'main/edit.html'