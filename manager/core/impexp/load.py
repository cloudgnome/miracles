from json import loads
from datetime import datetime
import importlib
import re
from django.db import IntegrityError
import csv
from catalog.models import Currency,Gallery,Product,ProductDescription,Category,Brand,BrandDescription,CategoryDescription
from shop.models import Language
from django.utils import timezone
import os
from requests import get
from requests.exceptions import MissingSchema
from transliterate import slugify
from settings import MEDIA_ROOT
from random import randint
from django.db.models import Q

prom_associate_data = {'Код_товара': 'model',
 'Название_позиции': 'name',
 'Цена': 'retail_price',
 'Ссылка_изображения': 'image',
 'Название_группы': 'category_name',
 'Адрес_подраздела': 'category_slug',
 'Идентификатор_группы': 'category_id',
 'Производитель': 'brand',
 'Страна_производитель': 'country',
 'Продукт_на_сайте': 'slug',
 'Наличие':'is_available',
 'Валюта':'currency',
 'Описание':'text',
 'Вес,кг': 'weight',
 'Ширина,см': 'width',
 'Высота,см': 'height',
 'Глубина,см': 'length',
 'HTML_заголовок': 'title',
 'HTML_описание': 'meta_description',
 'HTML_ключевые_слова': 'meta_keywords',
 'Единица_измерения':'counter',
 'Оптовая_цена':'opt_price',
}

def import_json(items,Model):
    items = loads(items)

    fields = Model._meta.fields

    columns = []
    for field in fields:
        columns.append(field.column)

    for i in items:
        description = i.get('description')
        del i['description']
        data = {}
        for c in columns:
            data[c] = i.get(c)

        try:
            item = Model.objects.create(**data)
        except Exception as e:
            try:
                item = Model.objects.get(id=data['id'])
            except Model.DoesNotExist:
                continue

        for d in description:
            try:
                item.description.create(**d)
            except IntegrityError:
                pass

base_url = 'https://ckl.com.ua%s'
def save_prom_image(src):
    src = src
    image = slugify(src.replace('https://ckl.com.ua/','').replace('https://images.ua.prom.st/',''),language_code='uk') + ".jpg"
    path = MEDIA_ROOT + '/%s/%s/'
    db_path = '%s/%s/%s' % (image[0],image[1],image)
    path = path % (image[0],image[1])

    print(src)

    if not os.path.isdir(path):
        os.makedirs(path)

    path = path + image

    if not os.path.isfile(path):
        r = get(src)

        print(r.status_code)
        if r.status_code == 200:
            with open(path, 'wb') as f:
                for chunk in r.iter_content():
                    f.write(chunk)

    return db_path

def load_category(name,data,d,language):
    url = d.get('url')[1:]
    try:
        c = Category.objects.get(slug=url)
    except Category.DoesNotExist:
        c = Category.objects.create(slug=url)

    print(c)

    try:
        cd = CategoryDescription.objects.get(name=name,language=language)
    except CategoryDescription.DoesNotExist:
        cd = CategoryDescription.objects.create(name=name,text=d.get('description'),language=language)

    c.description.add(cd)

    if d.get('parent'):
        parent = d.get('parent')
        try:
            c.parent = Category.objects.get(description__name=parent,description__language=language)
        except Category.DoesNotExist:
            c.parent = load_category(parent,data,data[parent],language)

    if d.get('image'):
        image = d.get('image')
        if not c.image:
            c.image = save_prom_image(image)

    c.save()

    return c

def prom_categories(filename):
    f = open(filename,'r')
    data = loads(f.read())
    language = Language.objects.get(id=1)

    for name in data.keys():
        d = data[name]
        load_category(name,data,d,language)

