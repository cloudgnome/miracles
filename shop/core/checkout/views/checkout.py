from django.shortcuts import render,redirect,Http404
from django.contrib.auth import login
from checkout.forms import CheckoutForm
from user.forms import UserForm,User
from cart.views import Buyer
from django.core.exceptions import PermissionDenied
from django.views.generic import View
import pymysql.cursors
from settings import BASE_URL,PHONES
from django.utils.translation import ugettext_lazy as _
from catalog.models import Product
from django.contrib import messages
from django.http import JsonResponse
from json import loads,dumps

try:
    from settings import SMS_ACCOUNT,SMS_PASSWORD,SMS_SIGN
except:
    SMS_ACCOUNT,SMS_PASSWORD,SMS_SIGN = None,None,None

class CheckoutView(View):
    def get(self,request,*args,**kwargs):
        buyer = Buyer(request)
        cart = buyer.cart

        if not cart.items_qty:
            if request.LANGUAGE_CODE == 'ua':
                return redirect('/ua/')
            else:
                return redirect('/')

        if request.user.is_authenticated:
            user = request.user
            initial = {'name':user.name,'phone':user.phone,'email':user.email,'lname':user.lname,'sname':user.sname}
            form = CheckoutForm(initial=initial)
        else:
            form = CheckoutForm()

        context = {
            'cart':cart,
            'form':form,
            'discount':cart.discount,
            'title':_("Оформление заказа"),
            'view':'Checkout',
            'cartJson':cart.dict
        }
        return render(request, 'checkout/%s/checkout.html' % request.folder, context)

    def post(self,request,*args,**kwargs):
        buyer = Buyer(request)
        items = loads(request.body)

        for item,qty in items.items():
            if item == 'csrfmiddlewaretoken':
                continue
            try:
                buyer.add_item(item=Product.objects.get(id=item),qty=qty)
            except Product.DoesNotExist:
                continue

        cart = buyer.cart
        cart.save()

        return JsonResponse({'result':True})

class OrderView(View):
    def get(self,request,*args,**kwargs):
        return self.post(request)

    def post(self,request,*args,**kwargs):
        buyer = Buyer(request)
        cart = buyer.cart

        if not cart.items_qty:
            if request.LANGUAGE_CODE == 'ua':
                return redirect('/ua/')
            else:
                return redirect('/')

        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            data = form.cleaned_data

            order.cart = cart
            order.user,request = self.user(request,data)
            order.save()
            buyer.new()
            try:
                order.send_mail(language=request.LANGUAGE_CODE)
            except:
                pass
            try:
                OrderView.send_sms(order.phone,order.id)
            except Exception as e:
                print(e)

            messages.success(request, _('Ваш заказ успешно оформлен.'))

            if request.user.is_authenticated:
                if request.LANGUAGE_CODE == 'ua':
                    return redirect('/{}/user/order/{}'.format(request.LANGUAGE_CODE,order.id))
                else:
                    return redirect('/user/order/%s' % order.id)
            else:
                if request.LANGUAGE_CODE == 'ua':
                    return redirect('/ua/')
                else:
                    return redirect('/')

        context = {
            'cart':cart,
            'form':form,
            'title':_("Оформление заказа"),
            'view':'Checkout',
            'cartJson':cart.dict
        }
        return render(request, 'checkout/%s/checkout.html' % request.folder, context)

    def user(self,request,data):
        if request.user.is_anonymous:
            try:
                user = User.objects.get(phone=data.get('phone'))
                if user.is_admin:
                    raise PermissionDenied
            except User.DoesNotExist:
                user = {
                    'subscription':True,
                    'lname':data.get('lname') or data.get('name'),
                    'sname':data.get('sname') or data.get('name'),
                    'phone':data.get('phone'),
                    'name':data.get('name'),
                    'email':data.get('email'),
                    'notifications':True,
                    'subscription':data.get('subscription')
                }
                user['password1'] = user['password2'] = User.make_random_password()
                form = UserForm(user)

                if form.is_valid():
                    user = form.save()
                else:
                    raise Exception(form.errors)
                    return None,request

            except User.MultipleObjectsReturned:
                user = User.objects.filter(phone=data.get('phone')).first()

            user.backend = 'user.backends.ModelBackend'
            login(request, user)
        else:
            user = request.user

        if data.get('subscription'):
            user.subscription = True
            user.save()

        if not user.lname or not user.sname:
            if not user.lname:
                user.lname = data.get('lname')
            if not user.sname:
                user.sname = data.get('sname')
            user.save()

        return user,request

    def send_sms(phone,id):
        if not SMS_ACCOUNT and SMS_PASSWORD:
            return False

        try:
            connection = pymysql.connect(host='94.249.146.189',user=SMS_ACCOUNT,password=SMS_PASSWORD,db='users',charset='utf8')
        except Exception as e:
            print(e)
            return False
        try:
            with connection.cursor() as cursor:
                query = "SET NAMES utf8"
                cursor.execute(query)
                if not "38" in phone[:2]:
                    phone = '38%s' % phone

                query = """INSERT INTO {} (sign,number,message) VALUES("{}","{}","Заказ {}. Магазин {} Тел. {}; {}")""".format(SMS_ACCOUNT,SMS_SIGN,phone,id,BASE_URL,PHONES[0],PHONES[1])
                cursor.execute(query)

            connection.commit()
        except Exception as e:
            print(e)
        finally:
            connection.close()