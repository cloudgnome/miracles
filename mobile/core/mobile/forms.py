#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.forms import ModelForm,Form,CharField
from user.models import User

class Form(Form):
    @property
    def errors(self):
        """Return an ErrorDict for the data provided for the form."""
        if self._errors is None:
            self.full_clean()

        errors = ''
        if self._errors:
            error_list = dict(self._errors)
            for key in error_list.keys():
                for value in list(error_list[key]):
                    errors += value

        return errors

class ModelForm(ModelForm):
    @property
    def errors(self):
        """Return an ErrorDict for the data provided for the form."""
        if self._errors is None:
            self.full_clean()

        errors = ''
        if self._errors:
            error_list = dict(self._errors)
            for key in error_list.keys():
                for value in list(error_list[key]):
                    errors += value

        return errors

device_token_errors = {
    'required': 'device_token обязательно поле',
    'invalid': 'Некорректное значение device_token',
    'max_length': 'Длина device_token должна быть не более 50 символов'
}
class TokenForm(Form):
    device_token = CharField(max_length=50,error_messages=device_token_errors)

name_errors = {
    'required': 'Имя обязательно',
    'invalid': 'Некорректное имя',
    'max_length': 'Длина имени должна быть не более 20 символов'
}
image_errors = {
    'invalid': 'Ошибка сохранения изображения'
}

class UserForm(ModelForm):
    name = CharField(max_length=20,error_messages=name_errors)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['fcm_token'].required = False
        self.fields['name'].required = False
        self.fields['notifications'].required = False
        self.fields['email'].required = False
        self.fields['phone'].required = False

    class Meta:
        model = User
        fields = ('name','notifications','fcm_token','email','phone')