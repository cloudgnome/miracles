from main.list.model import ModelAdmin
from catalog.models import Slug
from main.forms import SlugForm

class SlugAdmin(ModelAdmin):
    model = Slug
    form = SlugForm
    head = (('id','id'),('URL','slug'),('View','view'),('model_id','model_id'))
    head_search = (('по id','id'),('по URL','slug__icontains'),('по view','view__icontains'),('по model_id','model_id'))
    list_display = ('id','__str__','view','model_id')
    editTemplate = 'main/edit.html'