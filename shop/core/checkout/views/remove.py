from django.shortcuts import render,Http404
from django.http import JsonResponse
from cart.views import Buyer

def remove(request,id):
    if request.is_ajax() and 'cart_id' in request.session:
        buyer = Buyer(request)
        buyer.remove_item(id)
        buyer.cart.save()
        items = {item.id:item.price for item in buyer.cart}
        return JsonResponse({'total':buyer.cart.total,'discount':buyer.cart.discount,'items':items})
    else:
        raise Http404