from django.core.management.base import BaseCommand, CommandError
from xlsxwriter import Workbook
from catalog.models import Product,Category
from io import BytesIO
from settings import BASE_URL,STATIC_ROOT
import os

class Command(BaseCommand):
    help = ''

    def generate_pricelist(**options):
        output = BytesIO()

        book = Workbook(output)
        sheet = book.add_worksheet()

        row = 0
        col = 0
        merge_format = book.add_format({
            'align':'center',
            'valign':'vcenter',
            'bold': 1,
        })
        url_format = book.add_format({
            'font_color': 'blue',
            'underline':  1
        })
        user = options['user'][0] if options.get('user') else None

        if options.get('filters'):
            filters = options.get('filters')
            for product in Product.objects.filter(**filters):
                sheet.write(row, col, product.model)
                # sheet.write(row, col + 1, product.name)
                sheet.write_url(row, col + 1, "http://%s/%s" % (BASE_URL,product.slug), url_format, product.names(lang='ru'))
                sheet.write(row, col + 2, product.big_opt_price)
                row += 1
        else:
            for cat in Category.objects.filter(active=True):
                if cat.is_leaf_node():
                    sheet.merge_range(row,col,row,2,cat.names(lang='ru'),merge_format)
                    sheet.write(row, col, cat.names(lang='ru'))
                    row +=1
                    if not user:
                        products = Product.objects.filter(category=cat,is_available=True)
                    else:
                        products = Product.objects.filter(category=cat,is_available=True,storage=1)

                    for product in products:
                        sheet.write(row, col, product.model)
                        # sheet.write(row, col + 1, product.name)
                        sheet.write_url(row, col + 1, "http://%s/%s" % (BASE_URL,product.slug), url_format, product.names(lang='ru'))
                        if not user:
                            sheet.write(row, col + 2, product.retail_price)
                        else:
                            sheet.write(row, col + 2, product.big_opt_price)
                        row += 1

        book.close()

        output.seek(0)
        if options.get('name'):
            path = STATIC_ROOT + options.get('name') + '.xlsx'
        else:
            path = 'static/pricelist_opt.xlsx' if user else 'static/pricelist.xlsx'
        with open(path,'wb') as f:
            f.write(output.read())
        print('Завершено.')

    def add_arguments(self, parser):
        parser.add_argument('--user', nargs='+', type=str)

    def handle(self, *args, **options):
        Command.generate_pricelist(**options)