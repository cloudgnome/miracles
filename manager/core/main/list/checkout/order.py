from main.list.model import ModelAdmin
from checkout.models import Order
from main.forms import OrderForm
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext as _

class OrderAdmin(ModelAdmin):
    editTemplate = 'main/order.html'
    model = Order
    form = OrderForm
    listView = 'ListOrder'
    order_by = '-id'
    exclude = {'status__in':[6,3,8]}
    head = (('id','id'),('Имя','name'),('Фамилия','lname'),('Отчество','sname'),('Телефон','phone'),('Общая сумма','cart__total'),('Статус','status'),('Дата','created_at'))
    head_search = (('по id','id'),('по имени','name__icontains'),('по фамилии','lname__icontains'),('по отчеству','sname__icontains'),('по телефону','phone__icontains'),('по сумме','cart__total'),(),())
    list_display = ('id','name','lname','sname','phone','cart.total_currency','status_display','created_at.strftime("%d %b %H:%M")')

    def title(self,item):
        return _('Замовлення №') + str(item.id)

    def search(self,value):
        try:
            int(value)
            return Q(user__phone__contains=value) | Q(id=value) | Q(user__name__icontains=value) | Q(cart__items__product__model__icontains=value) | Q(ttn=value)
        except ValueError:
            return Q(user__phone__contains=value) | Q(user__name__icontains=value) | Q(cart__items__product__model__icontains=value) | Q(ttn=value)

    def extraContext(self,context):
        context.update({'date':str(timezone.now().date())})
        return context

    # def search(self,value):
    #     if not value:
    #         return Q()

    #     return (Q(cart__items__product__description__name__icontains=value) | Q(cart__items__product__model__icontains=value))