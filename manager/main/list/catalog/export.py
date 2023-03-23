from main.list.model import ModelAdmin
from main.models import Export
from main.forms import ExportForm
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

class ExportAdmin(ModelAdmin):
    listView = 'List'
    model = Export
    form = ExportForm
    head = (('id','id'),(_('Цель'),'name'))
    head_search = (('по id','id'),(_('Цель'),'name'))
    list_display = ('id','__str__')
    editTemplate = 'main/edit.html'

    def search(self,value):
        if not value:
            return Q()

        return Q(name__icontains=value)