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

    def clean_zip(self):
        zip = self.cleaned_data['zip']
        if zip < 10000:
            raise forms.ValidationError("Please insert valid zipcode")
        return zip
    
    def clean_image(self, MAX_UPLOAD_SIZE=2500000):
        image = self.cleaned_data['image']
        if image is None:
            return image
        # if not picture or not hasattr(picture, 'content_type'):
        #     raise forms.ValidationError('You must upload a picture')
        if not image.content_type or not image.content_type.startswith('image'):
            raise forms.ValidationError('File type is not image')
        if image.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return image

    def clean_qrcode(self, MAX_UPLOAD_SIZE=2500000):
        qrcode = self.cleaned_data['qrcode']
        if qrcode is None:
            return qrcode
        # if not picture or not hasattr(picture, 'content_type'):
        #     raise forms.ValidationError('You must upload a picture')
        if not qrcode.content_type or not qrcode.content_type.startswith('image'):
            raise forms.ValidationError('File type is not image')
        if qrcode.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return qrcode


class ItemForm(forms.ModelForm):
    class Meta:
        model = Items
        exclude = {'sales', 'content_type', 'status', 'created_by'}

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

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError('Price should be positive.')
        return price

    def clean_stocks(self):
        stocks = self.cleaned_data['stocks']
        if stocks < 0:
            raise forms.ValidationError('Stocks should be positive.')
        return stocks
    
    def clean_image(self, MAX_UPLOAD_SIZE=2500000):
        picture = self.cleaned_data['image']
        if not picture or not hasattr(picture, 'content_type'):
            raise forms.ValidationError('You must upload a picture')
        if not picture.content_type or not picture.content_type.startswith('image'):
            raise forms.ValidationError('File type is not image')
        if picture.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return picture


class ItemDetailForm(forms.ModelForm):
    class Meta:
        model = Items
        exclude = {'content_type', 'created_by'}

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

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError('Price should be positive.')
        return price

    def clean_stocks(self):
        stocks = self.cleaned_data['stocks']
        if stocks < 0:
            raise forms.ValidationError('Stocks should be positive.')
        return stocks

    def clean_sales(self):
        sales = self.cleaned_data['sales']
        if sales < 0:
            raise forms.ValidationError('Sales should be positive.')
        return sales

    def clean_image(self, MAX_UPLOAD_SIZE=2500000):
        image = self.cleaned_data['image']
        if image is None:
            return image
        # if not picture or not hasattr(picture, 'content_type'):
        #     raise forms.ValidationError('You must upload a picture')
        if not image.content_type or not image.content_type.startswith('image'):
            raise forms.ValidationError('File type is not image')
        if image.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return image