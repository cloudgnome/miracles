# -*- coding: utf-8 -*-
from django import forms
from checkout.models import Order
from cart.models import Cart
from django.utils.encoding import force_text
from django.utils.html import escape, conditional_escape
from django.utils.safestring import mark_safe
from checkout.widgets import SelectWithDisabled
from django.utils.translation import ugettext_lazy as _
import re

class CallbackForm(forms.Form):
    phone = forms.CharField(max_length=16,label=_('Введите номер телефона:'),widget=forms.TextInput(attrs={'placeholder': _('Номер телефона'),'type':'tel'}),required=True)

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r'[+\d]{9,20}',phone):
            raise forms.ValidationError(_('Неправильный телефон(пример +30971112233)'))

        return phone

    class Meta:
        fields = ('phone',)

class CartForm(forms.ModelForm):
    model = Cart
    fields = ('order','product','price','qty')

class CheckoutForm(forms.ModelForm):
    delivery_choices = (
        (4,_('Самовывоз')),
        (1,_('Новая почта')),
        (2,_('Деливери')),
        (3,_('УкрПочта')),
        (5,_('Курьерская Доставка'))
    )
    payment_choices = (
        (1,_('Наличными при получении')),
        (2,_('Оплата картой')),)

    delivery_type = forms.CharField(label=_('Способ доставки:'),widget=SelectWithDisabled(attrs={'autocomplete':'off'},choices=delivery_choices),required=True)
    payment_type = forms.CharField(label=_('Способ оплаты:'),widget=SelectWithDisabled(attrs={'autocomplete':'off'},choices=payment_choices),required=True)
    comment = forms.CharField(label=_('Уточнения к заказу:'),widget=forms.Textarea(attrs={'rows':4}),required=False)
    name = forms.CharField(label=_('Имя:'),widget=forms.TextInput(attrs={'placeholder':_('Имя'),'required':''}),required=False)
    lname = forms.CharField(label=_('Фамилия:'),widget=forms.TextInput(attrs={'placeholder':_('Фамилия'),'required':''}),required=False)
    sname = forms.CharField(label=_('Отчество:'),widget=forms.TextInput(attrs={'placeholder':_('Отчество'),'required':''}),required=False)
    email = forms.EmailField(label='Email:',widget=forms.TextInput(attrs={'placeholder':'Email'}),required=False)
    phone = forms.CharField(label=_('Номер телефона:'),widget=forms.TextInput(attrs={'placeholder':_('Телефон'),'type':'text'}))
    address = forms.CharField(label=_('Адрес:'),widget=forms.TextInput(attrs={'placeholder':_('Адрес')}),required=False)
    subscription = forms.BooleanField(label=_('Подписаться на рассылку'),widget=forms.CheckboxInput(attrs={'checked':''}),required=False)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['lname'].required = False
        self.fields['sname'].required = False
        self.fields['city'].required = False
        self.fields['departament'].required = False

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        phone = re.sub('[^\d]','',phone)
        if not re.match(r'[\d]{9,16}',phone):
            raise forms.ValidationError(_('Неправильный телефон(пример 0971112233)'))

        return phone

    def clean(self):
        data = super().clean()
        if not 'delivery_type' in data or data['delivery_type'] != '4':
            # if not data['sname']:
            #     raise forms.ValidationError({'sname':_('Обязательное поле')})
            if not data['name']:
                raise forms.ValidationError({'name':_('Обязательное поле')})
            if not data['lname']:
                raise forms.ValidationError({'lname':_('Обязательное поле')})

        if not 'delivery_type' in data or data['delivery_type'] == '3' and not data['address']:
            raise forms.ValidationError({'address':_('Обязательное поле')})

        if not 'delivery_type' in data or data['delivery_type'] == '5' and not data['address']:
            raise forms.ValidationError({'address':_('Обязательное поле')})

        return data

    class Meta:
        model = Order
        fields = ('address','delivery_type','city','departament','payment_type','comment','email','phone','name','lname','sname')

class OneClickOrderForm(forms.ModelForm):
    name = forms.CharField(label=_('Имя:'),widget=forms.TextInput(attrs={'placeholder': _('Имя')}),required=True)
    phone = forms.CharField(max_length=18,label=_('Номер телефона:'),widget=forms.TextInput(attrs={'placeholder': 'Номер телефона(Формат: 099 999 99 99)','title':'Формат: 099 999 99 99'}),required=True)

    class Meta:
        model = Order
        fields = ('name','phone')