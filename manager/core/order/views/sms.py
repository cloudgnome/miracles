import pymysql.cursors
from checkout.models import Order
from django.http import JsonResponse,Http404
from django.shortcuts import get_object_or_404
from shop.models import Sms
import re

try:
    from settings import SMS_ACCOUNT,SMS_PASSWORD,SMS_SIGN
except:
    SMS_ACCOUNT = SMS_PASSWORD = SMS_SIGN = None

def send_sms(phone,text):
    if not SMS_ACCOUNT or not SMS_PASSWORD or not SMS_SIGN:
        raise Http404('Укажите настройки СМС')

    connection = pymysql.connect(host='94.249.146.189',user=SMS_ACCOUNT,password=SMS_PASSWORD,db='users',charset='utf8')

    try:
        with connection.cursor() as cursor:
            query = "SET NAMES utf8"
            cursor.execute(query)
            query = """INSERT INTO {SMS_ACCOUNT} (sign,number,message) VALUES("{SMS_SIGN}","{phone}","{text}")""".format(**dict(globals()),**dict(locals()))
            cursor.execute(query)

        connection.commit()
    finally:
        connection.close()

def prepend_phone(phone):
    if not re.match(r'380[0-9]+',phone) and re.match(r'0[0-9]+',phone):
        phone = '38%s' % phone

    return phone

def sms(request,id,type):
    order = get_object_or_404(Order,id=id)
    phone = order.phone

    if type == 'ttn' and not order.ttn:
        raise Http404()

    send_sms(prepend_phone(phone),Sms.objects.get(type=type).text.format(order=order))

    if type == 'ttn':
        order.status = 6
        order.save()

    return JsonResponse({'result':True})

def mass_sms(request,type):
    orders = Order.objects.filter(status=8)
    if orders:
        for order in orders:
            send_sms(prepend_phone(order.phone),Sms.objects.get(type=type).text.format(order=order))
        return JsonResponse({'result':True})
    else:
        return JsonResponse({'errors':'Не найдены заказы'})