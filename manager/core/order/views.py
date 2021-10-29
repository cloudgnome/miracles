from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse,Http404
from checkout.models import Order,Np_City,Delivery_City,Np_Departament,Delivery_Departament
from .forms import OrderForm
from cart.models import Item,Cart
from catalog.models import Product
from user.forms import UserOrderForm
from user.models import User
from django.views.generic import View
from requests import post
from json import loads
from django.utils import timezone
import pymysql.cursors
from datetime import datetime,timedelta
from django.db.models import Q
from itertools import chain
from mobile.notifications import send_notification

__all__ = ['order','search','add','remove','save','save_items','departaments','new_order','new','ttn','igrushec','sms','mass_sms','tracking','track']

def track(request,id):
    track = {
        "apiKey": "a214e867d4421c45bc9b5877f7c832c2",
        "modelName": "TrackingDocument",
        "calledMethod": "getStatusDocuments",
        "methodProperties": {
            "Documents": [
                # {
                #     "DocumentNumber": "20400048799000",
                #     "Phone":""
                # },
            ]
        }
        
    }
    order = get_object_or_404(Order,id=id)
    track['methodProperties']['Documents'].append({'DocumentNumber':order.ttn})

    response = post('https://api.novaposhta.ua/v2.0/json/',json=track)
    json = loads(response.text)
    context = {}
    if json['data']:
        item = json['data'][0]
        context[order.ttn] = {
                    'Создан':item.get('DateCreated'),
                    'Ожид. дата доставки':item.get('ScheduledDeliveryDate'),
                    'Статус':item.get('Status')
                    }
    return JsonResponse({'item':context})


def tracking(request):
    track = {
        "apiKey": "a214e867d4421c45bc9b5877f7c832c2",
        "modelName": "TrackingDocument",
        "calledMethod": "getStatusDocuments",
        "methodProperties": {
            "Documents": [
                # {
                #     "DocumentNumber": "20400048799000",
                #     "Phone":""
                # },
            ]
        }
        
    }
    orders = Order.objects.filter(created_at__gte=datetime.today() - timedelta(days=8),status=6,ttn__isnull=False)
    for order in orders:
        track['methodProperties']['Documents'].append({'DocumentNumber':order.ttn})

    response = post('https://api.novaposhta.ua/v2.0/json/',json=track)
    json = loads(response.text)
    context = {}
    if json['data']:
        for item in json['data']:
            status = item.get('StatusCode')
            if status == '7' or status == '8':
                date = datetime.strptime('10:00 '+item.get('ScheduledDeliveryDate').replace('-','.'),'%H:%M %d.%m.%Y')
                if date < datetime.today() - timedelta(2):
                    ttn = item.get('Number')
                    order = orders.get(ttn=ttn)
                    context[ttn] = {
                                'Создан':item.get('DateCreated'),
                                'Телефон':order.user.phone,
                                'Имя':order.user.name,
                                'Ожид. дата доставки':item.get('ScheduledDeliveryDate'),
                                'Город':item.get('CityRecipient'),
                                'Отделение':Np_Departament.objects.get(id=order.departament).address
                                }
    if context:
        return JsonResponse({'items':context})
    else:
        return JsonResponse({'items':''})

templates = {
            'ttn':"""Посылка новой почты 
№ %s""",
            'payment':"""р/с приватбанка 26002052105969 мфо 351533 окпо 2604814519 Шинаков О.В. 
%s грн.""",
            'card':"""5218 5722 2069 6830 Шинаков Виталий Александрович 
%s грн.""",
            'order':"""Заказ %s igroteka.ua (096)443-47-58"""
            }





def mass_sms(request):
    orders = Order.objects.filter(status=8)
    if orders:
        connection = pymysql.connect(host='94.249.146.189',user='igroteka',password='JB8-GMT-ELg-dzE',db='users',charset='utf8')
        try:
            with connection.cursor() as cursor:
                query = "SET NAMES utf8"
                cursor.execute(query)
                for order in orders:
                    data = order.ttn
                    phone = order.user.phone
                    if not "38" in phone[:2]:
                        phone = '38%s' % phone
                    query = """INSERT INTO igroteka (sign,number,message) VALUES("Igroteka","{}","{}")""".format(phone,templates.get('ttn') % data)
                    cursor.execute(query)
                    order.status = 6
                    order.save()

                connection.commit()
        finally:
            connection.close()
        return JsonResponse({'result':True})
    else:
        return JsonResponse({'errors':'Не найдены заказы'})

def sms(request,id,type,summ = None):
    order = get_object_or_404(Order,id=id)
    phone = order.user.phone
    if not "38" in phone[:2]:
        phone = '38%s' % phone
    if type == 'ttn':
        if not order.ttn:
            raise Http404()
        data = order.ttn
    elif summ:
        data = summ
    else:
        data = order.cart.total
    connection = pymysql.connect(host='94.249.146.189',user='igroteka',password='JB8-GMT-ELg-dzE',db='users',charset='utf8')
    try:
        with connection.cursor() as cursor:
            query = "SET NAMES utf8"
            cursor.execute(query)
            query = """INSERT INTO igroteka (sign,number,message) VALUES("Igroteka","{}","{}")""".format(phone,templates.get(type) % data)
            cursor.execute(query)

        connection.commit()
        if type == 'ttn':
            order.status = 6
            order.save()
    finally:
        connection.close()
    return JsonResponse({'result':True})

