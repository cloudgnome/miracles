from ajax_select import register, LookupChannel
from catalog.models import Product,Category,Brand

@register('product')
class ProductLookup(LookupChannel):
    model = Product

    def get_query(self, q, request):
        return self.model.objects.filter(description__name__icontains=q).distinct()[:5]

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.names(lang='ru')

@register('brand')
class BrandLookup(LookupChannel):
    model = Brand

    def get_query(self, q, request):
        return self.model.objects.filter(description__name__icontains=q).distinct()[:5]

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.names(lang='ru')