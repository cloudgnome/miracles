from catalog.models import Product
from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from shop.context import meta

class NewView(View):
    def get(self,request,*args,**kwargs):
        page = request.GET.get('page')

        if request.user.is_opt:
            products = Product.objects.filter(is_available=True,slug__isnull=False,storage=1).order_by('-id')[:250]
        else:
            products = Product.objects.filter(is_available=True,slug__isnull=False).order_by('-id')[:250]

        paginator = Paginator(products, 30)
        try:
            products = paginator.page(page or 1)
        except:
            products = []

        if request.is_ajax():
            template = 'catalog/%s/more.html'
        else:
            template = 'catalog/%s/products.html'

        context = {
            'products':products,
            'page':page,
            'num_pages':paginator.num_pages
        }

        return render(request,template % request.folder,context)