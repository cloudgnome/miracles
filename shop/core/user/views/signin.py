from django.views.generic import View
from user.forms import SignInForm,ForgetPassForm
from django.forms.utils import ErrorList
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login
from django.shortcuts import render,redirect
from django.http import JsonResponse
from user.models import User
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from json import loads

__all__ = ['SigninView','authenticate']

class SigninView(View):
    template = ''

    def get(self,request,*args,**kwargs):
        if request.user.is_anonymous:
            context = {}
            context['base'] = 'shop/base.html' if request.is_ajax() else 'shop/%s/index.html' % request.folder
            context['next'] = request.GET.get('next')
            context['form'] = SignInForm()
            context['forget_form'] = ForgetPassForm()
            context['view'] = 'Signin'

            template = kwargs.get('template')
            if not template:
                template = 'user/%s/signin.html' % request.folder
            return render(request, template,context)
        elif request.is_ajax():
            return JsonResponse({'result':True})
        elif request.GET.get('next'):
            return redirect(request.GET.get('next'))
        else:
            return redirect('/')

    def post(self,request,*args,**kwargs):
        post = loads(request.body)

        if request.user.is_anonymous:
            base = 'shop/base.html' if request.is_ajax() else 'shop/%s/index.html' % request.folder
            form = SignInForm(post)

            if form.is_valid():
                if form.cleaned_data['phone'] == 'bigopt':
                    user = authenticate(value='bigopt', password=form.cleaned_data['password'])
                else:
                    user = authenticate(value=form.cleaned_data['phone'], password=form.cleaned_data['password'])
                if user is not None and request.is_ajax():
                    login(request, user)
                    return JsonResponse({'result':True})
                elif user is not None:
                    login(request,user)
                    next = post.get('next')
                    if next:
                        return redirect(next)
                    else:
                        return redirect('/user/profile/')
                else:
                    errors = form._errors.setdefault("__all__", ErrorList())
                    errors.append(_("Пароль не подошел"))
            else:
                errors = form._errors.setdefault("__all__", ErrorList())
                errors.append(_("Пароль не подошел"))

            template = kwargs.get('template')

            if not template:
                template = 'user/%s/signin.html' % request.folder

            return render(request, template,{'base':base,'form':form,'js':'login','forget_form':ForgetPassForm()})

        elif request.is_ajax():
            return JsonResponse({'result':True})

        elif request.GET.get('next'):
            return redirect(request.GET.get('next'))

        else:
            return redirect('/')

def find(key,value):
    params = {'%s' % key:value}
    try:
        return [User.objects.get(**params)]
    except User.MultipleObjectsReturned:
        return User.objects.filter(**params)
    except User.DoesNotExist:
        return []

def authenticate(value=None, password=None):
    for key in ['phone','email','name']:
        users = find(key,value)
        if users:
            break
    for user in users:
        if check_password(password, user.password):
            user.backend = 'user.backends.ModelBackend'
            user.last_login = timezone.now()
            return user
    return None