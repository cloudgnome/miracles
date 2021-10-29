from catalog.models import Product,Tag,Brand,Attribute
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render,get_object_or_404
from django.views.generic import View
from django.http import Http404,HttpResponsePermanentRedirect
from itertools import chain
from shop.context import meta
from catalog.clean import clean_filters

class TagView(View):
    def get(self,request,tag,*args,**kwargs):
        filters, and_filters, exclude, ordering, page = clean_filters(request.GET.copy())

        filters.update({
            'tags':tag,
            'is_available':True
        })

        if request.user.is_opt:
            filters['storage'] = 1

        products = Product.objects.filter(**filters).exclude(**exclude).distinct()
        for item in and_filters:
            products = products.filter(**dict((item,)))

        if ordering:
            products = products.order_by(ordering,'storage','-last_modified')
        else:
            products = products.order_by('storage','-last_modified')

        filters['is_available'] = False
        unproducts = Product.objects.filter(**filters).distinct()
        products = list(chain(products,unproducts))

        paginator = Paginator(list(products), 30)
        try:
            products = paginator.page(page or 1)
        except EmptyPage:
            products = []

        if request.is_ajax():
            template = 'catalog/%s/more.html'
            context = {
                'products':products,
                'page':page
            }
        else:
            context = {
                'tag':tag,
                'tag_id':tag.id,
                'products':products
            }

            brand_filters = {
                'product__tags':tag,
                'product__is_available':True
            }

            brands = Brand.objects.filter(**brand_filters).distinct()
            if len(brands) > 1:
                context['brands'] = brands

            if products and len(products) > 4:
                min_price = min([product.price for product in products])
                max_price = max([product.price for product in products])
                if min_price + 10 < max_price:
                    context['min_price'] = min_price
                    context['max_price'] = max_price

            if products:
                for p in products:
                    category = p.category.first()
                    if category:
                        break
                else:
                    category = None

                context['attributes'] = Attribute.objects.filter(category=category)
                if category:
                    context['breadcrumbs'] = ((category.names(lang=request.LANGUAGE_CODE),category.slug,),)
                    context['tags'] = Tag.objects.filter(products__category=category).exclude(id=tag.id).distinct()

            template = 'catalog/%s/products.html'

        return render(request,template % request.folder,context)