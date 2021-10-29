from django.views.generic import View
from django.http import JsonResponse
from django.shortcuts import render,get_object_or_404
from checkout.models import Order
from catalog.models import Product
from cart.models import Item
from django.db.models import Q
from itertools import chain

__all__ = ['CartView','remove','add']

class CartView(View):
    def get(self,request,*args,**kwargs):
        query = kwargs.get('query')
        product = Product.objects.filter(Q(model=query))
        products =  Product.objects.filter(Q(name__icontains=query) | Q(model__icontains=query))
        if product.first():
            products = products.exclude(model=product.first().model)
        products = chain(product,products[:7])
        return render(request,'search.html',{'products':products})

    def post(self,request,*args,**kwargs):
        data = loads(request.body.decode('utf-8'))
        items = data['items']
        order = Order.objects.get(id=kwargs['id'])

        cart = order.cart
        cart.save()

        data['result'] = True
        data['total'] = cart.total
        data['discount'] = cart.discount

        return JsonResponse(data)

def remove(request,id):
    item = get_object_or_404(Item,id=id)
    cart = item.cart
    cart.remove_item(item)
    item.delete()
    cart.save()

    return JsonResponse({'total':cart.total,'discount':cart.discount})

def add(request,product_id,order_id):
    product = get_object_or_404(Product,id=product_id)
    order = get_object_or_404(Order,id=order_id)
    cart = order.cart

    try:
        item = Item.objects.get(cart=cart,product=product)
        item.qty += 1
        item.save()
        cart.save()

        return JsonResponse({
            'total':item.total,
            'cart_total':cart.total,
            'discount':cart.discount,
            'id':item.id,
            'qty':item.qty,
            'price':item.price
        })
    except Item.DoesNotExist:
        item = Item.objects.create(cart=cart,product=product,qty=1,price=product.price)
        cart.add_item(item)
        cart.save()

        return JsonResponse({
            'price':product.price,
            'image':product.admin_image,
            'id':item.id,
            'total':item.total,
            'name':product.name,
            'storage':product.storage_icon,
            'cart_total':cart.total,
            'discount':cart.discount,
            'slug':product.slug,
            'qty':product.qty
        })