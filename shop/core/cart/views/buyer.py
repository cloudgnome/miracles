from cart.models import Cart,Item
from catalog.models.product import Product
from django.shortcuts import redirect

class Buyer:
    def __init__(self,request):
        if not request.session.session_key:
            request.session.create()
            request.session.save()
        cart_id = request.session.get('cart_id')
        self.request = request
        if cart_id:
            try:
                cart = Cart.objects.get(pk=cart_id)
            except Cart.DoesNotExist:
                try:
                    cart = Cart.objects.get(session_id=request.session.session_key)
                except:
                    cart = self.new()
        else:
            cart = self.new()
        self.cart = cart

    def new(self):
        cart = Cart()
        cart.session_id = self.request.session.session_key
        cart.save()
        self.request.session['cart_id'] = cart.id
        return cart

    def add_item(self,item,qty):
        try:
            item = Item.objects.get(cart=self.cart,product=item)
            item.qty = int(qty)
            item.save()
        except Item.DoesNotExist:
            item = Item(cart=self.cart,product=item,qty=int(qty),price=item.price)
            item.save()

        return item

    def quick_order(self,item,qty):
        cart = Cart.objects.create(session_id=self.request.session.session_key)
        item = Item(cart=cart,product=item,qty=int(qty),price=item.price)
        item.save()
        cart.save()

        return cart

    def remove_item(self,id):
        try:
            item = Item.objects.get(cart=self.cart,pk=id)
            item.delete()
            self.cart.remove_item(item)
        except Item.DoesNotExist:
            pass

    def clear_cart(self):
        Item.objects.filter(cart=self.cart).delete()
        self.cart.clear()

    def checkout(self):
        if self.cart:
            get = self.request.GET
            self.cart.total = 0
            for item,qty in get.items():
                try:
                    item = Item.objects.get(cart=self.cart,pk=item)
                    if item.qty != int(qty):
                        item.qty = int(qty)
                        item.save()
                    self.cart.total += item.qty * item.product.price
                except Item.DoesNotExist:
                    continue
            self.cart.save()
            return redirect('/checkout/')
        else:
            return redirect('/')