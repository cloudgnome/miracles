from django.db.models import Q
from django.template.loader import get_template
from json import loads
from main.forms import PageDescriptionForm,CategoryDescriptionForm, \
BrandDescriptionForm,TagDescriptionForm,CityDescriptionForm, \
ArticleDescriptionForm, ProductDescriptionForm, StorageDescriptionForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ast import literal_eval

class ModelAdmin:
    exclude = {}
    listView = 'List'
    editTemplate = 'main/slug.html'
    searchHtml = 'main/items.html'
    listHtml = 'main/list.html'
    database = 'default'
    itemsTemplate = 'main/items.html'
    listTemplate = 'main/list.html'
    disabled_paginator = False

    def delete(self,json):
        deleted = self.objects.filter(pk__in=json).delete()

        try:
            return list(deleted[1].values())[0]
        except:
            return ''

    def update_field(self,item,field,value):
        try:
            getattr(item,field)
            setattr(item,field,value)

            return True
        except:
            return False

    def parse_context(self,request):
        context = request.GET.dict()
        context['filters'] = request.GET.copy()
        context['limit'] = request.session.get('limit',10)

        return context

    def items(self,context):
        ordering = context['filters'].get('o') or self.ordering

        query = self.filters(context)

        if query:
            items = self.objects.filter(query).order_by(ordering).distinct()
        else:
            items = self.objects.filter(query).exclude(**self.exclude).order_by(ordering).distinct()

        count = items.count()

        context.update({
            'items':items,
            'count':count
        })

    def filters(self,context):
        filters = {}

        if context:
            for field in context:
                if field in ['page','limit','o','all','filters']:
                    continue

                try:
                    value = literal_eval(context[field])
                    if value is None:
                        raise Exception()
                except:
                    value = context[field]

                if field == 'value':
                    return self.search(value)
                else:
                    filters[field] = value

            return Q(**filters)

        return Q()

    def paginate(self,context):
        all_items = context['filters'].get('all')
        page = context['filters'].get('page')

        try:
            limit = int(context.get('limit',context['filters'].get('limit')))
        except:
            limit = 10

        if not self.disabled_paginator and not all_items:
            paginator = Paginator(context['items'], limit)
            try:
                context['items'] = paginator.page(page or 1)
            except:
                context['items'] = paginator.page(1)

    def extraContext(self,context):
        return context

    def __eq__(self,value):
        return self.model == value

    @property
    def meta(self):
        return eval('%sDescriptionForm' % self.__str__())

    def __init__(self,database = 'default'):
        self.database = database

    def context(self,item):
        return {}

    def list_extra_context(self,context):
        return context

    def saveExtras(self,request,item):
        return

    @property
    def panel(self):
        try:
            panel = 'main/panel/%s.html' % self.__str__().lower()
            get_template(panel)
        except:
            panel = 'main/panel/default.html'

        return panel

    @property
    def editPanel(self):
        try:
            panel = 'main/panel/edit/%s.html' % self.__str__().lower()
            get_template(panel)
        except:
            panel = 'main/panel/edit/default.html'

        return panel

    @property
    def panel_shortcuts(self):
        try:
            panel = 'main/panel/shortcuts/%s.html' % self.__str__().lower()
            get_template(panel)
        except:
            panel = 'main/panel/shortcuts/default.html'

        return panel

    def title(self,item):
        if hasattr(item,'name'):
            return str(item.name)
        else:
            return str(item)

    @property
    def ordering(self):
        return self.order_by or '-id'

    def __str__(self):
        return self.model.__name__

    def __len__(self):
        return len(self.list_display)

    def __iter__(self):
        for field in self.list_display:
            yield field

    def __getattr__(self,name):
        if hasattr(self.model,name):
            return getattr(self.model,name)

    def search(self,value):
        if not value:
            return Q()

        return Q(description__name__icontains=value)

    def get_filters(self,value):
        return Q(description__name__icontains=value)