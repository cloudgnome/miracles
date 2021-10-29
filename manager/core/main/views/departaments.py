from checkout.models import City,Departament
from django.http import JsonResponse

def city(request, type, value = None):
    items = [{'id':city.id,'address':city.address_ru} for city in City.objects.filter(type=type,address_ru__istartswith=value)]

    return JsonResponse(items,safe=False)

def departaments(request, type, city_id = None, value = None):
    if value:
        items = [{'id':dep.id,'address':dep.address_ru} for dep in Departament.objects.filter(type=type,city_id=city_id,address_ru__contains=value)]
    else:
        items = [{'id':dep.id,'address':dep.address_ru} for dep in Departament.objects.filter(type=type,city_id=city_id)]

    return JsonResponse(items,safe=False)