def igrushec(request):
    orders = Order.objects.using('igrushec').filter(status=1)
    if orders:
        return JsonResponse({'count':len(orders)})
    else:
        return JsonResponse({'count':0})

def ttn(request):
    data = {
        "apiKey": "a214e867d4421c45bc9b5877f7c832c2",
        "modelName": "InternetDocument",
        "calledMethod": "save",
        "methodProperties": {
            "AfterpaymentOnGoodsCost": "",
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
            "Sender": "2dbf2545-9f9c-11e8-8b24-005056881c6b",
            "SenderAddress": "7b422fbb-e1b8-11e3-8c4a-0050568002cf",
            "ContactSender": "96bbda2c-a122-11e8-8b24-005056881c6b",
            "SendersPhone": "380964434758",
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
        },
    }
    delivery = {
       "modelName": "InternetDocument",
       "calledMethod": "getDocumentPrice",
       "methodProperties": {
          "Sender":"2dbf2545-9f9c-11e8-8b24-005056881c6b",
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
       },
       "apiKey": "a214e867d4421c45bc9b5877f7c832c2"
    }
    city_ref = {
        "apiKey": "a214e867d4421c45bc9b5877f7c832c2",
        "modelName": "Address",
        "calledMethod": "searchSettlements",
        "methodProperties": {
            "CityName": "Черняхов",
            "Limit": 5
        }
    }
    city = get_object_or_404(Np_City,id=request.POST.get('order-city'))
    departament = get_object_or_404(Np_Departament,id=request.POST.get('order-departament'))

    city_ref['methodProperties']['CityName'] = city.address
    response = post('https://api.novaposhta.ua/v2.0/json/',json=city_ref)
    response = loads(response.text)

    if not response['data'] and response['errors']:
        return JsonResponse({'errors':response['errors']})

    if request.POST.get('order-payment_type') == '1':
        delivery['methodProperties']['PayerType'] = 'Sender'
        delivery['methodProperties']['PaymentMethod'] = 'NonCash'
        # data['methodProperties']["BackwardDeliveryData"] = [
        #     {
        #         "PayerType": "Recipient",
        #         "CargoType": "Money", 
        #         "RedeliveryString": request.POST.get('total')
        #     }
        # ]

    delivery['methodProperties']['CityRecipient'] = response['data'][0]['Addresses'][0]['Ref']
    delivery['methodProperties']['SeatsAmount'] = request.POST.get('seats')
    delivery['methodProperties']['Weight'] = request.POST.get('weight')
    delivery['methodProperties']['Cost'] = request.POST.get('total')
    delivery['methodProperties']['RecipientAddressName'] = departament.number
    delivery['methodProperties']['VolumeGeneral'] = (float(request.POST.get('volume')) * 4000) / 1000000
    response = post('https://api.novaposhta.ua/v2.0/json/',json=delivery)
    response = loads(response.text)
    if response['data']:
        cost = response['data'][0]['Cost']
    elif response['errors']:
        return JsonResponse({'errors':response['errors']})

    data['methodProperties']['RecipientsPhone'] = '38'+request.POST.get('user-phone')
    data['methodProperties']['RecipientName'] = request.POST.get('user-name')
    data['methodProperties']['RecipientCityName'] = city.address
    data['methodProperties']['RecipientAddressName'] = departament.number
    data['methodProperties']['Cost'] = request.POST.get('total')
    data['methodProperties']['SeatsAmount'] = request.POST.get('seats')
    data['methodProperties']['Weight'] = request.POST.get('weight')
    data['methodProperties']['VolumeGeneral'] = delivery['methodProperties']['VolumeGeneral']
    date = request.POST.get('date').replace('-','.').split('.')[::-1]
    data['methodProperties']['DateTime'] = ".".join(date)

    if request.POST.get('order-payment_type') == '1':
        data['methodProperties']['PayerType'] = 'Sender'
        data['methodProperties']['PaymentMethod'] = 'NonCash'
        data['methodProperties']['AfterpaymentOnGoodsCost'] = ((float(cost) + int(request.POST.get('total'))) * 1.02) + 25
        # data['methodProperties']["BackwardDeliveryData"] = [
        #     {
        #         "PayerType": "Recipient",
        #         "CargoType": "Money", 
        #         "RedeliveryString": request.POST.get('total')
        #     }
        # ]

    order = Order.objects.get(id=request.POST.get('item-id'))
    if len(order.items()) <= 2:
        data['methodProperties']['AdditionalInformation'] = ""
        for item in order.items():
            if item.qty > 1:
                data['methodProperties']['AdditionalInformation'] += "%s %sшт. " % (item.product.name, item.qty)
            else:
                data['methodProperties']['AdditionalInformation'] += "%s " % item.product.name
    else:
        data['methodProperties']['AdditionalInformation'] = "Заказ %s" % order.id

    data['methodProperties']['AdditionalInformation'] = data['methodProperties']['AdditionalInformation'][:100]

    response = post('https://api.novaposhta.ua/v2.0/json/',json=data)
    json = loads(response.text)
    if json['data'] and json['data'][0]['Ref']:
        order.link = "https://my.novaposhta.ua/orders/printDocument/orders[]/%s/type/html/apiKey/a214e867d4421c45bc9b5877f7c832c2" % json['data'][0]['Ref']
        order.ttn = json['data'][0]['IntDocNumber']
        order.status = 8
        order.ttn_created_date = timezone.now()
        order.save()
        send_notification('Заказ успешно отправлен','Ваш номер ТТН: %s' % order.ttn,[order.user],order.id)
        return JsonResponse({'ref':json['data'][0]['Ref']})
    else:
        return JsonResponse({'errors':json['errors']})

