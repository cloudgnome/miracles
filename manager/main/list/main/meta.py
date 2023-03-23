from main.list.model import ModelAdmin
from main.models import Meta
from main.forms import MetaForm

class MetaAdmin(ModelAdmin):
    model = Meta
    form = MetaForm
    head = (('id','id'),('Имя','name'),('URL','url'))
    head_search = (('по id','id'),('по model','model__icontains'),('по языку','language'),('по title','title'))
    list_display = ('id','get_model_display','language','title')
    editTemplate = 'main/edit.html'