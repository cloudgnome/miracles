from catalog.models import Product,Brand,Category,Attribute,Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render,get_object_or_404
from django.views.generic import View
from django.http import Http404,HttpResponsePermanentRedirect
from itertools import chain
from shop.context import meta
from catalog.clean import clean_filters
from django.db.models import Q
from json import dumps

class CategoryView(View):
    def get(self,request,category,*args,**kwargs):
        filters, and_filters, exclude, ordering, page = clean_filters(request.GET.copy(),model=Product)

        filters.update({
            'category__id':category.id,
            'is_available':True
        })

        if request.user.is_opt:
            filters['storage'] = 1

        if category.is_leaf_node():
            products = Product.objects.filter(**filters).exclude(**exclude).distinct()
            if and_filters.get('attributes__id'):
                for item in and_filters.get('attributes__id'):
                    products = products.filter(**{'attributes__id':item})

            if ordering:
                products = products.order_by(ordering,'storage','-is_top','-last_modified')
            else:
                products = products.order_by('storage','-is_top','-last_modified')

            filters['is_available'] = False

            unproducts = Product.objects.filter(**filters).distinct()
            if and_filters.get('attributes__id'):
                for item in and_filters.get('attributes__id'):
                    unproducts = unproducts.filter(**{'attributes__id':item})

            result_products = list(chain(products,unproducts))

            paginator = Paginator(result_products, 30)
            try:
                products = paginator.page(page or 1)
            except:
                products = []


            if request.is_ajax():
                template = 'catalog/%s/more.html'
                context = {
                    'products':products,
                    'page':page,
                }
            else:
                context = {
                    'category':category,
                    'breadcrumbs':category.breadcrumbs(lang=request.LANGUAGE_CODE),
                    'num_pages':paginator.num_pages
                }
                if category.parent:
                    context.update({
                        'aside_categories':category.parent.get_descendants()
                    })
                else:
                    context.update({
                        'aside_categories':Category.objects.filter(parent__isnull=True,active=True)
                    })

                brands = {'product__category':category,'product__is_available':True}

                if result_products:
                    prices = []
                    for product in result_products:
                        if product.price:
                            prices.append(product.price)

                    if prices:
                        context.update({
                            'min_price':min(prices),
                            'max_price':max(prices)
                        })

                del filters['is_available']

                context.update({
                    'page':page,
                    'products':products,
                    'category_id':category.id,
                    'attributes':Attribute.objects.filter(category=category),
                    'brands':Brand.objects.filter(**brands).distinct(),
                    'tags':Tag.objects.filter(products__category=category).distinct(),
                    'filters':dumps(filters),
                    'and_filters':and_filters
                })

                template = 'catalog/%s/products.html'
        else:
            context = {
                'products':Product.objects.filter(Q(**filters) | Q(category__in=category.get_descendants(),**filters))[:20],
                'categories':category.get_descendants(),
                'breadcrumbs':category.breadcrumbs(lang=request.LANGUAGE_CODE),
                'and_filters':and_filters,
                'category':category
            }
            if category.parent:
                context['aside_categories'] = category.parent.get_descendants()
            else:
                context['aside_categories'] = Category.objects.filter(parent__isnull=True,active=True)

            template = 'catalog/%s/category.html'

        return render(request,template % request.folder,context)