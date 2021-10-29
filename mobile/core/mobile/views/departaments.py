from django.http import JsonResponse,Http404
from checkout.models import City,Departament
from django.views.generic import View
from mobile.serializers import serialize,departaments

def city(request,type):
    cities = City.objects.filter(type=type)
    return JsonResponse({'success':1,'data':serialize(cities)})

def departament(request,type,city):
    departaments = Departament.objects.filter(type=type,city=city)
    return JsonResponse({'success':1,'data':serialize(departaments)})

def load_departaments(request):
    data = departaments()

    request.user.update_departaments = False
    request.user.save()

    return JsonResponse({'success':1,'data':data})