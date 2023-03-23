from main.models import Task
from settings import BASE_DIR,DOMAIN,CACHE_URL,STATIC_ROOT,COMPANY_NAME
from bs4 import BeautifulSoup
from catalog.models import Product,Currency,Category,Special
from math import ceil
import shutil
from impexp import load,dump
from django.utils import timezone
import pathlib
from datetime import timedelta
from django.template.loader import render_to_string
from checkout.models import City,Departament
from user.models import User
from shop.models import Settings
from requests import post
from json import loads

try:
    from settings import PARENT_DATABASE
except:
    PARENT_DATABASE = None

try:
    from settings import HOST,PROTOCOL
except:
    HOST = PROTOCOL = None

text = '{model}\t{title}\t{description}\t{link}\t{image_link}\t{availability}\t{price}\t{brand}\t{category}'
text_facebook = '{model}\t{title}\t{description}\t{link}\t{image_link}\t{availability}\t{price}\t{brand}\t{category}\t{condition}'

domain = 'https://%s/' % DOMAIN
domain_image = 'https://%s' % DOMAIN

def google_merchant(task_id):
    with open('{BASE_DIR}/{DOMAIN}/static/google_feed.txt'.format(BASE_DIR=BASE_DIR,DOMAIN=DOMAIN),'w') as f:
        f.write('id\ttitle\tdescription\tlink\timage_link\tavailability\tprice\tbrand\tgoogle product category')
        f.write('\n')
        products = Product.objects.filter(is_available=True,export_status__load=True,export_status__export__task__id=task_id)

        print(products)

        for product in products:
            description = product.description.filter(language__code='ru').first() or ''
            if description:
                try:
                    description = BeautifulSoup(description.text, "html.parser").text.replace('\n','').replace('\t','')[:5000]
                except:
                    description = ''
            f.write(text.format(model=product.model,title=product.names(lang='ru'),description=description,link=domain + product.slug,image_link=domain_image + product.image.list_thumb,availability=product.google_availability,price=str(product.price) + ' UAH',brand=product.brand_name,category=product.google_category_name()))
            f.write('\n')

    task = Task.objects.get(id=task_id)
    task.status = 2
    task.save()

def facebook_merchant(task_id):
    with open('{BASE_DIR}/{DOMAIN}/static/facebook_feed.txt'.format(BASE_DIR=BASE_DIR,DOMAIN=DOMAIN),'w') as f:
        f.write('id\ttitle\tdescription\tlink\timage_link\tavailability\tprice\tbrand\tgoogle product category\tcondition')
        f.write('\n')
        for product in Product.objects.filter(is_available=True,export_status__load=True,export_status__export__task__id=task_id):
            description = product.description.filter(language__code='ru').first() or ''
            if description:
                try:
                    description = BeautifulSoup(description.text, "html.parser").text.replace('\n','').replace('\t','')[:5000]
                except:
                    description = ''
            f.write(text_facebook.format(model=product.model,title=product.names(lang='ru'),description=description,link=domain + product.slug,image_link=domain_image + product.image.list_thumb,availability=product.google_availability,price=str(product.price) + ' UAH',brand=product.brand_name,category=product.google_category_name(),condition='new'))
            f.write('\n')

    task = Task.objects.get(id=task_id)
    task.status = 2
    task.save()

def currency_prices(task_id):
    for p in Product.objects.filter(currency=0):
        p.retail_price = ceil(p.retail_price)

        p.update()

    for p in Product.objects.exclude(currency=0):
        cur = Currency.objects.get(type=p.currency)
        p.retail_price = ceil(p.purchase_price * cur.value)

        p.update()

    shutil.rmtree(CACHE_URL + 'cache/html')

    task = Task.objects.get(id=task_id)
    task.status = 2
    task.save()

def clone_stock(items):
    if not PARENT_DATABASE:
        return

    related,data = dump(items)

    if related and data:
        load(related,data)

def stock(task_id,verbose=False):
    print(task_id)
    items = Product.objects.using(PARENT_DATABASE).filter(export_status__export__name=DOMAIN)
    new_items = []

    if verbose:
        print(items)

    for item in items:
        try:
            result = Product.objects.using(PARENT_DATABASE).values('is_available').get(model=item.model)
        except Product.DoesNotExist:
            if verbose:
                print('not_found:' + item.model)
            continue

        try:
            product = Product.objects.get(model=item.model)
            product.is_available = result.get('is_available')
            product.update()
        except Product.DoesNotExist:
            new_items.append(product)

    if len(new_items):
        pass
        # clone_stock(items)

    task = Task.objects.get(id=task_id)
    task.status = 2
    task.save()
    print(task.status)

