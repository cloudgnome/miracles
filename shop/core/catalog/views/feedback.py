from django.views.generic import View
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render
from catalog.models import Product
from catalog.forms import FeedbackForm
from json import loads

class FeedbackView(View):
    def post(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            data = loads(request.body)
            data['author'] = request.user.name
            form = FeedbackForm(data)
            if form.is_valid():
                form.save()
                try:
                    Product.objects.get(id=data.get('product')).feedback_cache()
                except:
                    pass
                return JsonResponse({'result':True,'author':request.user.name})
            else:
                return JsonResponse({'result':False,'errors':form.errors})
        else:
            return JsonResponse({'result':False,'authenticate':True})