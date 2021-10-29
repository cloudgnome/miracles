from django.http import JsonResponse
from checkout.forms import CheckoutForm,Order
from user.models import User
from cart.views import Buyer
from catalog.models import Product
from mobile.forms import UserForm
from json import loads

def checkout(request):
    data = loads(request.body.decode('utf8'))
    if request.user.is_anonymous:
        try:
            user = User.objects.get(phone=data.get('phone'))
            if user.is_admin:
                raise PermissionDenied
        except User.DoesNotExist:
            user = User.objects.create(phone=data.get('phone'),email=data.get('email'),name=data.get('name'))
            form = UserForm(request.user.init_form(data),instance=request.user)
            if form.is_valid():
                form.save()
        except User.MultipleObjectsReturned:
            user = User.objects.filter(phone=data.get('phone')).first()
            if user.is_admin:
                raise PermissionDenied
    else:
        user = request.user

    buyer = Buyer(request)
    for key in data['cart'].keys():
        buyer.add_item(Product.objects.get(id=key),data['cart'][key])

    buyer.cart.save()

    form = CheckoutForm(data)
    if form.is_valid():
        order = form.save(commit=False)
        order.user = user
        order.cart = buyer.cart
        order.save()
        order.send_mail(request)
        if 'cart_id' in request.session:
            del request.session['cart_id']

        if 'items_qty' in request.session:
            del request.session['items_qty']
        return JsonResponse({'success':1})

    return JsonResponse({'success':0,'errors':form.errors})

def quick_order(request):
    data = loads(request.body.decode('utf8'))
    if request.user.is_anonymous:
        try:
            user = User.objects.get(phone=data.get('phone'))
            if user.is_admin:
                raise PermissionDenied
        except User.DoesNotExist:
            user = User.objects.create(phone=data.get('phone'))
            form = UserForm(request.user.init_form(data),instance=request.user)
            if form.is_valid():
                form.save()
        except User.MultipleObjectsReturned:
            user = User.objects.filter(phone=data.get('phone')).first()
            if user.is_admin:
                raise PermissionDenied
    else:
        user = request.user

    buyer = Buyer(request)
    buyer.add_item(Product.objects.get(id=data['id']),data['qty'])

    order = Order.objects.create(
            user = user,
            cart = buyer.cart,
            phone = data.get('phone'),
            name = data.get('name'),
        )
    order.send_mail(request)
    if 'cart_id' in request.session:
        del request.session['cart_id']

    if 'items_qty' in request.session:
        del request.session['items_qty']

    return JsonResponse({'success':1})