from django.core.management.base import BaseCommand, CommandError
from catalog.models import Prom_Category,Category,Prom,Product
from json import loads
import csv
from system.settings import BASE_DIR

class Command(BaseCommand):
    help = 'Load data'
    items = {}

    def handle(self, *args, **options):
        for prom in Prom.objects.all():
            if prom.full_store:
                products = Product.objects.filter(is_available=True).exclude(category=None)
            else:
                products = Product.objects.filter(storage=1,is_available=True).exclude(category=None)

            print(len(products))

            with open(BASE_DIR + '/static/proms/%s.csv' % prom.prom_id,'w') as f:
                writer = csv.writer(f,quoting=csv.QUOTE_ALL)
                writer.writerow(["Код_товара","Уникальный_идентификатор","Идентификатор_товара","Название_позиции","Цена","Скидка","Валюта","Единица_измерения","Ссылка_изображения","Наличие","Номер_группы","Производитель"])

                for product in products:
                    price = product.prom_percent_price(prom.percent)
                    try:
                        category_id = product.prom_category().proms.get(prom=prom).prom_category_id
                    except Prom_Category.DoesNotExist:
                        category_id = ''
                    except Prom_Category.MultipleObjectsReturned:
                        category_id = product.prom_category().proms.filter(prom=prom).first().prom_category_id
                    except:
                        category_id = ''

                    writer.writerow(["%s"%product.model,"","%s"%product.id,"%s"%product.names(lang='ru'),"%s"%price,"%s"%product.prom_special(),"UAH","шт","%s"%product.prom_images(),"%s"%product.prom_stock(),"%s"%category_id,"%s"%product.brand_name])