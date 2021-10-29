from django.http import JsonResponse
from catalog.models import Product
from django.db.models import Q
from itertools import chain
from mobile.serializers import serialize
from json import loads

def search(request):
    query = loads(request.body.decode('utf8')).get('query')

    products = Product.objects.filter(Q(name__icontains=query) | Q(model__icontains=query) | Q(brand__name__icontains=query),slug__isnull=False,is_available=True).distinct()

    if request.user.is_opt:
        products = products.filter(storage=1)

    products = products.order_by('storage','-last_modified')
    
    unproducts = Product.objects.filter(Q(name__icontains=query) | Q(model__icontains=query) | Q(brand__name__icontains=query),slug__isnull=False,is_available=False).distinct()

    products = list(chain(products,unproducts))

    return JsonResponse({'success':1,'data':serialize(products)})