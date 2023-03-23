from main.list.model import ModelAdmin
from catalog.models import Popular
from main.forms import PopularForm
from django.db.models import Q

class PopularAdmin(ModelAdmin):
    model = Popular
    form = PopularForm
    order_by = '-product_id'
    head = (('id','id'),('Товар','product__name'),('',''))
    head_search = (('по id','id'),('по названию','product__name__icontains'))
    list_display = ('product.id','product.__str__','product.admin_image')
    editTemplate = 'main/edit.html'

    def get_filters(self,value):
        return Q(product__name__icontains=value)