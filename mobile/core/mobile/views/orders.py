from checkout.models import Order
from checkout.forms import CheckoutForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from mobile.serializers import serialize
from json import loads
from django.views.generic import View

def orders(request):
    orders = Order.objects.filter(user=request.user)
    orders = serialize(orders)

    return JsonResponse({'success':1,'data':orders})

class OrderView(View):
    def get(self,request,*args,**kwargs):
        order = get_object_or_404(Order,id=kwargs['id'])

        return JsonResponse({'success':1,'data':order.detail()})

    def post(self,request,*args,**kwargs):
        order = get_object_or_404(Order,id=kwargs['id'])
        data = loads(request.body.decode('utf8'))

        form = CheckoutForm(order.init_form(data),instance = order)
        if form.is_valid():
            order = form.save()

        if data.get('cart'):
            for id in data['cart'].keys():
                item = order.cart.items.get(id=id)
                item.qty = data['cart'][id]
                item.save()
            order.cart.save()

        return JsonResponse({'success':1,'data':order.detail(),'errors':form.errors})