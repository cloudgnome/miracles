from django import forms
from cart.models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('cart','product','price','qty')