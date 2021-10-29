from catalog.models import Product,Brand,Category
from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from itertools import chain
from catalog.clean import clean_filters
from settings import BASE_URL

def search(request,lang='ua'):
    filters, and_filters, exclude, ordering, page = clean_filters(request.GET.copy())
    query = request.GET.get('q')

    if not query or len(query) < 3:
        return redirect('/')

    if request.is_ajax() and 'autocomplete' in request.GET:
        products = Product.objects.filter(Q(description__name__icontains=query) | Q(model__icontains=query),slug__isnull=False,is_available=True).exclude(**exclude).distinct()
        try:
            products = list(chain(Product.objects.filter(id=query,slug__isnull=False),products))
        except:
            pass

        if request.user.is_opt:
            products = products.filter(storage=1)

        products = products[:30]

        return render(request,'catalog/autocomplete.html',{'products':products})

    if request.user.is_opt:
        filters['storage'] = 1

    products = Product.objects.filter(Q(description__name__icontains=query) | Q(model__icontains=query) | Q(brand__description__name__icontains=query),slug__isnull=False,is_available=True,**filters).exclude(**exclude).distinct()

    unproducts = Product.objects.filter(Q(description__name__icontains=query) | Q(model__icontains=query) | Q(brand__description__name__icontains=query),slug__isnull=False,is_available=False,**filters).exclude(**exclude).distinct()
    
    if ordering:
        products = products.order_by('storage',ordering)
    else:
        products = products.order_by('storage','-last_modified')

    try:
        products = list(chain(Product.objects.filter(id=query,slug__isnull=False),products))
    except:
        pass

    products = list(chain(products,unproducts))

    paginator = Paginator(list(products), 24)
    try:
        products = paginator.page(page or 1)
    except:
        products = []

    context = {
        'q':query,
        'products': products,
        'h1':'Поиск "%s"' % query,
        'title':'%s | Поиск %s' % (BASE_URL,query)
    }

    if request.is_ajax():
        template = 'catalog/%s/more.html' % request.folder
    else:
        if products and len(products) > 4:
            context.update({
                'min_price':min([product.price for product in products]),
                'max_price':max([product.price for product in products]),
                'num_pages':paginator.num_pages
            })

        context['brands'] = Brand.objects.filter(product__in=products).distinct()
        context['view'] = 'Category'
        context['search_categories'] = Category.objects.filter(products__in=products).distinct()

        template = 'catalog/%s/search.html' % request.folder

    return render(request,template,context)