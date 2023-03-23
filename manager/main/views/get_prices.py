from django.http import HttpResponse,Http404
from catalog.models import Product
from io import StringIO

def get_prices(request):
    products = Product.objects.filter(storage="Игротека")

    f = StringIO()

    for p in products:
        f.write('%s\n' % p.model)
        if hasattr(p, 'special'):
            f.write('%s\n' % p.special.price)
        else:
            f.write('%s\n' % p.retail_price)

    f.seek(0,0)

    response = HttpResponse(f.read(),content_type='text/plain')
    response['Content-Disposition'] = "attachment; filename=opt_prices_res.txt"

    return response