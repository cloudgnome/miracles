from django.http import HttpResponse, Http404
from user.views import authenticate

from django.views.generic import View
from tasks import stock

__all__ = ['StockView']

class StockView(View):
    def get(self,request,*args,**kwargs):
        if not authenticate(value=request.GET.get('username'),password=request.GET.get('password')):
            raise Http404('Ой все! Что-то пошло не так.')

        stock.apply_async()

        return HttpResponse('Задача запущена')