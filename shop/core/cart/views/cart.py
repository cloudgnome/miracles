#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render,get_object_or_404
from django.http import Http404,JsonResponse
from .buyer import Buyer
from catalog.models import Product
from django.views.generic import View
from django.utils.translation import ugettext_lazy as _
from json import loads

class CartView(View):
    def post(self,request,*args,**kwargs):
        buyer = Buyer(request)
        data = loads(request.body.decode('utf-8'))
        if not data.keys():
            buyer.clear_cart()
        for item in data.keys():
            try:
                buyer.add_item(item=Product.objects.get(id=item),qty=data[item])
            except:
                continue
        buyer.cart.save()

        items = list(buyer.cart)
        h2 = _('Корзина') if items else _('Ваша корзина пуста')
        return render(request,'cart/%s/cart.html' % request.folder,{'items_qty':buyer.cart.items_qty,'items':items,'h2':h2,'total':buyer.cart.total})

class RemoveView(View):
    def get(self,request,*args,**kwargs):
        if request.is_ajax() and 'cart_id' in request.session:
            context = {}
            buyer = Buyer(request)
            buyer.remove_item(kwargs['id'])
            return JsonResponse({'result':True})
        else:
            raise Http404

class ClearView(View):
    def get(self,request,*args,**kwargs):
        if 'cart_id' in request.session:
            buyer = Buyer(request)
            buyer.clear_cart()
        h2 = _('Ваша корзина пуста')
        return render(request,'cart/%s/cart.html' % request.folder,{'h2':h2})

def checkout(request):
    return Buyer(request).checkout()