#-*- coding=utf-8 -*-
from django.db import models
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from random import choice
from string import ascii_lowercase, digits
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)
from django.utils.translation import ugettext_lazy as _
from settings import BASE_URL

class PassCode(models.Model):
    code = models.CharField(max_length=25,verbose_name=_('Код'))
    created = models.DateTimeField(auto_now_add=True)

class User(models.Model):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,blank=True,null=True)
    verified = models.BooleanField(default=0,verbose_name=_("Email подтвержден"))
    name = models.CharField(max_length=255,blank=False,null=True,verbose_name=_('Имя'))
    lname = models.CharField(max_length=255,blank=False,null=True,verbose_name=_('Фамилия'))
    sname = models.CharField(max_length=255,blank=False,null=True,verbose_name=_('Отчество'))
    phone = models.CharField(max_length=16,verbose_name=_('Номер телефона'), null=True)
    password = models.CharField(verbose_name='password', max_length=128)
    is_active = models.BooleanField(verbose_name='active', default=True)
    is_admin = models.BooleanField(default=False)
    subscription = models.BooleanField(verbose_name=_('Подписка на рассылку'),default=True)
    price_type_choices = (
        (1,_('Розничная')),
        (2,_('Биг-оптовая')))
    price_type = models.PositiveIntegerField(choices=price_type_choices,default=1,verbose_name=_("Тип цен"))
    last_login = models.DateTimeField(auto_now_add=True,verbose_name=_("Последний раз на сайте"),null=True)
    created_at = models.DateTimeField(auto_now_add=True,verbose_name=_("Дата регистрации"),null=True)
    device_token = models.CharField(max_length=50,unique=True,null=True)
    notifications = models.BooleanField(default=1)
    fcm_token = models.CharField(max_length=255,null=True)
    update_departaments = models.BooleanField(default=False)
    social_type_choices = (
            (1,'fb'),
            (2,'g')
        )
    social_type = models.PositiveIntegerField(null=True,choices=social_type_choices)
    social_id = models.CharField(max_length=255,null=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'device_token'

    @property
    def full_name(self):
        return "%s %s %s" % (self.name,self.lname,self.sname)

    def dict(self):
        fields = ['id','sname','lname','name','notifications','phone','email','subscription']

        data = {field:getattr(self,field) for field in fields}

        return data

    def init_form(self,data):
        fields = ['sname','lname','name','phone','email','subscription','notifications']

        for field in fields:
            if data.get(field) is None:
                data[field] = getattr(self,field)

        return data

    @property
    def is_opt(self):
        return True if self.price_type == 2 else False

    @property
    def db(self):
        return self._state.db

    @property
    def admin(self):
        return '<div class="bool %s"></div>' % str(self.is_admin).lower()

    def restore_password(self,code):
        context = {'phone':self.phone,'password':code}
        subject, from_email, to = _('Восстановление пароля', "%s Интернет магазин <info@%s>") % (BASE_URL,BASE_URL), self.email
        text_content,html_content = render_to_string('verify.txt',context),render_to_string('verify.html',context)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def save(self,*args,**kwargs):
        if self.pk:
            try:
                user = User.objects.get(pk=self.pk)
                if user.__dict__ == self.__dict__:
                    return
            except User.DoesNotExist:
                pass
        super().save(*args,**kwargs)

    def generate_name(length=16, chars=ascii_lowercase+digits, split=4, delimiter=_('-')):
    
        name = ''.join([choice(chars) for i in range(length)])
        
        if split:
            name = delimiter.join([name[start:start+split] for start in range(0, len(name), split)])
        
        try:
            User.objects.get(name=name)
            return generate_name(length=length, chars=chars, split=split, delimiter=delimiter)
        except User.DoesNotExist:
            return name

    def make_random_password(length=32,
                             allowed_chars='abcdefghjkmnpqrstuvwxyz'
                                           'ABCDEFGHJKLMNPQRSTUVWXYZ'
                                           '23456789'):
        """
        Generate a random password with the given length and given
        allowed_chars. The default value of allowed_chars does not have "I" or
        "O" or letters and digits that look similar -- just to avoid confusion.
        """
        return get_random_string(length, allowed_chars)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def get_short_name(self):
        return self.name.title()

    def get_full_name(self):
        return '%s %s' % (self.first_name.title(), self.last_name.title(),)

    def __unicode__(self):
        return self.email

    def __str__(self):
        return self.name

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    class Meta:
        verbose_name = _('Пользователи')
        verbose_name_plural = _('Пользователи')

class AnonymousUser:
    id = None
    pk = None
    name = ''
    is_staff = False
    is_active = False
    is_superuser = False
    # _groups = EmptyManager(Group)
    # _user_permissions = EmptyManager(Permission)

    def __str__(self):
        return 'AnonymousUser'

    def __eq__(self, other):
        return isinstance(other, self.__class__)

    def __hash__(self):
        return 1  # instances always return the same hash value

    def save(self):
        raise NotImplementedError("Django doesn't provide a DB representation for AnonymousUser.")

    def delete(self):
        raise NotImplementedError("Django doesn't provide a DB representation for AnonymousUser.")

    def set_password(self, raw_password):
        raise NotImplementedError("Django doesn't provide a DB representation for AnonymousUser.")

    def check_password(self, raw_password):
        raise NotImplementedError("Django doesn't provide a DB representation for AnonymousUser.")

    @property
    def groups(self):
        return self._groups

    @property
    def user_permissions(self):
        return self._user_permissions

    def get_group_permissions(self, obj=None):
        return set()

    def get_all_permissions(self, obj=None):
        return _user_get_all_permissions(self, obj=obj)

    def has_perm(self, perm, obj=None):
        return _user_has_perm(self, perm, obj=obj)

    def has_perms(self, perm_list, obj=None):
        return all(self.has_perm(perm, obj) for perm in perm_list)

    def has_module_perms(self, module):
        return _user_has_module_perms(self, module)

    @property
    def is_anonymous(self):
        return True

    @property
    def is_opt(self):
        return False

    @property
    def is_admin(self):
        return False

    @property
    def is_authenticated(self):
        return False

    def get_username(self):
        return self.name