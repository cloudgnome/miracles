from main.list.catalog import ProductAdmin
from main.models import Storage
from main.forms import StorageForm

class StorageAdmin(ProductAdmin):
    listView = 'List'
    model = Storage
    form = StorageForm
    head = (('id','id'),('Имя','name'),('Артикул','model'),('',''))
    head_search = (('по id','id'),('по названию','name__icontains'),('по артикулу','model__icontains'))
    list_display = ('id','name','model')

    def context(self,item):
        return {'href':'/Product/%s' % item.id}

    def list_extra_context(self,context):
        pass