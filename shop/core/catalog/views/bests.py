from django.shortcuts import render
from cart.models import Item
from catalog.models import Offer,Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View
from shop.context import meta

class BestsellersView(View):
    def get(self,request,*args,**kwargs):
        context = {}
        offers = Offer.objects.filter(product__is_available=True)

        paginator = Paginator(list(offers), 30)
        try:
            offers = paginator.page(request.GET.get('page') or 1)
        except EmptyPage:
            offers = []

        context['products'] = [item.product for item in offers]

        if request.is_ajax():
            template = 'catalog/%s/more.html'
        else:
            template = 'catalog/%s/products.html'

        return render(request,template % request.folder,context)