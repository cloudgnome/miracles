# -*- coding: utf-8 -*-
from django.template.loader import render_to_string
from catalog.models import Category,City
import os
from shop.models import Language
try:
    from settings import CATEGORIES_CLASS
except:
    CATEGORIES_CLASS = ""

def StaticView(request,root):
    context = {}
    context['navigation'] = Category.objects.filter(parent__isnull=True)
    context['cities'] = City.objects.all()
    context['lang'] = request.LANGUAGE_CODE
    context['languages'] = Language.objects.all()
    context['CATEGORIES_CLASS'] = CATEGORIES_CLASS

    if not os.path.isdir(root):
        try:
            os.makedirs(root)
        except FileExistsError:
            pass

    categories = render_to_string('shop/%s/nav.html' % request.folder,context=context).replace('\t','').replace('\n','')
    footer = render_to_string('shop/%s/footer.html' % request.folder,context=context).replace('\t','').replace('\n','')

    with open(root + 'categories.html','w',encoding='utf-8') as template:
        template.write(categories)

    with open(root + 'footer.html','w',encoding='utf-8') as template:
        template.write(footer)