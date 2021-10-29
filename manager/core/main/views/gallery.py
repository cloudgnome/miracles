from catalog.models import Product
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from json import loads

def ordering(request,Model,id):
    product = get_object_or_404(Model.objects,id=id)
    ordering = loads(request.body.decode('utf8'))
    for id,position in ordering.items():
        image = product.gallery.get(id=id)
        image.position = position
        image.save()

    return JsonResponse({'result':True})