from django.shortcuts import render


def list(request):
    return render(request, 'goods/list_items.html', {})


def detail(request):
    return render(request, 'goods/item_detail.html', {})
