from django.shortcuts import render
from order.forms import OrderForm
from user.forms import UserOrderForm
from checkout.models import Order
from user.models import User
from django.http import JsonResponse

class EditView(View):
    def get(self,request,*args,**kwargs):
        try:
            order = Order.objects.get(id=kwargs.get['id'])
        except Order.DoesNotExist:
            return redirect('/order/list')
        form = OrderForm(initial=order.__dict__,instance=order)
        user = UserOrderForm(instance=order.user)
        date = str(timezone.now().date())

        context = {
            'date':date,
            'model':'order',
            'view':'order',
            'order':order,
            'form':form,
            'user':user
        }

        return render(request,'order.html',context)

    def post(self,request,*args,**kwargs):
        order = Order.objects.get(id=kwargs.get['id'])
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

class AddView(View):
    def get(self,request,*args,**kwargs):
        context = {}
        context['form'] = OrderForm()
        context['view'] = 'order'
        context['user'] = UserOrderForm()
        context['js'] = 'order'
        context['model'] = 'order'

        return render(request,'order.html',context)

    def post(self,request,*args,**kwargs):
        form = OrderForm(request.POST,prefix='order')
        user = UserOrderForm(request.POST,prefix='user')
        if user.is_valid():
            user = user.save()
        elif not request.POST.get('phone') or not request.POST.get('name'):
            user = User.objects.get(name='Администратор')

        if form.is_valid():
            cart = Cart()
            cart.session_id = request.session.session_key
            cart.save()
            order = form.save(commit=False)
            order.user = user
            order.cart = cart
            order.save()
            return JsonResponse({'result':True,'href':'/order/edit/%s' % order.id,'item_id':order.id})
        else:
            return JsonResponse({'errors':form.errors,'user-errors':user.errors})