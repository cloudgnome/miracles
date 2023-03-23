from django import template

register = template.Library()

@register.simple_tag
def translate(obj, attr, lang):
    if obj:
        return getattr(obj, attr)(lang)