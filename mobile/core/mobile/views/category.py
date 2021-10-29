from django.views.generic import View
from django.http import JsonResponse
from catalog.models import Category,Product
from django.shortcuts import get_object_or_404
from mobile.serializers import serialize

class CategoryView(View):
    def get(self,request,*args,**kwargs):
        category = get_object_or_404(Category,id=kwargs.get('id'))
        products = serialize(Product.objects.filter(category=category,is_available=True).order_by('storage','-last_modified'))
        if request.user.is_opt:
            products = products.filter(storage=1)

        context = {
            'success':1,
            'data':products
        }
        return JsonResponse(context)