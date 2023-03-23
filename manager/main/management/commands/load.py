from django.core.management.base import BaseCommand, CommandError
from beles.models import Category
from catalog.models import Category as Igroteka
from json import loads

class Command(BaseCommand):
    help = 'Load data'
    items = {}

    def handle(self, *args, **options):
        with open('/home/petrov/db/beles_category_category.json','r') as f:
            data = loads(f.read())
            for d in data:
                self.items[d['id']] = d
            for item in self.items:
                item = self.items[item]
                for value in item:
                    if item[value] == '<null>':
                        item[value] = None

                # del item['category_igrushec_id']
                # del item['setting_id']
                # item['category_id'] = item['category_igroteka_id']
                # del item['category_igroteka_id']

                # try:
                #     Image.objects.get(id=item['id'])
                # except:
                #     Image.objects.create(**item)

                # try:
                #     prom = Prom.objects.get(id=item['prom_id'])
                #     cat = Category.objects.get(id=item['category_id'])
                #     Prom_Category.objects.create(prom_category_id=item['prom_category_id'],category=cat,prom=prom)
                # except Prom.DoesNotExist:
                #     continue

                # category = Category.objects.get(id=item['beles_category_id'])
                # category.category_id = item['category_id']
                # category.save()

                product = Category.objects.get(id=item['beles_category_id'])
                category = Igroteka.objects.get(id=item['category_igroteka_id'])
                product.category.add(category)
                product.save()

    #             if 'last_modified' in item:
    #                 del item['last_modified']
    #             if 'date_added' in item and item['date_added']:
    #                 item['date_added'] = item['date_added'].replace(' +0000','')

                # del item['site_id']

                # if 'description' in item:
                #     del item['description']
                # if "description_igroteka" in item:
                #     if item['description_igroteka'] and item['description_igroteka'] != '<p><strong>':
                #         item['description'] = item["description_igroteka"]
                #     del item['description_igroteka']
                # if 'slug' in item:
                #     del item['slug']
                # if "slug_igroteka" in item:
                #     if item['slug_igroteka']:
                #         item['slug'] = item["slug_igroteka"]
                #     del item['slug_igroteka']
                # if "iname" in item:
                #     if item['iname']:
                #         item['name'] = item["iname"]
                #     del item['iname']

                # try:
                #     Item.objects.get(id=item['id'])
                # except Item.DoesNotExist:
                #     it = Item()
                #     it.cart = Cart.objects.get(id=item['cart_id'])
                #     try:
                #         it.product = Product.objects.get(id=item['product_id'])
                #     except Product.DoesNotExist:
                #         continue
                #     it.price = int(item['price'])
                #     it.qty = int(item['qty'])
                #     it.save()

                # try:
                #     Product.objects.get(id=item['id'])
                # except Product.DoesNotExist:
                #     product = Product(**item)
                #     product.update()
                # item['product'] = item['product_id']
                # del item['product_id']
                # item['url'] = item['beles_url'] 
                # del item['beles_url']
                # del item['price']

                # try:
                #     Product.objects.get(product_id=item['product_id'])
                # except Product.DoesNotExist:
                #     Product.objects.create(**item)

                # try:
                #     Gallery.objects.get(id=item['id'])
                # except:
                #     gallery = Gallery()
                #     gallery.product = Product.objects.get(id=item['product_id'])
                #     gallery.position = item['position']
                #     gallery.image = item['image']
                #     gallery.id = item['id']
                #     gallery.save()
                # try:
                #     Thumb.objects.get(id=item['id'])
                # except Thumb.DoesNotExist:
                #     try:
                #         thumb = Thumb()
                #         thumb.image = Gallery.objects.get(id=item['image_id'])
                #         thumb.size = item['size']
                #         thumb.url = item['url']
                #         thumb.save()
                #     except Gallery.DoesNotExist:
                #         pass

    # def category(self,item):
    #     for value in item:
    #         if item[value] == '<null>':
    #             item[value] = None
    #     if item['parent_id']:
    #         self.category(self.items[item['parent_id']])

    #     if 'last_modified' in item:
    #         del item['last_modified']
    #     if 'created_at' in item and item['created_at']:
    #         item['created_at'] = item['created_at'].replace(' +0000','')
    #     if 'keywords' in item:
    #         item['meta_keywords'] = item['keywords']
    #         del item['keywords']
    #     try:
    #         Beles_Category.objects.get(id=item['id'])
    #     except Beles_Category.DoesNotExist:
    #         Beles_Category.objects.create(**item)

    # def handle(self, *args, **options):
    #     with open('/home/petrov/beles_category.json','r') as f:
    #         data = loads(f.read())
    #         for d in data:
    #             self.items[d['id']] = d
    #         for item in self.items:
    #             item = self.items[item]
    #             self.category(item)