def new(request):
    form = OrderForm(request.POST,prefix='order')
    user = UserOrderForm(request.POST,prefix='user')
    if form.is_valid() and user.is_valid():
        user = user.save(commit=False)
        user.save()
        cart = Cart()
        cart.session_id = request.session.session_key
        cart.save()
        order = form.save(commit=False)
        order.user = user
        order.cart = cart
        order.save()
        return JsonResponse({'result':True,'href':'/order/edit/%s' % order.id,'item_id':order.id})
    else:
        return JsonResponse({'errors':form.errors})

def new_order(request):
    context = {}
    context['form'] = OrderForm()
    context['view'] = 'order'
    context['user'] = UserOrderForm()
    context['js'] = 'order'
    context['model'] = 'order'

    return render(request,'order.html',context)

def departaments(request,t,model, city_id = None):
    model = eval(t.capitalize() + '_' + model.capitalize())
    if city_id:
        departaments = {dep.id:dep.address for dep in model.objects.filter(city_id=city_id)}
    else:
        departaments = {dep.id:dep.address for dep in model.objects.all()}
    return JsonResponse(departaments)

def save(request,id):
    order = Order.objects.get(id=id)
    user = UserOrderForm(request.POST,prefix="user",instance=order.user)
    order = OrderForm(request.POST,prefix="order",instance=order)

    if user.is_valid():
        user.save()
    else:
        return JsonResponse({'errors':user.errors,'non-field':user.non_field_errors()})

    if order.is_valid():
        order.save()
    else:
        return JsonResponse({'errors':order.errors,'non-field':order.non_field_errors()})

    return JsonResponse({'result':True})

def save_items(request,id):
    data = loads(request.body.decode('utf-8'))
    items = data['items']
    order = Order.objects.get(id=id)

    cart = order.cart
    cart.discount = 0
    total = 0
    discount = 0
    for item_id in items:
        item = Item.objects.get(id=item_id)
        item.qty = int(items[item_id]['qty'])
        if total >= 2000 and items[item_id]['price'] == item.price:
            item.price = item.product.big_opt_price
        else:
            item.price = int(items[item_id]['price'])
        item.save()
        total += item.total
        discount += item.product.retail_price * item.qty
    cart.total = total
    if discount > total:
        discount = discount - total
    else:
        discount = 0
    cart.discount = discount
    cart.save()

    data['result'] = True
    data['total'] = cart.total
    data['discount'] = cart.discount

    return JsonResponse(data)

def order(request,id):
    try:
        order = Order.objects.get(id=id)
    except Order.DoesNotExist:
        return redirect('/order/list')
    form = OrderForm(initial=order.__dict__,instance=order)
    user = UserOrderForm(instance=order.user)
    date = str(timezone.now().date())
    return render(request,'order.html',{'date':date,'js':'order','view':'order','order':order,'form':form,'user':user})

def search(request,query):
    product = Product.objects.filter(Q(model=query)).values('id','name','model')
    products =  Product.objects.filter(Q(name__icontains=query) | Q(model__icontains=query)).values('id','name','model')
    if product.first():
        products = products.exclude(model=product.first()['model'])
    products = chain(product,products[:7])
    return render(request,'order/search.html',{'products':products})

def remove(request,id):
    item = get_object_or_404(Item,id=id)
    cart = item.cart
    cart.remove_item(item)
    item.delete()
    cart.calculate_total()
    return JsonResponse({'total':cart.total,'discount':cart.discount})

def add(request,product_id,order_id):
    product = get_object_or_404(Product,id=product_id)
    order = get_object_or_404(Order,id=order_id)
    cart = order.cart
    try:
        item = Item.objects.get(cart=cart,product=product)
        item.qty += 1
        item.save()
        cart.calculate_total()
        return JsonResponse({'total':item.total,'id':item.id,'cart_total':cart.total,'discount':cart.discount,'qty':item.qty,'price':item.price})
    except Item.DoesNotExist:
        item = Item.objects.create(cart=cart,product=product,qty=1,price=product.price)
        cart.add_item(item)
        cart.calculate_total()
        return JsonResponse({'price':product.price,'id':item.id,'total':item.total,'name':product.name,'storage':product.get_storage_display(),'cart_total':cart.total,'discount':cart.discount,'slug':product.slug})