def prices(task_id,verbose=False):
    items = Product.objects.values('model').all()

    if verbose:
        print(items)

    for item in items:
        try:
            result = Product.objects.using(PARENT_DATABASE).values('id','special__price','big_opt_price','retail_price').get(model=item.get('model'))
            Product.objects.filter(model=item.get('model')).update(
                retail_price=result.get('retail_price'),
                big_opt_price=result.get('big_opt_price')
            )

            p = Product.objects.get(model=item.get('model'))
            if result.get('special__price'):
                try:
                    Special.objects.create(product=p,price=result.get('special__price'))
                except:
                    p.special.price = result.get('special__price')
                    p.special.save()

            elif hasattr(p,'special'):
                p.special.delete()

        except Product.DoesNotExist:
            if verbose:
                print('not_found:' + item.get('model'))
            continue

    task = Task.objects.get(id=task_id)
    task.status = 2
    task.save()

def rozetka(task_id,verbose=False):
    if HOST and PROTOCOL:
        products = Product.objects.filter(is_available=True,slug__isnull=False,export_status__export__task__id=task_id,export_status__meta__isnull=False)
        
        for product in products:
            retail_price = product.price * 1.2
            for status in product.export_status.all():
                if retail_price != status.price:
                    status.price = retail_price
                    status.save()

        context = {
            'categories':Category.objects.filter(active=True),
            'products':products,
            'HOST':HOST,
            'PROTOCOL':PROTOCOL,
            'COMPANY_NAME':COMPANY_NAME
        }

        content = render_to_string('main/export.xml', context).replace('\n','').replace('\t','').replace('    ','')
        with open(STATIC_ROOT + 'export.xml','w') as f:
            f.write(content)

    task = Task.objects.get(id=task_id)
    task.status = 2
    task.save()

def hotline(task_id,verbose=False):
    if HOST and PROTOCOL:
        context = {
            'categories':Category.objects.filter(active=True),
            'products':Product.objects.filter(is_available=True,slug__isnull=False,export_status__export__task__id=task_id),
            'HOST':HOST,
            'PROTOCOL':PROTOCOL,
            'COMPANY_NAME':COMPANY_NAME
        }

        content = render_to_string('main/export1.xml', context).replace('\n','').replace('\t','').replace('    ','')
        with open(STATIC_ROOT + 'export1.xml','w') as f:
            f.write(content)

    task = Task.objects.get(id=task_id)
    task.status = 2
    task.save()

def np(task_id):
    settings = Settings.objects.first()

    url = "https://api.novaposhta.ua/v2.0/json/"
    data = {
        "modelName": "Address",
        "calledMethod": "getCities",
        "methodProperties": {},
        "apiKey": settings.api_key
    }
    departament = {
        "modelName": "AddressGeneral",
        "calledMethod": "getWarehouses",
        "methodProperties": {
            "CityRef":"",
        },
        "apiKey": settings.api_key
    }
    response = post(url,json=data)
    json = loads(response.text)

    for item in json['data']:
        try:
            city = City.objects.get(address_ua=item['Description'])
        except City.DoesNotExist:
            city = City()
            city.id = item['CityID']
            city.address_ua = item['Description']
            city.address_ru = item['DescriptionRu']
            city.type = 1

        city.save()

        City.objects.filter(last_modified__lt=timezone.now() - timedelta(days=1)).delete()

        departament['methodProperties']['CityRef'] = item['Ref']
        response = post(url,json=departament)
        departaments = loads(response.text)
        if departaments['data']:
            for dep in departaments['data']:
                try:
                    depar = Departament.objects.get(address_ua=dep['Description'])
                except Departament.DoesNotExist:
                    depar = Departament()
                    depar.address_ua = dep['Description']
                    depar.address_ru = dep['DescriptionRu']
                    depar.number = dep['Number']
                    depar.city = city
                    depar.type = 1

                depar.save()
            Departament.objects.filter(last_modified__lt=timezone.now() - timedelta(days=1)).delete()

    for user in User.objects.all():
        user.update_departaments = True
        user.save()

    task = Task.objects.get(id=task_id)
    task.status = 2
    task.save()