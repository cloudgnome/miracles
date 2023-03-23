from main.list.model import ModelAdmin
from catalog.models import Special
from django.db.models import Q
from main.forms import SpecialForm

class SpecialAdmin(ModelAdmin):
    model = Special
    form = SpecialForm
    order_by = '-product_id'
    head = (('Цена','price'),('Товар','product__name'),('',''))
    head_search = (('по цене','price'),('по названию','product__description__name__icontains'))
    list_display = ('price_currency','product.__str__','product.admin_image')
    editTemplate = 'main/edit.html'

    def get_filters(self,value):
        return Q(product__description__name__icontains=value)