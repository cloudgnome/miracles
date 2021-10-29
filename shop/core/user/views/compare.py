from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from catalog.models import Product
from json import loads

def compare(request,lang='ua'):
    json = loads(request.body.decode('utf8')) if request.body else {}

    context = {
        'title':_('Порівняння товарів'),
        'view':'Compare',
        'products':Product.objects.filter(id__in=json.get('compare',[]))
    }
    context['base'] = 'shop/base.html' if request.is_ajax() else 'shop/%s/index.html' % request.folder

    return render(request,'user/%s/compare.html' % request.folder,context)