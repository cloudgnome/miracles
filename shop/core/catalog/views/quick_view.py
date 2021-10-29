from django.shortcuts import render,get_object_or_404
from catalog.models import Product
from django.views.generic import View

class Quick_View(View):
    def get(self,request,*args,**kwargs):
        product = get_object_or_404(Product,id=kwargs['id'])
        return render(request,'catalog/%s/quick_view.html' % request.folder,{'product':product})
