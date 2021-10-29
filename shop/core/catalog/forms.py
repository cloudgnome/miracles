from django import forms
from catalog.models import Feedback

__all__ = ['FeedbackForm']

class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = '__all__'