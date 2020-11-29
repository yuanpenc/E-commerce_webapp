from django import forms

from order.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['orderid']

    def clean_desc(self):
        desc = self.cleaned_data['desc']
        return desc