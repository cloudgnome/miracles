from django.views.generic import View
from user.forms import UserCreationForm,UserSocialForm
from user.models import User
from django.contrib.auth import authenticate,login
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _
from json import loads
from requests import get
from settings import MEDIA_ROOT
import os
from transliterate import slugify

class SignupView(View):
    form = UserCreationForm
    template = 'user/%s/signup.html'
    path = '%susers/image/%s/'

    def email(self,json):
        social_type = dict(User.social_type_choices).get(json.get('social_type'))
        email = json.get('email')
        email = email if email else '%s%s@mail.ru' % (social_type,json.get('social_id'))

        return email

    def social_auth(self,request):
        json = loads(request.body.decode('utf-8'))
        user = False
        try:
            user = User.objects.get(social_type=json.get('social_type'),social_id=json.get('social_id'))
        except User.DoesNotExist:
            json['email'] = self.email(json)
            form = UserSocialForm(json)
            if form.is_valid():
                user = form.save()

        if user:
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request,user)
            return JsonResponse({'href':request.META.get('HTTP_REFERER','/')})
        else:
            return JsonResponse({'errors':form.errors})

    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        context = {}
        context['base'] = 'shop/base.html' if request.is_ajax() else 'shop/%s/index.html' % request.folder
        context['form'] = self.form()
        context['h1'] = _('Регистрация')
        return render(request, self.template % request.folder, context)

    def post(self,request,*args,**kwargs):
        try:
            json = loads(request.body.decode('utf-8'))
            if json.get('social'):
                return self.social_auth(request)
        except Exception as e:
            pass

        form = self.form(loads(request.body.decode('utf-8')))
        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request,user)
            if request.is_ajax():
                return JsonResponse({'href':request.META.get('HTTP_REFERER','/')})
            else:
                return redirect(request.META['HTTP_REFERER'])
        else:
            context = {}
            context['base'] = 'shop/base.html' if request.is_ajax() else 'shop/%s/index.html' % request.folder
            context['form'] = form
            context['error'] = _('С полями формы что то не так.')
        return render(request, self.template % request.folder, context)

    def save_image(self,src,type):
        href = src
        if type == 1:
            src = src.replace('https://pp.userapi.com/','').replace('/','').replace('-','')
        elif type == 2:
            src = src.replace('https://platform-lookaside.fbsbx.com/','').replace('/','').replace('-','')

        path = self.path % (MEDIA_ROOT,src[0:2])
        if not os.path.isdir(path):
            os.mkdir(path)
            os.chmod(path,0o777)
        image = slugify(src,language_code='uk') + ".jpg"
        path = path + image

        if not os.path.isfile(path):
            r = get(href)
            image = "users/image/%s/%s" % (src[0:2],image)
            with open(path, 'wb') as f:
                for chunk in r.iter_content():
                    f.write(chunk)
        return image