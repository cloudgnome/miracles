from main.list.model import ModelAdmin
from catalog.models import Category,Prom,Prom_Category
from category.forms import CategoryForm
from django.db.models import Q

class CategoryAdmin(ModelAdmin):
    model = Category
    form = CategoryForm
    listView = 'CategoryList'
    searchTemplate = 'category/categories.html'
    listTemplate = 'category/categories.html'

    disabled_paginator = True

    def list_extra_context(self,context):
        context['items'] = context['items'].get_descendants(include_self=True)

        return context

    def search(self,value):
        if not value:
            return Q()

        return Q(name_ru__icontains=value)

    def saveExtras(self,json,category):
        category.proms.all().delete()
        if json.get('proms'):
            for value in json.get('proms'):
                prom_id,prom_category_id = value.split('|')
                prom = Prom.objects.get(prom_id=prom_id)
                try:
                    category.proms.get(prom=prom)
                except Prom_Category.DoesNotExist:
                    try:
                        category.proms.create(prom=prom,prom_category_id=prom_category_id)
                    except:
                        pass