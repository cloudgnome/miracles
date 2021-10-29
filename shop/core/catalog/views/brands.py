from catalog.models import Brand
from django.shortcuts import render
from django.views.generic import View
from shop.context import meta

class BrandsView(View):
    def get(self,request,*args,**kwargs):
        context = {}
        context['brands'] = Brand.objects.filter(active=True)

        return render(request,'catalog/%s/brands.html' % request.folder,context)