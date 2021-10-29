from django.http import JsonResponse
from checkout.models import City,Departament
from django.views.generic import View
from django.db.models import Q
from django.utils.translation import LANGUAGE_SESSION_KEY

class CityView(View):
    def get(self,request,*args,**kwargs):
        context = {}
        lang = request.session.get(LANGUAGE_SESSION_KEY)
        if lang == 'ua':
            address = '{ua} - {ru}'
        else:
            address = '{ru} - {ua}'

        context['items'] = [{'id':city.id,'address':address.format(**{'ru':city.address_ru, 'ua':city.address_ua})} for city in City.objects.filter(Q(address_ua__istartswith=kwargs['value']) | Q(address_ru__istartswith=kwargs['value']),type=kwargs['type']).distinct()]

        context['id'] = 'city'
        return JsonResponse(context)

class DepartamentView(View):
    def get(self,request,*args,**kwargs):
        context = {}
        lang = request.session.get(LANGUAGE_SESSION_KEY)

        if kwargs.get('value'):
            context['items'] = [{'id':dep.id,'address':dep.address(lang)} for dep in Departament.objects.filter(Q(address_ru__icontains=kwargs['value']) | Q(address_ua__icontains=kwargs['value']),type=kwargs['type'],city=kwargs['city']).distinct()]
        else:
            context['items'] = [{'id':dep.id,'address':dep.address(lang)} for dep in Departament.objects.filter(type=kwargs['type'],city=kwargs['city']).distinct()]


        context['id'] = 'departament'
        return JsonResponse(context)