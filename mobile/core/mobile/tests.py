from django.test import TestCase
from requests import session,get,post
from json import loads
from datetime import datetime
from base64 import b64encode
from json import dumps

base_url = 'http://m.igroteka.ua'
s = session()
def parse(response):
    try:
        response = loads(response.text)
        return response.get('data')
    except:
        log(response.text)

def log(text):
    with open('/home/core/shop/igroteka.ua/static/test.html','w') as f:
        f.write(text)

def GET(url,headers={}):
    print('\n' + url)
    response = s.get(base_url + url,headers=headers)
    log(response.text+url)

    return response

def POST(url,json,headers):
    print('\n' + url)
    response = s.post(base_url + url,json=json,headers=headers)
    log(response.text+url)

    return response

headers = {}
def signup():
    # response = GET('/signup')
    # data = parse(response)
    # print(data)
    global headers
    # headers = {'X-CSRFToken':data.get('csrf_token')}
    signup = {'device_token':'41166ec9cca746b0b984ee3ca61e470aff'}

    response = POST('/signup',json=signup,headers=headers)
    data = parse(response)
    headers = {'X-CSRFToken':data.get('csrf_token')}

    print(data)
    print(headers)

def home():
    response = GET('/')
    data = parse(response)
    print(data)

def category():
    response = GET('/category/26')
    data = parse(response)
    print(data)

def create_order():
    order = {'email':'icloudgnome@gmail.com','subscription':'on','phone':'0944409046',
            'name':'vasya','lname':'vetrov','sname':'pizdec','payment_type':1,
            'delivery_type':1,'city':1,'departament':1,'cart':{"1276": 1, "1036": 4}}
    response = POST('/checkout',json=order,headers=headers)
    data = parse(response)
    print(data)

def orders():
    response = GET('/orders')
    data = parse(response)
    print(data)

def order():
    response = GET('/order/8')
    data = parse(response)
    print(data)

def change_order():
    order = {'payment_type':2,'cart':{"37081": 8, "37082": 14}}
    response = POST('/order/8',json=order,headers=headers)
    data = parse(response)
    print(data)

def departamens():
    response = GET('/departaments')
    data = parse(response)
    print(data)

signup()
home()
category()
# orders()
# change_order()
departamens()