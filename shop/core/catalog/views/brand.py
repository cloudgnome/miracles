from catalog.models import Brand,Product,Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render,get_object_or_404
from django.views.generic import View
from django.http import Http404
from shop.context import meta
from catalog.clean import clean_filters

class BrandView(View):
    def get(self,request,brand,*args,**kwargs):
        filters, and_filters, exclude, ordering, page = clean_filters(request.GET.copy())

        filters.update({
            'brand':brand,
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

        paginator = Paginator(products, 30)
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
                'brand':brand,
                'brand_slug':brand.slug,
                'products':products
            }
            categories = Category.objects.filter(products__brand=brand,products__is_available=True).distinct()
            if len(categories) > 1:
                context['filter_categories'] = categories

            if products and len(products) > 4:
                prices = []
                for product in products:
                    if product.price:
                        prices.append(product.price)

                min_price = min(prices)
                max_price = max(prices)

                context['num_pages'] = paginator.num_pages
                if min_price + 10 < max_price:
                    context['min_price'] = min_price
                    context['max_price'] = max_price

            template = 'catalog/%s/products.html'

        return render(request,template % request.folder,context)