from django import forms

class SelectInputWidget(forms.TextInput):
    template_name = "form/select_input.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['departament'] = self.model.departament
        return context