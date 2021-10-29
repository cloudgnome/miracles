from django import template
from checkout.models import Order
from catalog.models.product import Product
register = template.Library()
 
@register.inclusion_tag('order_admin.html')
def products(object_id):
	order = Order.objects.get(pk=object_id)
	order_dict = order.order_dict()
	products = Product.objects.filter(pk__in=order_dict.keys())
	data = {}
	total = 0
	for product in products:
		if str(product.id) in order_dict:
			data[product] = order_dict[str(product.id)]
			total += product.price * order_dict[str(product.id)]
		elif product.id in order_dict:
			data[product] = order_dict[product.id]
			total += product.price * order_dict[product.id]
	return { 'products': data, 'total': order.total }

@register.filter(name='multiply')
def multiply(value, arg):
	return value*arg