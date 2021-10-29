from catalog.models import Product
from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from shop.context import meta

class SaleView(View):
    def get(self,request,*args,**kwargs):
        context = {}
        if request.user.is_opt:
            context['products'] = Product.objects.filter(is_available=True,storage=1,special__gt=0)
        else:
            context['products'] = Product.objects.filter(is_available=True,special__gt=0)

        paginator = Paginator(list(context['products']), 30)

        try:
            context['products'] = paginator.page(request.GET.get('page') or 1)
        except EmptyPage:
            context['products'] = []

        if request.is_ajax():
            template = 'catalog/%s/more.html'
        else:
            template = 'catalog/%s/products.html'

        return render(request,template % request.folder,context)