from django.shortcuts import render
from django.core.paginator import Paginator

def search(request,Model):
    value = request.GET.get('value')
    ordering = request.GET.get('o')
    page = request.GET.get('page')
    block = request.GET.get('block')
    limit = request.GET.get('limit') or 8
    filters = request.GET.copy()

    if request.is_ajax() and block:
        template = Model.searchHtml
    else:
        template = Model.listHtml

    query = Model.search(value)

    items = Model.objects.filter(query).order_by(ordering or '-id').distinct()[:100]
    found = items.count()

    paginator = Paginator(list(items), limit)
    try:
        items = paginator.page(page or 1)
    except:
        items = []

    context = {
        'items':items,
        'model':Model,
        'value':value,
        'page':page,
        'view':'List',
        'filters':filters,
        'panel':Model.panel,
        'count':Model.objects.count(),
        'found':found
    }

    return render(request,template,context)