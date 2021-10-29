from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from requests import get
from json import loads
from checkout.models import City,Departament
from user.models import User

class Command(BaseCommand):
    help = 'Sync Delivery Depratments'

    def handle(self, *args, **options):
        time = timezone.now()
        print('Поехали..')

        base_url = "http://www.delivery-auto.com/"
        region_url = 'api/v4/Public/GetRegionList?culture={culture}&country=1'
        cities_url = 'api/v4/Public/GetAreasList?culture={culture}&regionId={regionId}&country=1'
        departaments_url = 'api/v4/Public/GetWarehousesList?culture={culture}&includeRegionalCenters=true&CityId={CityId}&RegionId={RegionId}&country=1'
        dep_url = 'api/v4/Public/GetWarehousesInfo?culture={culture}&WarehousesId={WarehousesId}'

        regions = loads(get(base_url + region_url.format(culture='uk-UA')).text)
        cities = loads(get(base_url + cities_url.format(culture='uk-UA',regionId=regions['data'][2]['externalId'])).text)
        regions_ru = loads(get(base_url + region_url.format(culture='ru-RU')).text)
        cities_ru = loads(get(base_url + cities_url.format(culture='ru-RU',regionId=regions_ru['data'][2]['externalId'])).text)

        for item in cities_ru['data']:
            for city in cities['data']:
                if city['id'] == item['id']:
                    city['name_ru'] = item['name']

        City.objects.filter(type=2).delete()

        print('Удалили старые отделения..')
        print('Грузим новые..')

        for item in cities['data']:
            try:
                city = City.objects.get(address_ru=item['name_ru'],address_ua=item['name'],type=2)
            except City.DoesNotExist:
                city = City.objects.create(address_ru=item['name_ru'],address_ua=item['name'],type=2)

            departaments = loads(get(base_url + departaments_url.format(culture='uk-UA',CityId=item['id'],RegionId=regions['data'][2]['externalId'])).text)
            departaments_ru = loads(get(base_url + departaments_url.format(culture='ru-RU',CityId=item['id'],RegionId=regions_ru['data'][2]['externalId'])).text)

            for dep in departaments['data']:
                address_ua = loads(get(base_url + dep_url.format(culture='uk-UA',WarehousesId=dep['id'])).text)['data']['address']
                address_ru = loads(get(base_url + dep_url.format(culture='ru-RU',WarehousesId=dep['id'])).text)['data']['address']

                try:
                    departament = Departament.objects.get(address_ru=address_ru,address_ua=address_ua,type=2,city=city)
                except Departament.DoesNotExist:
                    departament = Departament.objects.create(address_ru=address_ru,address_ua=address_ua,type=2,city=city)

        for user in User.objects.all():
            user.update_departaments = True
            user.save()

        print('Потрачено времени: %s' % (timezone.now() - time))
        print('Завершено.')