from django.core.management.base import BaseCommand, CommandError
from main.models import GoogleFeed
from system.settings import BASE_DIR,DOMAIN
from bs4 import BeautifulSoup

text = '{model}\t{title}\t{description}\t{link}\t{image_link}\t{availability}\t{price}\t{brand}\t{category}'

class Command(BaseCommand):
    help = 'Google CSV'

    def handle(self, *args, **options):
        DOMAIN = 'https://igroteka.ua/'
        DOMAIN_IMAGE = 'https://igroteka.ua'
        with open(BASE_DIR + '/static/google_feed.txt','w') as f:
            f.write('id\ttitle\tdescription\tlink\timage_link\tavailability\tprice\tbrand\tgoogle product category')
            f.write('\n')
            for item in GoogleFeed.objects.all():
                product = item.product
                description = product.description.filter(language__code='ru').first().text
                if description:
                    description = BeautifulSoup(description, "html.parser").text.replace('\n','').replace('\t','')[:5000]

                f.write(text.format(model=product.model,title=product.names(lang='ru'),description=description,link=DOMAIN + product.slug,image_link=DOMAIN_IMAGE + product.image.large_thumb,availability=product.google_availability,price=str(product.price) + ' UAH',brand=product.brand.name.strip(),category=product.category_name()))
                f.write('\n')