from django import template

register = template.Library()

@register.filter(name='attribute')
def attribute(value,id):
    return value.products.filter(id=id)