from django.views.generic import View
from django.http import JsonResponse,HttpResponse
from django.middleware.csrf import get_token
from mobile.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from mobile.serializers import categories
from django.template.loader import render_to_string

__all__ = ['SignUpView']

class SignUpView(View):
    # def get(self,request,*args,**kwargs):
    #     try:
    #         response = render_to_string('AF3ECF26E8E8AB393962951DF77B86D7.txt')
    #     except Exception as e:
    #         response = str(e) + str(kwargs.get('name'))

    #     response = render_to_string('AF3ECF26E8E8AB393962951DF77B86D7.txt')

    #     return HttpResponse(response, content_type='text/plain')

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self,request,*args,**kwargs):
        data = authenticate(request)
        data['data']['categories'] = categories()
        return JsonResponse(data)