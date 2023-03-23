from ajax_select import register, LookupChannel
from catalog.models import Product,Category,Brand,Prom,Tag
from beles.models import Category as BelesCategory

@register('prom')
class PromLookup(LookupChannel):
    model = Prom

    def get_query(self, q, request):
        return self.model.objects.filter(prom_id__icontains=q)[:5]

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.prom_id

@register('product')
class ProductLookup(LookupChannel):
    model = Product

    def get_query(self, q, request):
        return self.model.objects.filter(model__icontains=q)[:5]

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.names(lang='ru')

@register('brand')
class BrandLookup(LookupChannel):
    model = Brand

    def get_query(self, q, request):
        return self.model.objects.filter(description__name__icontains=q).distinct()[:5]

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.names(lang='ru')

@register('category')
class CategoryLookup(LookupChannel):
    model = Category

    def get_query(self, q, request):
        categories = self.model.objects.filter(description__name__icontains=q).distinct()[:5]
        if not len(categories):
            categories = self.model.objects.filter(active=True)

        return categories

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item

@register('tag')
class TagLookup(LookupChannel):
    model = Tag

    def get_query(self, q, request):
        tags = self.model.objects.filter(description__name__icontains=q).distinct()[:5]
        if not len(tags):
            tags = self.model.objects.filter(active=True)

        return tags

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.names(lang='ru')

@register('beles_category')
class BelesCategoryLookup(LookupChannel):
    model = BelesCategory

    def get_query(self, q, request):
        categories = self.model.objects.filter(description__name__icontains=q).distinct()[:5]
        if not len(categories):
            categories = self.model.objects.filter(active=True)

        return categories

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.name