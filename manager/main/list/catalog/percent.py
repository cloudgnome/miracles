from main.list.model import ModelAdmin
from main.models import Percent
from main.forms import PercentForm

class PercentAdmin(ModelAdmin):
    model = Percent
    form = PercentForm
    editTemplate = 'main/edit.html'
    head = (('id','id'),('Цена','price'),('Наценка','percent'),('И накинуть еще','additional'))
    head_search = ((),(),(),())
    list_display = ('id','price','percent','additional')