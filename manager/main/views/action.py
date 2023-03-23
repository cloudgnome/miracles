from django.http import JsonResponse
from json import loads
from catalog.models import Product
from main.models import Export

def product_export(request,product_id):
    try:
        product = Product.objects.get(id=product_id)

        export_status = product.export_status()
        return JsonResponse({
                'result':True,
                'data':{
                    'export':export_status
                }
            })

    except Product.DoesNotExist:
        return JsonResponse({'result':False})

def product_update_export(request,product_id):
    try:
        product = Product.objects.get(id=product_id)

        data = loads(request.body())
        product.export.filter(type=data.get('type')).update(load=data.get('load'))
    except Product.DoesNotExist:
        return JsonResponse({'result':False})

def availability(request,product_id):
    data = loads(request.body)

    try:
        product = Product.objects.get(id=product_id)
        availability = data.get('availability')
        if availability == False:
            product.is_available = False
        else:
            product.is_available = True
        product.save()

        return JsonResponse({'result':True})
    except Product.DoesNotExist:
        return JsonResponse({'result':False})

def action(request,type):
    data = loads(request.body)

    pass
