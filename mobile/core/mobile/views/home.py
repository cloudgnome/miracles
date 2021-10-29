from django.views.generic import View
from django.http import JsonResponse
from catalog.models import Product,Offer
from mobile.serializers import serialize
from settings import BIG_OPT_TOTAL

__all__ = ['HomeView']

class HomeView(View):
    def get(self,request,*args,**kwargs):
        latest = Product.objects.filter(slug__isnull=False,is_available=True).order_by('-id')[:18]
        special = Product.objects.filter(special__gt=0,is_available=True)[:18]
        offers = Offer.objects.filter(product__is_available=True)[:18]
        if request.user.is_opt:
            latest = latest.filter(storage=1)
            special = special.filter(storage=1)
            offers = offers.filter(storage=1)

        context = {
            'success':1,
            'data':{
                'latest':serialize(latest),
                'special':serialize(special),
                'offers':serialize(offers),
                'big_opt_total':BIG_OPT_TOTAL,
                'update_departaments':request.user.update_departaments
            }
        }
        return JsonResponse(context)