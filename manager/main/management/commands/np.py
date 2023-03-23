from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from requests import post
from json import loads
from checkout.models import City,Departament
from user.models import User
from shop.models import Settings

class Command(BaseCommand):
    help = 'Sync Np Depratments'

    def handle(self, *args, **options):
        settings = Settings.objects.first()
        time = timezone.now()
        print('Поехали..')

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

        Departament.objects.filter(type=1).delete()
        City.objects.filter(type=1).delete()

        print('Удалили старые отделения..')
        print('Грузим новые..')

        for item in json['data']:
            city = City()
            city.id = item['CityID']
            city.address_ua = item['Description']
            city.address_ru = item['DescriptionRu']
            city.type = 1
            city.save()

            departament['methodProperties']['CityRef'] = item['Ref']
            response = post(url,json=departament)
            departaments = loads(response.text)
            if departaments['data']:
                for dep in departaments['data']:
                    depar = Departament()
                    depar.address_ua = dep['Description']
                    depar.address_ru = dep['DescriptionRu']
                    depar.number = dep['Number']
                    depar.city = city
                    depar.type = 1
                    depar.save()

        for user in User.objects.all():
            user.update_departaments = True
            user.save()

        print('Потрачено времени: %s' % (timezone.now() - time))
        print('Завершено.')