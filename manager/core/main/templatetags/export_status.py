from django import template
from catalog.models import Product
from main.models import ExportStatus

register = template.Library()

@register.simple_tag
def export_status(item, export, attr):
    try:
        return getattr(item.export_status.get(export=export).meta,attr)
    except Exception as e:
        return ''

@register.simple_tag
def export_status_checked(item,export,load):
	try:
		loadStatus = item.export_status.get(export=export,load=load)
	except ExportStatus.DoesNotExist:
		loadStatus = False

	return 'checked' if loadStatus else ''