# -*- coding: utf-8 -*-
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _

def validate_phone(value):
    try:
        phone = phonenumbers.parse(value,"UA")
        if not phonenumbers.is_valid_number(phone):
            raise Exception()
    except:
        raise ValidationError(_("Некорректный номер телефона"),params={'value': value})