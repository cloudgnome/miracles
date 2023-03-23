from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from requests import post
from json import loads
from checkout.models import City,Departament

class Command(BaseCommand):
    help = 'Sync Beles'

    def handle(self, *args, **options):
        time = timezone.now()
        print('Поехали..')

        url = "https://api.novaposhta.ua/v2.0/json/"
        data = {
            "modelName": "Address",
            "calledMethod": "getCities",
            "methodProperties": {},
            "apiKey": "c7400a665bf9e32b62c2f748bf5bf890"
        }
        departament = {
            "modelName": "AddressGeneral",
            "calledMethod": "getWarehouses",
            "methodProperties": {
                "CityRef":"",
            },
            "apiKey": "c7400a665bf9e32b62c2f748bf5bf890"
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
            city.address = item['Description']
            city.type = 1
            city.save()

            departament['methodProperties']['CityRef'] = item['Ref']
            response = post(url,json=departament)
            departaments = loads(response.text)
            if departaments['data']:
                for dep in departaments['data']:
                    depar = Departament()
                    depar.address = dep['Description']
                    depar.number = dep['Number']
                    depar.city = city
                    depar.type = 1
                    depar.save()


        print('Потрачено времени: %s' % (timezone.now() - time))
        print('Завершено.')