from checkout.forms import CheckoutForm,CustomSelectWidget
from .widgets import SelectInputWidget
from django import forms
from checkout.models import Order,Delivery_Departament,Np_Departament,Np_City,Delivery_City

class OrderForm(forms.ModelForm):
    def clean_city(self):
        value = self.cleaned_data['city']
        if self.cleaned_data.get('delivery_type') and self.cleaned_data['delivery_type'] == 'np':
            try:
                value = Np_City.objects.get(address=value).id
            except Np_City.DoesNotExist:
                try:
                    value = Np_City.objects.filter(address=value).first().id
                except:
                    pass
        elif self.cleaned_data.get('delivery_type') and self.cleaned_data['delivery_type'] == 'd':
            try:
                value = Delivery_City.objects.get(address=value).id
            except:
                try:
                    value = Delivery_City.objects.filter(address=value).first().id
                except:
                    pass

        return value

    def clean_departament(self):
        value = self.cleaned_data['departament']
        if self.cleaned_data.get('delivery_type') and self.cleaned_data['delivery_type'] == 'np':
            try:
                value = Np_Departament.objects.get(address=value).id
            except Np_Departament.DoesNotExist:
                pass
        elif self.cleaned_data.get('delivery_type') and self.cleaned_data['delivery_type'] == 'd':
            try:
                value = Delivery_Departament.objects.get(address=value).id
            except Delivery_Departament.DoesNotExist:
                pass

        return value

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            if self.instance.delivery_type == 'np':
                self.fields['city'] = forms.ModelChoiceField(widget=CustomSelectWidget(attrs={'autocomplete':'address-level2'}),queryset=Np_City.objects.all(),label='Город',required=False)
                # self.fields['departament'] = forms.ModelChoiceField(widget=CustomSelectWidget(),queryset=Np_Departament.objects.all(),label='Отделение',required=False)
            elif self.instance.delivery_type == 'd':
                self.fields['city'] = forms.ModelChoiceField(widget=CustomSelectWidget(attrs={'autocomplete':'address-level2'}),queryset=Delivery_City.objects.all(),label='Город',required=False)
                # self.fields['departament'] = forms.ModelChoiceField(widget=CustomSelectWidget(),queryset=Delivery_Departament.objects.all(),label='Отделение',required=False)
        if self.instance:
            self.fields['departament'].widget.model = self.instance
        self.fields['delivery_type'].required = False
        self.fields['payment_type'].required = False

    prefix = 'order'
    delivery_choices = (
        ('','-----'),
        ('np','Новая почта'),
        ('d','Деливери'),
        ('u','УкрПочта'),
        ('s','Самовывоз'),)
    payment_choices = (
        ('','-----'),
        (1,'Наличными при получении'),
        (2,'Приват 24'),)
    status_choices = (
        (1,'Новый'),
        (2,'Оплачен'),
        (3,'Отменен'),
        (10,'Ждем товар'),
        (9,'Опл. ждем'),
        (7,'На отправку'),
        (8,'Отправлен'),
        (4,'Нет связи'),
        (5,'Liqpay'),
        (6,'Закрыт'),)

    delivery_type = forms.CharField(label='Способ доставки*',widget=CustomSelectWidget(choices=delivery_choices),required=True)
    payment_type = forms.CharField(label='Способ оплаты*',widget=CustomSelectWidget(choices=payment_choices),required=True)
    city = forms.CharField(label='Город*',required=False,widget=forms.TextInput(attrs={'placeholder':'Город'}))
    departament = forms.CharField(label='Отделение',widget=SelectInputWidget(),required = False)

    status = forms.CharField(label='Статус',widget=CustomSelectWidget(choices=status_choices),required = False)
    comment = forms.CharField(label='Уточнения к заказу',widget=forms.Textarea(attrs={'rows':4}),required=False)

    class Meta:
        model = Order
        fields = ('delivery_type','city','departament','payment_type','status','comment')