def prom_products_csv(filename,only_price=False):
    f = open(filename,'r')
    data = csv.reader(f,delimiter=',',quotechar='"')
    ps = [i for i in data]
    cs = ps[0]
    ps = ps[1:]

    print(cs)
    print(ps[18])

    data = [{cs[i]: p[i] for i in range(0,len(p))} for p in ps]

    items = []
    for item in data:
        item_data = {}
        for field in item.keys():
            f = prom_associate_data.get(field)
            if f:
                item_data[f] = item.get(field)
        items.append(item_data)

    language = Language.objects.get(id=1)

    for item in items:
        if not only_price:
            slug = slugify(item['category_name'].strip())
            try:
                category = Category.objects.get(description__name=item['category_name'].strip(),slug=slug)
            except:
                try:
                    cd = CategoryDescription.objects.create(name=item['category_name'].strip(),language=language)
                    category = Category.objects.create(slug=slug)
                    category.description.add(cd)
                    category.save()
                except:
                    category = None

            try:
                brand = Brand.objects.get(description__name=item['brand'])
            except Brand.DoesNotExist:
                slug = slugify(item['brand'])
                print(slug)
                print(item['brand'])
                if item['brand']:
                    brand = Brand.objects.create(slug=slug or item['brand'].lower(),country="Україна")
                    bd = BrandDescription.objects.create(name=item['brand'],language=language)
                    brand.description.add(bd)
                    brand.save()
                    print('brand created %s' % item['brand'])
                elif slug:
                    brand = Brand.objects.get(slug=slug)
                else:
                    brand = None

            if brand and item.get('country'):
                brand.country = item.get('country')
                brand.update()

        try:
            p = Product.objects.get(model=item['model'])
        except Product.DoesNotExist:
            if not only_price:
                p = Product.objects.create(
                    slug=item['slug'].replace('https://ckl.com.ua/',''),
                    model=item['model'],
                )
            else:
                p = None

        if not only_price:
            p.width = item.get('width')
            p.height = item.get('height')
            p.weight = item.get('weight')
            p.length = item.get('length')

            p.counter = item.get('counter')

        currency = list(dict(Product.currency_choices).values())
        if item['currency'] in currency:
            currency = currency.index(item['currency'])
        else:
            currency = None

        if not p:
            continue

        try:
            price = float(item['retail_price'].replace(',','.'))
        except:
            price = item['retail_price']
        print(price)
        if price:
            p.purchase_price = price
            if currency and currency != 0:
                try:
                    cur = Currency.objects.get(type=currency)
                    price = price * cur.value
                except Currency.DoesNotExist:
                    pass

            p.retail_price = price

        else:
            p.storage = 2

        # if item.get('opt_price'):
        #     p.big_opt_price = float(item.get('opt_price').replace(',','.'))
        #     if currency and currency != 0:
        #         try:
        #             cur = Currency.objects.get(type=currency)
        #             p.big_opt_price = p.big_opt_price * cur.value
        #         except Currency.DoesNotExist:
        #             pass

        is_available = item.get('is_available')
        if is_available and is_available == '+':
            p.is_available = True

        if currency:
            p.currency = currency

        p.save()

        if only_price:
            continue

        if brand:
            if brand.name == 'Frap' or brand.name == 'Gappo':
                p.category.clear()
                c = Category.objects.filter(Q(description__name__icontains=item['category_name']),Q(description__name__icontains=brand.name)).distinct().first()
                p.category.add(c)
                p.update()

            p.brand = brand
            p.save()

        try:
            pd = ProductDescription.objects.get(name=item['name'],language=language)
        except ProductDescription.DoesNotExist:
            pd = ProductDescription.objects.create(name=item['name'],language=language)

        pd.title = item.get('title')
        pd.meta_description = item.get('meta_description')
        pd.meta_keywords = item.get('meta_keywords')
        pd.text = item['text']

        try:
            pd.save()
        except IntegrityError:
            pass

        p.description.add(pd)

        if category:
            p.category.add(category)

        for image in item['image'].split(', '):
            image = save_prom_image(image)
            try:
                g = Gallery.objects.get(image=image,product=p)
            except Gallery.DoesNotExist:
                Gallery.objects.create(image=image,product=p)

def import_json(items,Model):
    items = loads(items)
    for i in items:
        description = i.get(description)
        del i['description']
        item = Model.objects.create(**i)
        for d in description:
            item.description.create(**d)

def import_model(Model):
    model = re.search(r"'.*'",Model).group().replace("'","").split('.')[-1]
    if not model in locals():
        path = '.'.join(re.search(r"'.*'",Model).group().replace("'","").split('.')[0:-1])
        exec('from %s import %s' % (path,model))

    return locals().get(model)

def many_to_manies(mm,create):
    if mm:
        for m in mm.keys():
            Model = import_model(mm[m].get('Model'))
            for i in mm[m]['items']:
                try:
                    mitem = Model.objects.create(**i)
                except IntegrityError:
                    continue
                getattr(create,m).add(mitem)

def related_objects(items):
    for item in items:
        Model = import_model(item.get('Model'))
        for i in item.get('items'):
            try:
                create = Model.objects.create(**i)
            except IntegrityError:
                continue

def load(related=None,items=None,filename=None):
    if filename:
        with open(filename,'r') as f:
            data = loads(f.read())

    if not related:
        related = data['related']

    if not items:
        items = data['data']

    for item in related.keys():
        Model = import_model(related[item].get('Model'))
        try:
            create = Model.objects.create(**related[item]['fields'])
        except IntegrityError as e:
            print(e)
            continue

        many_to_manies(related[item].get('mm'),create)

    for item in items:
        Model = import_model(item.get('Model'))
        try:
            create = Model.objects.create(**item['fields'])
        except IntegrityError as e:
            print(e)
            related_objects(item.get('related'))
            continue

        related_objects(item.get('related'))
        many_to_manies(item.get('mm'),create)