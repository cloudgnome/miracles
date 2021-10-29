# -*- coding: utf-8 -*-
from django import forms
from .models import Review
from redactor.widgets import RedactorEditor
from form_utils.forms import BetterModelForm

class ReviewForm(BetterModelForm):
    description = forms.CharField(widget=RedactorEditor(attrs={'placeholder': 'Текст отзыва'}),label='Текст отзыва',required=True)
    class Meta:
        model = Review
        fields = ('title','description','active')
        fieldsets = [
                    ('main', {'fields':['title','active'],'legend':''}),
                    ('description', {'fields':['description'],'legend':'Описание','classes':['description']}),
                ]