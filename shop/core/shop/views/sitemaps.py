from functools import wraps
from catalog.models import Product,Category,Brand,Tag,City
from blog.models import Article
from django.utils import timezone
from shop.models import Settings,Language
from django.template.loader import render_to_string
from settings import BASE_URL,STATIC_ROOT
from django.http import HttpResponse

def x_robots_tag(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        response = func(request, *args, **kwargs)
        response['X-Robots-Tag'] = 'noindex, noodp, noarchive'
        return response
    return inner

@x_robots_tag
def sitemap(request):
    context = {}
    settings = Settings.objects.first()
    if not settings:
        Settings.objects.create()
    context['language'] = '/%s' % request.LANGUAGE_CODE if request.LANGUAGE_CODE != 'ru' else ''

    try:
        if timezone.now() < settings.sitemap_cache:
            with open(STATIC_ROOT + 'sitemap.xml','rb') as content:
                response = HttpResponse(content=content)
                response['Content-Type'] = 'application/xml'
                response['Content-Disposition'] = 'attachment; filename=sitemap.xml'
                return response
    except:
        pass

    context['languages'] = Language.objects.all()
    context['categories'] = Category.objects.filter(active=True)
    context['products'] = Product.objects.filter(is_available=True,slug__isnull=False)
    context['articles'] = Article.objects.filter(active=True)
    context['tags'] = Tag.objects.all()
    context['cities'] = City.objects.all()
    context['BASE_URL'] = BASE_URL

    content = render_to_string('shop/sitemap.xml', context)
    with open(STATIC_ROOT + 'sitemap.xml','w') as f:
        f.write(content)
        response = HttpResponse(content=content)
        response['Content-Type'] = 'application/xml'
        response['Content-Disposition'] = 'attachment; filename=sitemap.xml'
        settings.sitemap_cache = timezone.now() + timezone.timedelta(days=7)
        settings.save()
        return response