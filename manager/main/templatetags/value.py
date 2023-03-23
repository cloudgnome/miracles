from django import template

register = template.Library()

@register.filter(name='value')
def value(model,item):
    for field in model:
        if '.' in field:
            try:
                yield eval('item.%s' % field)
            except:
                yield ''
        else: 
            yield getattr(item,field)

@register.filter(name='val')
def val(filters,key):
    return filters.get(key) or ''