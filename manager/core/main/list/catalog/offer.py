from main.list.model import ModelAdmin
from catalog.models import Offer
from main.forms import OfferForm
from django.db.models import Q

class OfferAdmin(ModelAdmin):
    model = Offer
    form = OfferForm
    order_by = '-product_id'
    head = (('id','id'),('Товар','product__name'),('',''))
    head_search = (('по id','id'),('по названию','product__name__icontains'))
    list_display = ('product.id','product.__str__','product.admin_image')
    editTemplate = 'main/edit.html'

    def get_filters(self,value):
        return Q(product__name__icontains=value)