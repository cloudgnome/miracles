from django.http import Http404
from user.forms import ForgetPassForm,ChangePasswordForm
from user.models import User,PassCode
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import auth
from django.shortcuts import render,redirect
from django.utils.translation import ugettext_lazy as _

__all__ = ['forget_password','ChangePasswordView']

def forget_password(request):
    if request.POST:
        form = ForgetPassForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(phone=form.cleaned_data['phone'])
                if user.is_admin:
                    raise Exception
            except Exception:
                return render(request, 'forget_password.html',{'form':form,'error':_('Пользователь не найден.')})
            passcode = PassCode()
            passcode.code = User.make_random_password()
            passcode.save()
            user.restore_password(passcode.code)
            return render(request, 'forget_password.html')
    return render(request, 'user/forget_password.html',{'form':form})

class ChangePasswordView(View):
    def get(self, request, *args, **kwargs):
        if 'password' in request.GET and 'phone' in request.GET:
            try:
                user = User.objects.get(phone=request.GET['phone'])
                password = PassCode.objects.get(code=request.GET['password'])
                if request.GET['password'] == password.code:
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    auth.login(request, user)
                    if not user.verified:
                        user.verified = True
                        user.save()
                    return redirect('/user/change-password')
                else:
                    raise Http404(_('Не сошлись данные пароля'))
            except Exception:
                raise Http404(_('Не сошлись данные'))
        if request.user.is_authenticated:
            context = {}
            context['title'] = _('Смена пароля')
            context['form'] = ChangePasswordForm()
            if 'result' in context:
                del context['result']
            return render(request,'user/%s/change-password.html' % request.folder,context)
        else:
            return redirect('/')

    @method_decorator(login_required)
    def post(self,request, *args, **kwargs):
        if request.user.is_authenticated:
            context = {}
            context['title'] = _('Смена пароля')
            context['form'] = ChangePasswordForm(request.POST)
            if context['form'].is_valid():
                user = request.user
                user.set_password(context['form'].cleaned_data['password1'])
                user.save()
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                auth.login(request, user)
                context['form'] = False
                context['result'] = _('Пароль изменен успешно.')
            return render(request,'user/%s/change-password.html' % request.folder,context)
        else:
            return redirect('/')