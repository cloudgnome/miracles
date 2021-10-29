from django.core.management.base import BaseCommand
from catalog.models import Product,Category,Brand,Tag,Page
from blog.models import Article
from django.utils import timezone
from shop.models import Language
import os
import re
from settings import CACHE_URL,BASE_URL
from catalog.views import router
from django.test import RequestFactory
from user.models import User
from django.http import Http404,HttpRequest
from django.utils import translation

class Command(BaseCommand):
    help = 'Sync Beles'

    def add_arguments(self, parser):
        parser.add_argument('--model', nargs='+', type=str)
        parser.add_argument('--id', nargs='+', type=str)
        parser.add_argument('--output', nargs='?', default=False)

    def handle(self, *args, **options):
        time = timezone.now()
        self.verbose = options.get('output')

        if options['model']:
            filters = {'model':options['model'][0]}
            try:
                item = Product.objects.get(**filters)
                self.create_cache(item)
            except Product.DoesNotExist:
                pass
        elif options['id']:
            filters = {'id':options['id'][0]}
            try:
                item = Product.objects.get(**filters)
                self.create_cache(item)
            except Product.DoesNotExist:
                pass
        else:
            for page in Page.objects.all():
                page.cache()
                self.create_cache(page)

            for product in Product.objects.filter(cached=False,slug__isnull=False):
                product.cache()
                self.create_cache(product)

            for category in Category.objects.filter(cached=False,slug__isnull=False,active=True):
                self.create_cache(category)

            for brand in Brand.objects.filter(cached=False,slug__isnull=False,active=True):
                self.create_cache(brand)

            for tag in Tag.objects.filter(cached=False,slug__isnull=False):
                self.create_cache(tag)

        print('Потрачено времени: %s' % (timezone.now() - time))
        print('Завершено.')

    def create_cache(self,item):
        request = HttpRequest()
        for device in ['mobile','desktop']:
            for lang in Language.objects.all():
                for user in [User.objects.filter(price_type=1).first(),User.objects.filter(price_type=2).first()]:
                    slug = '/'
                    if item.slug:
                        slug += item.slug

                    request.method = 'GET'
                    request.META['SERVER_NAME'] = BASE_URL
                    request.META['SERVER_PORT'] = 80
                    request.path = slug
                    request.folder = device
                    request.user = user
                    translation.activate(lang.code)
                    request.LANGUAGE_CODE = translation.get_language()

                    if self.verbose:
                        print(slug + '?opt='+ str(user.price_type) + '&lang=' + lang.code)

                    try:
                        router(request,lang=lang.code,slug=item.slug)
                    except Exception as e:
                        print('error %s %s' % (e,item.slug))