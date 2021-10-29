from catalog.models import Product,Feedback,Featured
from django.shortcuts import render,get_object_or_404
from django.views.generic import View
from django.http import Http404
from calendar import timegm
from itertools import chain
from django.db.models import Q

try:
    from settings import OPT_LINK
except:
    OPT_LINK = 'igrushki-optom'

class ProductView(View):
    def get(self,request,product,*args,**kwargs):
        if product.user and not hasattr(product,'storage'):
            raise Http404()

        similar = Product.objects.filter(category=product.category.first(),is_available=True).exclude(model=product.model).order_by('storage')
        usimilar = Product.objects.filter(category=product.category.first(),is_available=False).exclude(model=product.model).order_by('storage')

        context = {
            'product':product,
            'related':product.featured.all()[:4] or Featured.objects.filter(category__in=product.category.all()).first(),
            'similar':list(chain(similar,usimilar))[:4],
            'breadcrumbs':product.breadcrumbs(lang=request.LANGUAGE_CODE),
            'feedbacks':Feedback.objects.filter(product=product),
            'next':Product.objects.filter(category__in=product.category.all(),id__gt=product.id).exclude(id=product.id).order_by('-is_available','id').first() or Product.objects.filter(category__in=product.category.all()).exclude(id=product.id).order_by('-is_available','id').first(),
            'prev':Product.objects.filter(category__in=product.category.all(),id__lt=product.id).exclude(id=product.id).order_by('-is_available','-id').first() or Product.objects.filter(category__in=product.category.all()).exclude(id=product.id).order_by('-is_available','-id').first(),
            'OPT_LINK':OPT_LINK
        }

        return render(request,'catalog/%s/product.html' % request.folder,context)