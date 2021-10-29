from catalog.models import Product,Brand,Attribute,Tag,Category
from django.core.paginator import Paginator
from catalog.clean import clean_filters
from django.shortcuts import render
from json import dumps
from itertools import chain
from settings import CACHE_URL
import os
from django.views.generic import View

class FilterView(View):
    def get(request,lang='ru'):
        filters, and_filters, exclude, ordering, page = clean_filters(request.GET.copy())
        root = '{CACHE_URL}html/{lang}/filters/'.format(lang=lang,CACHE_URL=CACHE_URL)
        path = root + request.GET.urlencode()

        if request.user.is_opt:
            filters['storage'] = 1

        products = Product.objects.filter(**filters).exclude(**exclude).distinct()
        for item in and_filters:
            products = products.filter(**dict((item,)))

        if ordering:
            products = products.order_by('storage',ordering)
        else:
            products = products.order_by('storage','-last_modified')

        if request.is_ajax() and page:
            filters['is_available'] = False
            unproducts = Product.objects.filter(**filters)
            for item in and_filters:
                unproducts = unproducts.filter(**dict((item,)))
            products = list(chain(products,unproducts))

        paginator = Paginator(list(products), 30)

        try:
            products = paginator.page(page or 1)
        except:
            products = []

        if request.is_ajax():
            template = 'catalog/%s/more.html' % request.folder
            context = {
                'products':products,
                'page':page
            }
        else:
            context = {
                'brands':Brand.objects.filter(product__in=products).distinct(),
                'products':products,
                'page':page,
                'filters':dumps(filters),
                'and_filters':dumps(and_filters),
                'storage':request.GET.get('storage'),
                'ordering':ordering
            }

            if filters.get('category__id'):
                category = Category.objects.get(id=filters.get('category__id'))
                brands = {'product__category':category,'product__is_available':True}

                context.update({
                    'attributes':Attribute.objects.filter(category=category).distinct(),
                    'tags':Tag.objects.filter(products__category=category,products__in=products).distinct(),
                    'category':category,
                    'breadcrumbs':category.breadcrumbs(lang=request.LANGUAGE_CODE),
                    'brands':Brand.objects.filter(**brands).distinct(),
                })
                products = Product.objects.filter(is_available=True,category=category)
                if products:
                    context.update({
                        'min_price':min([product.price for product in products]),
                        'max_price':max([product.price for product in products])
                    })

                request.meta = 'Категория'
                request.obj = category

            if filters.get('brand__id'):
                context['brand'] = Brand.objects.get(id=filters.get('brand__id'))
                categories = Category.objects.filter(products__brand=context['brand'],products__is_available=True).distinct()
                if len(categories) > 1:
                    context['categories'] = categories

            if filters.get('tag__id'):
                context['tag'] = Tag.objects.get(id=filters.get('tag__id'))

            template = 'catalog/%s/products.html' % request.folder

        response = render(request,template,context)

        return render(request,'shop/%s/index.html' % request.folder,context={'content':response.content})