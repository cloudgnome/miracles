from django.http import Http404
from django.shortcuts import render
from django.views.generic import View
from shop.context import meta
from catalog.models import Brand
from catalog.management.commands.pricelist import Command

class PriceList(View):
    def get(self,request,*args,**kwargs):
        context = {
            'brands':Brand.objects.filter(active=True)
        }
        return render(request, 'catalog/%s/pricelist.html' % request.folder,context)

    def post(self,request,*args,**kwargs):
        if not request.POST or not request.user.is_opt:
            raise Http404

        filters = {
            'brand__id': request.POST.get('brand__id'),
            'is_available': True,
            'storage': 1
        }
        pricelist = 'pricelist.brand=' + str(filters.get('brand__id'))
        Command.generate_pricelist(name=pricelist,filters=filters)
        context = {
            'brands':Brand.objects.filter(active=True),
            'pricelist':pricelist
        }
        return render(request, 'catalog/%s/pricelist.html' % request.folder,context)