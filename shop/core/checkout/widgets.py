from django import forms
from django.forms.widgets import TextInput

class SelectWithDisabled(forms.Select):
    """
    Subclass of Django's select widget that allows disabling options.
    To disable an option, pass a dict instead of a string for its label,
    of the form: {'label': 'option label', 'disabled': True}
    """
    def render_option(self, selected_choices, option_value, option_label):
        option_value = force_text(option_value)
        if (option_value in selected_choices):
            selected_html = u' selected="selected"'
        else:
            selected_html = ''
        disabled_html = ''
        if isinstance(option_label, dict):
            if dict.get(option_label, 'disabled'):
                disabled_html = u' disabled="disabled"'
            option_label = option_label['label']
        return u'<option value="%s"%s%s>%s</option>' % (
            escape(option_value), selected_html, disabled_html,
            conditional_escape(force_text(option_label)))

class CustomSelectWidget(SelectWithDisabled):
    template_name = "form/select.html"

class PhoneWidget(TextInput):
    def render(self, name, value, attrs=None):
        return mark_safe(u'''%s<a href="tel:%s" alt="позвонить"></a>''' % (super(PhoneWidget,self).render(name,value,attrs),value))