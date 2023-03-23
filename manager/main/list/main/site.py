from main.list.model import ModelAdmin
from main.models import Site
from main.forms import SiteForm

class SiteAdmin(ModelAdmin):
    model = Site
    form = SiteForm
    head = (('id','id'),('Имя','name'),('URL','url'))
    head_search = (('по id','id'),('по имени','name__icontains'),('по URL','url__icontains'))
    list_display = ('id','name','url')
    editTemplate = 'main/edit.html'