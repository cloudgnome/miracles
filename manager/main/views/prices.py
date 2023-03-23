from django.http import HttpResponse, Http404
from user.views import authenticate
from django.views.generic import View
from tasks import prices

__all__ = ['PricesView']

class PricesView(View):
    articles = {}
    percents = False

    def dispatch(self,request,*args,**kwargs):
        if not authenticate(value=request.GET.get('username'),password=request.GET.get('password')):
            raise Http404('Неправильный юзер или парол.')
        return super().dispatch(request,*args,**kwargs)

    def get(self,request,*args,**kwargs):

        prices.apply_async()

        return HttpResponse('Задача поставлена в очередь')


