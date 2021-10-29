from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from checkout.models import Order,City,Departament,Seat
from main.forms import SeatForm
from json import loads
from requests import post,get
from django.utils import timezone
from shop.models import Settings
from settings import PHONES
import re

VOLUME_MAX = 70

try:
    from settings import AOC
except:
    AOC = False

def ttn(request):
    request_data = loads(request.body)
    settings = Settings.objects.first()

    data = {
        "apiKey": settings.api_key,
        "modelName": "InternetDocument",
        "calledMethod": "save",
        "methodProperties": {
            "NewAddress": "1",
            "PayerType": "Recipient",
            "PaymentMethod": "Cash",
            "CargoType": "Cargo",
            "VolumeGeneral": "0.1",
            "Weight": "10",
            "ServiceType": "WarehouseWarehouse",
            "SeatsAmount": "1",
            "Description": "ТНП",
            "Cost": "500",
            "CitySender": "db5c88e0-391c-11dd-90d9-001a92567626",
            "Sender": settings.senderRef,
            "SenderAddress": "7b422fbb-e1b8-11e3-8c4a-0050568002cf",
            "ContactSender": settings.contactsRef,
            "SendersPhone": settings.phone,
            "RecipientCityName": "Киев",
            "RecipientArea": "",
            "RecipientAreaRegions": "",
            "RecipientAddressName": "1",
            "RecipientHouse": "",
            "RecipientFlat": "",
            "RecipientName": "Тест Тест Тест",
            "RecipientType": "PrivatePerson",
            "RecipientsPhone": "380991234567",
            "DateTime": "",
            "AdditionalInformation":"",
            "OptionsSeat": []
        },
    }
    if AOC:
        data["AfterpaymentOnGoodsCost"] = ""

    delivery = {
       "modelName": "InternetDocument",
       "calledMethod": "getDocumentPrice",
       "methodProperties": {
          "Sender":settings.senderRef,
          "CitySender": "db5c88e0-391c-11dd-90d9-001a92567626",
          "CityRecipient": "db5c88e0-391c-11dd-90d9-001a92567626",
          "Weight": "10",
          "ServiceType": "WarehouseWarehouse",
          "Cost": "100",
          "CargoType": "Cargo",
          "SeatsAmount": "10",
          "PayerType":"Recipient",
          "PaymentMethod": "Cash",
          "VolumeGeneral":"",
          "OptionsSeat": []
       },
       "apiKey": settings.api_key
    }

    city_ref = {
        "apiKey": settings.api_key,
        "modelName": "Address",
        "calledMethod": "searchSettlements",
        "methodProperties": {
            "CityName": "Черняхов",
            "Limit": 5
        }
    }
    order = Order.objects.get(id=request_data['order'].get('item-id'))
    city = get_object_or_404(City,type=1,id=request_data['order'].get('city'))
    departament = get_object_or_404(Departament,type=1,id=request_data['order'].get('departament'))

    # if order.SpecialCargo:
    #     data['methodProperties']['SpecialCargo'] = "1"
    #     delivery['methodProperties']['SpecialCargo'] = "1"

    Weight = 0

    for seat_data in request_data['seats']:
        volHght = seat_data.get('volumetricHeight')
        volWdth = seat_data.get('volumetricWidth')
        volLnth = seat_data.get('volumetricLength')

        try:
            seat = Seat.objects.get(
                order=order,
                cost=seat_data.get('cost'),
                weight=seat_data.get('weight'),
                volumetricHeight=volHght,
                volumetricWidth=volWdth,
                volumetricLength=volLnth
            )
            form = SeatForm(seat_data,instance=seat)
        except Seat.DoesNotExist:
            form = SeatForm(seat_data)

        if form.is_valid():
            seat = form.save(commit=False)
            seat.order = order
            seat.save()
        else:
            return JsonResponse({'result':False,'errors':form.errors})

        Volume = (int(volHght) * int(volWdth) * int(volLnth)) / 4000

        Weight += seat.weight
        seat = seat.dict()

        # if Volume > 30:
        #     del seat['specialCargo']
        #     data['methodProperties']['CargoType'] = 'Pallet'
        #     delivery['methodProperties']['CargoType'] = 'Pallet'

        #     seat["volumetricVolume"] = Volume

        if Volume > 2 and (True in [(lambda x: int(x))(x) > VOLUME_MAX for x in [volLnth,volWdth,volHght]]):
            data['methodProperties']['OptionsSeat'].append(seat)
            delivery['methodProperties']['OptionsSeat'].append(seat)

    try:
        city_ref['methodProperties']['CityName'] = city.address_ru
        response = post('https://api.novaposhta.ua/v2.0/json/',json=city_ref)
        response = loads(response.text)
        if not response['data'] and response['errors']:
            return JsonResponse({'type':'city','errors':response['errors']})
        delivery['methodProperties']['CityRecipient'] = response['data'][0]['Addresses'][0]['Ref']
    except IndexError:
        city_ref['methodProperties']['CityName'] = city.address_ua
        response = post('https://api.novaposhta.ua/v2.0/json/',json=city_ref)
        response = loads(response.text)
        if not response['data'] and response['errors']:
            return JsonResponse({'type':'city','errors':response['errors']})
        delivery['methodProperties']['CityRecipient'] = response['data'][0]['Addresses'][0]['Ref']

    if request_data['order'].get('payment_type') == '1':
        delivery['methodProperties']['PayerType'] = 'Recipient'
        delivery['methodProperties']['PaymentMethod'] = 'Cash'
        if not AOC:
            data['methodProperties']["BackwardDeliveryData"] = [
                {
                    "PayerType": "Recipient",
                    "CargoType": "Money", 
                    "RedeliveryString": request_data.get('total')
                }
            ]

    delivery['methodProperties']['SeatsAmount'] = len(request_data.get('seats')) or request_data['ttn'].get('seats')
    delivery['methodProperties']['Weight'] = Weight or request_data['ttn'].get('weight')
    delivery['methodProperties']['Cost'] = request_data.get('total')
    delivery['methodProperties']['RecipientAddressName'] = departament.number
    delivery['methodProperties']['VolumeGeneral'] = (float(request_data['ttn'].get('volume')) * 4000) / 1000000
    response = post('https://api.novaposhta.ua/v2.0/json/',json=delivery)
    response = loads(response.text)
    if response['data']:
        cost = response['data'][0]['Cost']
    elif response['errors']:
        return JsonResponse({'result':False,'type':'delivery_request','errors':response['errors']})

    phone = request_data['order'].get('phone')
    if not "38" in phone[:2]:
        phone = '38%s' % phone

    data['methodProperties']['RecipientsPhone'] = phone

    data['methodProperties']['RecipientName'] = "%s %s %s" % (request_data['order'].get('name'),request_data['order'].get('lname'),request_data['order'].get('sname') or '')
    data['methodProperties']['RecipientCityName'] = city.address_ua
    data['methodProperties']['RecipientAddressName'] = departament.number
    data['methodProperties']['Cost'] = request_data.get('total')
    data['methodProperties']['SeatsAmount'] = len(request_data.get('seats')) or request_data['ttn'].get('seats')
    data['methodProperties']['Weight'] = Weight or request_data['ttn'].get('weight')
    data['methodProperties']['VolumeGeneral'] = delivery['methodProperties']['VolumeGeneral']
    date = request_data['ttn'].get('date').replace('-','.').split('.')[::-1]
    data['methodProperties']['DateTime'] = ".".join(date)

    if request_data['order'].get('payment_type') == '1':
        data['methodProperties']['PayerType'] = 'Recipient'
        data['methodProperties']['PaymentMethod'] = 'Cash'
        if AOC:
            data['methodProperties']['AfterpaymentOnGoodsCost'] = (int(request_data.get('total')) * 1.03) + 20
        else:
            data['methodProperties']["BackwardDeliveryData"] = [
                {
                    "PayerType": "Recipient",
                    "CargoType": "Money",
                    "RedeliveryString": request_data.get('total')
                }
            ]

    if len(order.items()) <= 2:
        data['methodProperties']['AdditionalInformation'] = ""
        for item in order.items():
            if item.qty > 1:
                data['methodProperties']['AdditionalInformation'] += "%s %sшт. " % (item.product.names(lang='ru'), item.qty)
            else:
                data['methodProperties']['AdditionalInformation'] += "%s " % item.product.names(lang='ru')
    else:
        data['methodProperties']['AdditionalInformation'] = "Заказ %s" % order.id

    data['methodProperties']['AdditionalInformation'] = data['methodProperties']['AdditionalInformation'][:100]

    response = post('https://api.novaposhta.ua/v2.0/json/',json=data)
    json = loads(response.text)
    if json['data'] and json['data'][0]['Ref']:
        order.link = "https://my.novaposhta.ua/orders/printDocument/orders[]/%s/type/html/apiKey/%s" % (json['data'][0]['Ref'],settings.api_key)
        order.ttn = json['data'][0]['IntDocNumber']
        order.status = 8
        order.ttn_created_date = timezone.now()
        order.save()
        return JsonResponse({'ref':json['data'][0]['Ref']})
    else:
        return JsonResponse({'type':'ttn','errors':json['errors'],'data':data})