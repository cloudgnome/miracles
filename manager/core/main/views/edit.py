from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse,Http404
from json import loads,dumps
from django.views.generic import View
from django.db.models.fields.files import ImageFieldFile
from shop.models import Language
from main.models import Meta
from settings import COMPANY_NAME, PHONES

class EditViewSimple(View):
    def get(self,request,*args,**kwargs):
        Model = kwargs.get('Model')
        item = get_object_or_404(Model.objects,pk=kwargs.get('id'))

        initial = item.__dict__
        form = Model.form(initial=initial,instance=item)

        context = {
            'item':item,
            'form':form,
            'Model':Model,
            '%s_id' % Model:item.pk,
            'context':{
                'title':Model.title(item)
            }
        }
        context = Model.extraContext(context)

        context['context'] = dumps(dumps(context['context']))

        return render(request,Model.editTemplate,context)

    def post(self,request,*args,**kwargs):
        Model = kwargs.get('Model')
        item = get_object_or_404(Model.objects,pk=kwargs.get('id'))
        json = loads(request.body.decode('utf8'))

        updated = 0
        for field,value in json.items():
            if Model.update_field(item,field,value):
                updated += 1

        if updated:
            item.save()
            return JsonResponse({'result':True,'updated':updated})

        return JsonResponse({'result':False,'updated':updated})

    def put(self,request,*args,**kwargs):
        Model = kwargs.get('Model')
        item = get_object_or_404(Model.objects,pk=kwargs.get('id'))
        json = loads(request.body.decode('utf8'))

        initial = item.__dict__
        form = Model.form(json,instance=item,initial=initial)

        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            form.save_m2m()
            Model.saveExtras(json,item)

            return JsonResponse({'result':True})
        else:
            return JsonResponse({'result':False,'errors':form.errors,'nonferrs':form.non_field_errors()})

class EditView(EditViewSimple):
    def get(self,request,*args,**kwargs):
        Model = kwargs.get('Model')
        if Model.editTemplate != 'main/slug.html':
            return super().get(request,*args,**kwargs)

        item = get_object_or_404(Model.objects,pk=kwargs.get('id'))

        initial = item.__dict__
        form = Model.form(initial=initial,instance=item)

        context = {
            'item':item,
            'form':form,
            'Model':Model,
            '%s_id' % Model:item.pk,
            'context':{
                'title':Model.title(item)
            }
        }
        context['meta'] = []
        for lang in Language.objects.all():

            try:
                meta = Model.meta(instance=item.description.get(language=lang),initial={'lang':lang})
            except:
                meta = Model.meta(initial={'lang':lang,'name':item.name},item=item)

            context['meta'].append(meta)
        context = Model.extraContext(context)

        context['context'] = dumps(dumps(context['context']))

        return render(request,Model.editTemplate,context)

    def put(self,request,*args,**kwargs):
        Model = kwargs.get('Model')
        if Model.editTemplate != 'main/slug.html':
            return super().put(request,*args,**kwargs)

        item = get_object_or_404(Model.objects,pk=kwargs.get('id'))
        json = loads(request.body.decode('utf8'))
        initial = item.__dict__

        metaM2M = []
        json['description'] = []
        for lang in Language.objects.all():
            try:
                currentMeta = item.description.get(language=lang)
                metaForm = Model.meta(json,instance=currentMeta,initial=currentMeta.__dict__,prefix=lang.code)
            except Exception as e:
                metaForm = Model.meta(json,item=item,initial={'lang':lang,'name':item.name},prefix=lang.code)

            if metaForm.is_valid():
                meta = metaForm.save(commit=False)

                template = Meta.objects.filter(language=meta.language,model=list(dict(Meta.model_choices).values()).index(Model.form._meta.model.__name__)).first()
                if template:
                    meta.title = meta.title or template.title.format(**{'obj':meta,'COMPANY_NAME':COMPANY_NAME})
                    meta.meta_description = meta.meta_description or template.meta_description.format(**{'obj':meta,'COMPANY_NAME':COMPANY_NAME,'PHONES':' '.join(PHONES)})[:255]
                    meta.meta_keywords = meta.meta_keywords or template.meta_keywords.format(**{'obj':meta,'COMPANY_NAME':COMPANY_NAME,'PHONES':' '.join(PHONES)})[:255]

                if not meta.title and not template:
                    return JsonResponse({'nonferrs':'Укажите title или заполните <a href="/meta/list">Meta</a>-шаблон.'})

                if not meta.meta_description and not template:
                    return JsonResponse({'nonferrs':'Укажите meta_description или заполните <a href="/meta/list">Meta</a>-шаблон.'})

                metaM2M.append(meta)
            else:
                return JsonResponse({'errors':metaForm.errors,'nonferrs':metaForm.non_field_errors()})

        form = Model.form(json,instance=item,initial=initial,name=metaM2M[0].name)

        if form.is_valid():
            item = form.save(commit=False)

            if item.customView == 'City':
                item.customView = 'Home'

            item.save()

            form.save_m2m()
            Model.saveExtras(json,item)

            for meta in metaM2M:
                meta.save()
                item.description.add(meta)

            context = {
                'result':True
            }
            context.update(Model.context(item))

            return JsonResponse(context)

        return JsonResponse({'errors':form.errors,'nonferrs':form.non_field_errors()})

    def delete(self,request,Model,*args,**kwargs):
        item = get_object_or_404(Model.objects,pk=kwargs.get('id'))
        item.delete()

        return JsonResponse({'result':True})