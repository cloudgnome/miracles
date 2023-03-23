from main.list.model import ModelAdmin
from catalog.models import Product,Add_Model
from main.forms import ProductForm,GalleryForm,Gallery
from django.db.models import Q
from base64 import b64decode
from django.core.files.base import ContentFile
from django.utils.translation import gettext as _
from re import sub,search
from main.models import Export,ExportStatus,ExportMeta
from django.db.models import Max,Min

class ProductAdmin(ModelAdmin):
    listView = 'ListProduct'
    model = Product
    form = ProductForm
    list_display = ('id','__str__','admin_image','model','price','available','brand_name','get_storage_display')
    list_search = [
        {
            'name':'id',
            'text':_('по id'),
            'query':'id',
            'ordering':'id',
            'head_text':'id'
        },
        {
            'name':'description__name',
            'text':_('по названию'),
            'query':'description__name__icontains',
            'ordering':'description__name',
            'head_text':_('Название')
        },
        {
            'name':'model',
            'text':_('по артикулу'),
            'query':'model',
            'ordering':'model',
            'head_text':_('Артикул')
        },
        {
            'name':'retail_price',
            'text':_('по цене'),
            'query':'retail_price',
            'ordering':'retail_price',
            'head_text':_('Розничная')
        },
        {
            'name':'is_available',
            'text':_('по наличию'),
            'query':'is_available',
            'ordering':'is_available',
            'head_text':_('Нал')
        },
        {
            'name':'brand',
            'text':_('по производителю'),
            'query':'brand__description__name__icontains',
            'ordering':'brand__description__name',
            'head_text':_('Произ-тель')
        },
        {
            'name':'storage',
            'text':_('по складу'),
            'query':'storage',
            'ordering':'storage',
            'head_text':_('Склад')
        },
    ]
    listTemplate = 'main/productList.html'
    itemsTemplate = 'main/productItems.html'

    def extraContext(self,context):
        context['exports'] = Export.objects.all()

        return context

    def list_extra_context(self,context):
        context['context'].update({
            'min_price':context['items'].aggregate(Min('retail_price')).get('retail_price__min',0),
            'max_price':context['items'].aggregate(Max('retail_price')).get('retail_price__max',0),
        })
        context['exports'] = Export.objects.all()

    def search(self,value):
        try:
            int(value)
            return Q(id=value) | Q(model__icontains=value) | Q(description__name__icontains=value)
        except:
            return Q(model__icontains=value) | Q(description__name__icontains=value)

    def saveExtras(self,json,product):
        if json.get('images'):
            for image in json.get('images'):
                try:
                    image = sub(r'data:image/[a-z]+;base64,','',image)
                    image = ContentFile(b64decode(image), name='{}.{}'.format(search(r'[a-z0-9A-Z]+',image[27:42])[0],'jpg'))
                    image = Gallery(image=image,product = product)
                    image.save()
                except Exception as e:
                    continue

        if json.get('remove_images'):
            Gallery.objects.filter(id__in=json.get('remove_images',[])).delete()

        product.add_model.all().delete()
        if json.get('add_model'):
            for model in json.get('add_model'):
                product.add_model.create(model=model)

        if json.get('export_status'):
            for status in json.get('export_status'):
                try:
                    export = Export.objects.get(id=status['id'])
                except Export.DoesNotExist:
                    continue

                try:
                    export = ExportStatus.objects.get(product=product,export=export)
                except ExportStatus.DoesNotExist:
                    if status.get('load') != None:
                        export = ExportStatus.objects.create(product=product,export=export)

                if status.get('load') != None:
                    export.load = status.get('load')

                if status.get('meta'):
                    meta = status.get('meta')

                    if not hasattr(export,'meta'):
                        export.meta = ExportMeta.objects.create(export=export)

                    if meta.get('name'):
                        export.meta.name = meta.get('name')

                    if meta.get('text'):
                        export.meta.text = meta.get('text')

                    export.meta.save()

                export.save()

class Add_ModelAdmin(ModelAdmin):
    model = Add_Model