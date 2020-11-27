from django.shortcuts import render


# Create your views here.
from seller.forms import *


def sellerinfo(request):
    return render(request, 'seller/sellerinfo.html', {})


def sellersetting(request):
    context = {}
    if request.method == 'GET':
        context['form'] = SellerForm()
        return render(request, 'seller/sellersetting.html', context)

    form = SellerForm(request.POST)
    return render(request, 'seller/sellerinfo.html', {})

def addItems(request):
    context = {}
    if request.method == 'GET':
        context['form'] = ItemForm()
        return render(request, 'seller/addItem.html', context)


    return render(request, 'seller/addItem.html', {})