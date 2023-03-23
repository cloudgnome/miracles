from main.list.model import ModelAdmin
from catalog.models import Featured
from django.db.models import Q
from main.forms import FeaturedForm

class FeaturedAdmin(ModelAdmin):
    model = Featured
    form = FeaturedForm
    head = (('id','id'),('Категория','category__name'))
    head_search = (('по id','id'),('по категории','category__description__name__icontains'))
    list_display = ('id','category.__str__')
    editTemplate = 'main/edit.html'

    def get_filters(self,value):
        return Q(category__description__name__icontains=value)