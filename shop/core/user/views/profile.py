from django.views.generic import View
from checkout.models import Order
from checkout.forms import CheckoutForm
from user.forms import UserForm
from django.shortcuts import render
from django.http import JsonResponse,Http404
from django.utils import timezone
from django.utils.translation import LANGUAGE_SESSION_KEY
from django.utils.translation import ugettext_lazy as _
from base64 import b64encode,b64decode
from json import loads,dumps
from hashlib import sha1
from settings import LIQPAY_PUBLIC,LIQPAY_PRIVATE,DOMAIN
from django.views.decorators.csrf import csrf_exempt
import hmac
from ast import literal_eval
from shop.models import Language,Settings

try:
    from settings import CHECKOUT_TYPE
except:
    CHECKOUT_TYPE = 'liqpay'

__all__ = ['OrderView','ProfileView','lang','pay_callback']

@csrf_exempt
def pay_callback(request):
    with open('pay.txt','wb') as f:
        f.write(request.body)

    if CHECKOUT_TYPE == 'wfp':
        post = loads(list(request.POST.keys())[0])
        try:
            order = Order.objects.get(id=post.get('orderReference'),cart__total=post.get('amount'))
        except Order.DoesNotExist:
            raise Http404('Order not found')

        signature = '{merchantAccount};{orderReference};{amount};{currency};{authCode};{cardPan};{transactionStatus};{reasonCode}'
        signature = signature.format(**{
            'merchantAccount':'ckl_com_ua',
            'orderReference':post.get('orderReference'),
            'amount':post.get('amount'),
            'currency':'UAH',
            'authCode':post.get('authCode'),
            'cardPan':post.get('cardPan'),
            'transactionStatus':post.get('transactionStatus'),
            'reasonCode':post.get('reasonCode')
        })

        signature = hmac.new('bd15e8bcca4c6f11de6bd792edbaa9b6a71fa867'.encode('utf8'),signature.encode('utf8'),'MD5').hexdigest()
        if signature != post.get('merchantSignature'):
            raise Http404('Invalid signature')

        if post.get('transactionStatus') == 'Approved' and post.get('reason') == 'Ok' and post.get('reasonCode') == 1100:
            order.status = 11
            order.save()

            date = int(timezone.now().timestamp())

            signature = '{orderReference};{status};{time}'
            signature.format(**{
                "orderReference":order.id,
                "status":"accept",
                "time":date,
            })
            signature = hmac.new('bd15e8bcca4c6f11de6bd792edbaa9b6a71fa867'.encode('utf8'),signature.encode('utf8'),'MD5').hexdigest()

            success = {
                "orderReference":order.id,
                "status":"accept",
                "time":date,
                "signature":signature
            }

            return JsonResponse(success)

    if CHECKOUT_TYPE == 'liqpay':
        data = request.POST.get('data')
        signature = request.POST.get('signature')

        if signature == b64encode(sha1((LIQPAY_PRIVATE + data + LIQPAY_PRIVATE).encode()).digest()).decode('utf8'):
            data = loads(b64decode(data).decode('utf8'))
            if data['action'] == 'pay' and data['status'] == 'success':
                order = Order.objects.get(id=data['order_id'].replace('order_id_',''))
                order.status = 11
                order.save()

        return JsonResponse({})

def lang(request):
    request.session[LANGUAGE_SESSION_KEY] = request.GET.get('lang') or 'ru'
    request.session['lang'] = request.GET.get('lang') or 'ru'

    return JsonResponse({'result':True})

class OrderView(View):
    def liqpay(self,order):
        public_key = LIQPAY_PUBLIC
        private_key = LIQPAY_PRIVATE
        params = {
            'public_key':public_key,
            'private_key':private_key,
            "action": "pay",
            "amount":order.cart.total,
            "currency":"UAH",
            "description":"Оплата заказа №%s %s" % (order.id,DOMAIN),
            "order_id":"order_id_%s" % order.id,
            "version":3,
            "server_url":'https://%s/user/pay/callback' % DOMAIN
        }
        data = b64encode(dumps(params).encode('utf8'))
        signature = b64encode(sha1((private_key + data.decode('utf8') + private_key).encode()).digest())

        return data.decode('utf8'),signature.decode('utf8')

    def wfp(self,order):
        date = int(order.created_at.timestamp())
        signature = '{merchantAccount};{merchantDomainName};{orderReference};{orderDate};{amount};{currency};{productName};{productCount};{productPrice}'
        signature = signature.format(**{
                'merchantAccount':'ckl_com_ua',
                'merchantDomainName':'ckl.com.ua',
                'orderReference':order.id,
                'orderDate':date,
                'amount':order.cart.total,
                'currency':'UAH',
                'productName':'Заказ №%s' % order.id,
                'productCount':'1',
                'productPrice':order.cart.total,
            })

        signature = hmac.new('bd15e8bcca4c6f11de6bd792edbaa9b6a71fa867'.encode('utf8'),signature.encode('utf8'),'MD5').hexdigest()

        return date.encode('utf8'),signature.encode('utf8')

    def get(self,request,*args,**kwargs):
        shop_settings = Settings.objects.values('google_conversion').first()

        context = {
            'view':'Profile'
        }

        try:
            if request.user.is_admin:
                order = Order.objects.get(id=kwargs['id'])
            else:
                order = Order.objects.get(id=kwargs['id'],user=request.user)

            if order.status == 1 and order.payment_type == 2:
                if CHECKOUT_TYPE == 'wfp':
                    context['data'],context['signature'] = self.wfp(order)
                else:
                    context['data'],context['signature'] = self.liqpay(order)

            context['title'] = 'Заказ №%s' % order.id
            context['form'] = CheckoutForm(initial=order.__dict__)
            context['order'] = order
            context['CHECKOUT_TYPE'] = CHECKOUT_TYPE
            context['GOOGLE_CONVERSION'] = shop_settings.get('google_conversion')

        except Order.DoesNotExist:
            if 'order' in context:
                del context['order']
            context['title'] = _('Информации нет')

        return render(request, 'user/%s/order.html' % request.folder, context)

    def post(self,request,*args,**kwargs):
        if request.user.is_admin:
            order = Order.objects.get(id=kwargs['id'])
        else:
            order = Order.objects.get(id=kwargs['id'],user=request.user)
        order = CheckoutForm(request.POST,instance=order)
        if order.is_valid():
            order.save()
            return JsonResponse({'result':1})

        return JsonResponse({'result':order.errors})

class ProfileView(View):
    def get(self,request,*args,**kwargs):
        context = {
            'view':'Profile'
        }

        context['title'] = _('Личный кабинет')

        if request.user.name != 'bigopt':
            context['orders'] = Order.objects.filter(user=request.user).order_by('-id')

        return render(request, 'user/%s/profile.html' % request.folder,context)