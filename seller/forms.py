from django import forms
from django.contrib.auth import authenticate

from goods.models import Items
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
        exclude = {'stocks', 'sales', 'content_type', 'status', 'seller', 'created_by'}

        widgets = {
            'desc': forms.Textarea(),
            'detail': forms.Textarea(),
            'category': forms.Select(choices=(('Arts', 'Arts'), ('Automotive', 'Automotive'), ('Baby', 'Baby'),
                                              ('Books', 'Books'), ('Computers', 'Computers'),
                                              ('Electronics', 'Electronics'), ('Health', 'Health'),
                                              ('Luggage', 'Luggage'), ('Software', 'Software'))),
        }

        labels = {
            'desc': "Description"
        }
