from catalog.models import Product
from django.http import JsonResponse

def rating(request,id,value):
    if request.user.is_authenticated:
        product = Product.objects.get(id=id)
        product.rating = round((product.rating + int(value)) / 2)
        product.update()
        return JsonResponse({'result':True})

    return JsonResponse({'result':False})