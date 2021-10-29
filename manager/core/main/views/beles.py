from xlsxwriter import Workbook
from catalog.models import Product,Category,Beles_Category
from io import BytesIO
from django.http import HttpResponse
from shop.models import Percents
from catalog.views.prices import percent

def beles_prom(request):
    output = BytesIO()

    book = Workbook(output)
    products_sheet = book.add_worksheet('Export Products Sheet')
    categories_sheet = book.add_worksheet('Export Groups Sheet')

    head_format = book.add_format({
        'bg_color':'#e6e6e6',
        'locked': 1,
        'bold': 1,
    })
    products = Product.objects.extra(where=['catalog_product.id IN (select product_id from catalog_beles)']).filter(beles__load_on_prom=True)
    categories = Beles_Category.objects.all()

    row = 0
    col = 0
    categories_sheet.write(row, col, 'Номер_группы', head_format)
    categories_sheet.write(row, col + 1,'Название_группы', head_format)
    categories_sheet.write(row, col + 2,'Идентификатор_группы', head_format)
    categories_sheet.write(row, col + 3,'Номер_родителя', head_format)
    categories_sheet.write(row, col + 4,'Идентификатор_родителя', head_format)
    row += 1
    for category in categories:
        categories_sheet.write(row, col, '')
        categories_sheet.write(row, col + 1, category.name)
        categories_sheet.write(row, col + 2, category.id)
        categories_sheet.write(row, col + 3, '')
        if category.is_root_node():
            categories_sheet.write(row, col + 4, '')
        else:
            categories_sheet.write(row, col + 4, category.parent.id)
        row += 1
    row = 0
    col = 0
    products_sheet.write(row, col, 'Код_товара', head_format)
    products_sheet.write(row, col + 1, 'Идентификатор_товара', head_format)
    products_sheet.write(row, col + 2, 'Название_позиции', head_format)
    products_sheet.write(row, col + 3, 'Цена', head_format)
    products_sheet.write(row, col + 4, 'Скидка', head_format)
    products_sheet.write(row, col + 5, 'Валюта', head_format)
    products_sheet.write(row, col + 6, 'Единица_измерения', head_format)
    products_sheet.write(row, col + 7, 'Ссылка_изображения', head_format)
    products_sheet.write(row, col + 8, 'Наличие', head_format)
    products_sheet.write(row, col + 9, 'Идентификатор_группы', head_format)
    products_sheet.write(row, col + 10, 'Производитель', head_format)
    row += 1
    prom_percents = Percents.objects.get(site__domain='beles.com.ua')
    for product in products:
        price = round(percent(product.beles.purchase_price,prom_percents),2)
        products_sheet.write(row, col, product.model)
        products_sheet.write(row, col + 1, product.id)
        products_sheet.write(row, col + 2, product.name)
        products_sheet.write(row, col + 3, price)
        products_sheet.write(row, col + 4, product.prom_special())
        products_sheet.write(row, col + 5, "UAH")
        products_sheet.write(row, col + 6, "шт")
        products_sheet.write(row, col + 7, product.prom_images())
        products_sheet.write(row, col + 8, '+')
        products_sheet.write(row, col + 9, product.beles.category.id)
        if product.brand and product.brand != 'Китай':
            products_sheet.write(row, col + 10, product.brand.name)
        else:
            products_sheet.write(row, col + 10, "")
        row += 1

    book.close()

    output.seek(0)
    response = HttpResponse(output.read(),content_type="application/vnd.ms-excel")
    response['Content-Disposition'] = 'attachment; filename="pricelist.xlsx"'

    return response