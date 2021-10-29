from django.views.generic import View
from user.forms import SignInForm,ForgetPassForm
from django.forms.utils import ErrorList
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login
from django.shortcuts import render,redirect
from django.http import JsonResponse
from user.models import User
from json import loads

class SigninView(View):
    template = 'main/registration/login.html'

    def get(self,request,*args,**kwargs):
        if request.user.is_anonymous:
            context = {
                'next': request.GET.get('next'),
                'form': SignInForm(),
                'view': 'login'
            }
            return render(request, self.template,context)

        elif 'next' in request.GET:
            return redirect(request.GET['next'])
        else:
            return redirect('/')

    def post(self,request,*args,**kwargs):
        if request.user.is_anonymous:
            data = loads(request.body)
            form = SignInForm(data)
            if form.is_valid():
                user = authenticate(
                    name=form.cleaned_data['phone'],
                    password=form.cleaned_data['password']
                )

                if user is not None:
                    login(request, user)
                    return JsonResponse({'next':data.get('next') or '/'})
                else:
                    return JsonResponse({'errors':{'password':['Пароль не подошел']}})

            return JsonResponse({'errors':form.errors})
        else:
            return JsonResponse({'next':request.POST.get('next')})

def authenticate(name=None, password=None):
    try:
        user = User.objects.get(name=name)

        if check_password(password, user.password):
            user.backend = 'main.backends.ModelBackend'
            return user
    except:
        pass

    return None