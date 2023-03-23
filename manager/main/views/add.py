from django.shortcuts import render
from django.http import JsonResponse,Http404
from django.views.generic import View
from json import loads,dumps
from shop.models import Language
from transliterate import slugify
from main.models import Meta
from settings import COMPANY_NAME, PHONES

__all__ = ['AddView']

class AddViewSimple(View):
    def get(self,request,*args,**kwargs):
        Model = kwargs.get('Model')
        form = Model.form()

        context = {
            'form':form,
            'view':str(Model),
            'model':Model,
            'context':dumps({})
        }

        return render(request,Model.editTemplate,context)

    def put(self,request,*args,**kwargs):
        Model = kwargs.get('Model')
        json = loads(request.body.decode('utf8'))
        form = Model.form(json)

        image_file = json.get('image')
        if image_file:
            del json['image']

        if form.is_valid():
            item = form.save(commit=False)

            item.save()
            form.save_m2m()
            Model.saveExtras(json,item)

            return JsonResponse({'result':True,'href':'/%s/%s' % (Model,item.id),'view':str(Model),'id':item.id})

        context = {
            'form':form,
            'view':str(Model)
        }

        return JsonResponse({'errors':form.errors,'nonferrs':form.non_field_errors()})

class AddView(AddViewSimple):
    def get(self,request,*args,**kwargs):
        Model = kwargs.get('Model')
        if Model.editTemplate != 'main/slug.html':
            return super().get(request,*args,**kwargs)

        form = Model.form()

        context = {
            'form':form,
            'view':str(Model),
            'model':Model,
            'meta':[Model.meta(initial={'lang':lang}) for lang in Language.objects.all()],
            'context':dumps({})
        }

        return render(request,Model.editTemplate,context) 

    def put(self,request,*args,**kwargs):
        Model = kwargs.get('Model')
        if Model.editTemplate != 'main/slug.html':
            return super().put(request,*args,**kwargs)

        json = loads(request.body.decode('utf8'))

        metaM2M = []

        for lang in Language.objects.all():
            metaForm = Model.meta(json,prefix=lang.code)
            if metaForm.is_valid():
                meta = metaForm.save(commit=False)

                template = Meta.objects.filter(language=meta.language,model=list(dict(Meta.model_choices).values()).index(Model.form._meta.model.__name__)).first()
                if template:
                    meta.title = meta.title or template.title.format(**{'obj':meta,'COMPANY_NAME':COMPANY_NAME})
                    meta.meta_description = meta.meta_description or template.meta_description.format(**{'obj':meta,'COMPANY_NAME':COMPANY_NAME,'PHONES':''.join(PHONES)})[:255]
                    meta.meta_keywords = meta.meta_keywords or template.meta_keywords.format(**{'obj':meta,'COMPANY_NAME':COMPANY_NAME,'PHONES':''.join(PHONES)})[:255]

                if not meta.title and not template:
                    return JsonResponse({'nonferrs':'Укажите title или заполните <a href="/meta/list">Meta</a>-шаблон.'})

                if not meta.meta_description and not template:
                    return JsonResponse({'nonferrs':'Укажите meta_description или заполните <a href="/meta/list">Meta</a>-шаблон.'})

                metaM2M.append(meta)
            else:
                return JsonResponse({'errors':metaForm.errors,'nonferrs':metaForm.non_field_errors()})

        form = Model.form(json,name=metaM2M[0].name)
        if form.is_valid():
            item = form.save(commit=False)

            if not item.slug:
                item.slug = slugify(metaM2M[0].name) or metaM2M[0].name

            if item.view == 'City':
                item.view = 'Home'

            item.save()
            form.save_m2m()
            Model.saveExtras(json,item)

            for meta in metaM2M:
                meta.save()
                item.description.add(meta)

            return JsonResponse({'result':True,'href':'/%s/%s' % (Model,item.id),'view':str(Model),'id':item.id})

        context = {
            'form':form,
            'view':str(Model)
        }

        return JsonResponse({'errors':form.errors,'nonferrs':form.non_field_errors()})