from django.views.generic import View
from django.http import JsonResponse
from catalog.models import Product
from django.shortcuts import get_object_or_404
from mobile.serializers import serialize

class ProductView(View):
    def get(self,request,*args,**kwargs):
        context = {
            'success':1,
            'data':get_object_or_404(Product,id=kwargs.get('id')).detail()
        }
        return JsonResponse(context)