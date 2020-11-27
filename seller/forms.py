from django import forms
from django.contrib.auth import authenticate
from seller.models import *


class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        exclude = {'user', 'image_content_type', 'qrcode_content_type'}

        widgets = {
            'desc': forms.Textarea()
        }

        labels = {
            'desc': "Description",
        }

class ItemForm(forms.ModelForm):
    class Meta:
        model = Items
        exclude = {'stocks', 'sales', 'content_type', 'status', 'seller'}

        widgets = {
            'desc': forms.Textarea(),
            'detail' : forms.Textarea(),
        }

        labels = {
            'desc': "Description"
        }