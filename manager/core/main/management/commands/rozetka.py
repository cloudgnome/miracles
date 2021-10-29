import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from catalog.models import Category, Product
from system.settings import HOME_URL

class Command(BaseCommand):
    help = 'Rozetka XML'
    items = {}

    def handle(self, *args, **options):
        y = ET.Element('yml_catalog')
        y.attrib = {'date':timezone.now().strftime('%Y-%b-%d %H:%M')}
        s = ET.SubElement(y, 'shop')
        s.text = 'Igroteka'
        c = ET.SubElement(y, 'company')
        c.text = 'ФОП Шинаков Виталий Александрович'
        u = ET.SubElement(y, 'url')
        u.text = 'http://igroteka.ua'
        cur = ET.SubElement(y, 'currencies')
        curr = ET.SubElement(cur,'currency')
        curr.attrib = {'id':"UAH", 'rate':"1"}
        categories = ET.SubElement(y,'categories')
        for category in Category.objects.filter(active=True).exclude(id=338):
            cat = ET.SubElement(categories,'category')
            cat.attrib = {'id':str(category.id)}
            if category.parent:
                cat.attrib['parentId'] = str(category.parent.id)
            cat.text = category.name

        offers = ET.SubElement(y,'offers')
        for product in Product.objects.filter(category__isnull=False,is_available=True,slug__isnull=False,storage=1):
            if not product.brand:
                continue
            offer = ET.SubElement(offers,'offer')
            offer.attrib = {'id':str(product.id), 'available':"true"}
            url = ET.SubElement(offer, 'url')
            url.text = 'http://igroteka.ua%s' % product.slug
            price = ET.SubElement(offer, 'price')
            price.text = str(product.retail_price)
            currencyId = ET.SubElement(offer, 'currencyId')
            currencyId.text = 'UAH'
            categoryId = ET.SubElement(offer, 'categoryId')
            categoryId.text = str(product.get_category().id)
            for image in product.gallery.all():
                picture = ET.SubElement(offer, 'picture')
                picture.text = "http://igroteka.ua%s" % image.image.url

            print(product.name)
            vendor = ET.SubElement(offer, 'vendor')
            vendor.text = product.brand.name
            stock_quantity = ET.SubElement(offer,'stock_quantity')
            stock_quantity.text = '100'
            name = ET.SubElement(offer, 'name')
            name.text = product.name

        tree = ET.ElementTree(y)
        tree.write(HOME_URL + 'static/rozetka.xml',encoding='utf-8', xml_declaration=True)