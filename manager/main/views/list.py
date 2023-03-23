from django.shortcuts import render
from django.http import JsonResponse,Http404
from django.views.generic import View
from json import loads,dumps

class List(View):
    def get(self,request,Model,*args,**kwargs):
        context = Model.parse_context(request)

        Model.items(context)

        context.update({
            'Model':Model,
            'panel':Model.panel,
            'panel_shortcuts':Model.panel_shortcuts,
            'context':{}
        })

        Model.list_extra_context(context)
        Model.paginate(context)

        context['context'] = dumps(dumps(context['context']))

        return render(request,Model.listTemplate,context)

    def post(self,request,Model,*args,**kwargs):
        context = Model.parse_context(request)

        Model.items(context)
        Model.paginate(context)

        context.update({
            'Model':Model
        })

        return render(request,Model.itemsTemplate,context)

    def put(self,request,Model,*args,**kwargs):
        json = loads(request.body)
        updated = 0

        if json.get('update_data'):
            context = Model.parse_context(request)

            if json.get('update_list'):
                items = Model.objects.filter(id__in=json.get('update_list'))
            else:
                items = Model.items(context)

            for item in items:
                for field,value in json.get('update_data').items():
                    if Model.update_field(item,field,value):
                        updated += 1

            return JsonResponse({'result':True,'updated':updated})
        else:
            return JsonResponse({'result':True,'updated':updated})

    def delete(self,request,Model,*args,**kwargs):
        json = loads(request.body.decode('utf8'))

        deleted = Model.delete(json)

        return JsonResponse({'result':True,'deleted':deleted})