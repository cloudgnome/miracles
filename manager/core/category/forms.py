from django import forms
from main.forms import SlugifyForm
from main.fields import AutocompleteSelectField
from catalog.models import Category
from redactor.widgets import RedactorEditor
from main.widgets import ImageWidget
from main.fields import ImageField
from transliterate import slugify
from django.utils.translation import ugettext_lazy as _

class CategoryForm(SlugifyForm):
    parent = AutocompleteSelectField(model=Category,help_text=None,label=_('Родительская'),required=False)
    image = ImageField(
        widget=ImageWidget(),
        label='Logo',
        required=False
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.model = self.instance
        self.fields['description'].required = False
        self.fields['bgcolor'].required = False

    class Meta:
        model = Category
        fields = '__all__'
        fieldsets = [
                    ('main', {'fields':['slug','bgcolor','active','image'],'legend':'Общее'}),
                    ('related', {'fields':['parent'],'legend':'Связи'})
                ]