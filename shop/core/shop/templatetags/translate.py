from django import template

register = template.Library()

@register.simple_tag
def translate(obj, attr, lang):
    if obj:
        if hasattr(obj,attr):
            return getattr(obj, attr)(lang)
        else:
            return obj
    else:
        return ''