from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404

from goods.models import Items
import random

ITEMS_IN_ONE_PAGE = 15


def get_photo(request, id):
    item = get_object_or_404(Items, id=id)
    print('Picture #{} fetched from db: {} (type={})'.format(id, item.image, type(item.image)))

    # Maybe we don't need this check as form validation requires a picture be uploaded.
    # But someone could have delete the picture leaving the DB with a bad references.
    if not item.image:
        raise Http404

    return HttpResponse(item.image, content_type=item.content_type)


def list_items(request):
    pageNum = request.GET.get('pageNum', default='1')
    orderBy = request.GET.get('orderBy', default='id')
    items = Items.objects.all().order_by(orderBy)
    recommend = list()

    numOfItems = len(items)
    if numOfItems <= 2:
        recommend = items
    else:
        num1 = random.randint(0, numOfItems - 1)
        num2 = random.randint(0, numOfItems - 1)
        while num2 == num1:
            num2 = random.randint(0, numOfItems - 1)
        recommend.append(items[num1])
        recommend.append(items[num2])

    start = (int(pageNum) - 1) * ITEMS_IN_ONE_PAGE
    end = start + ITEMS_IN_ONE_PAGE
    context = {'items': items[start:end],
               'user': request.user,
               'recommend': recommend}

    return render(request, 'goods/list_items_demo.html', context)


def detail(request):
    itemId = request.GET.get('itemId', default='1')
    item = Items.objects.get(id=itemId)

    items = Items.objects.all().order_by('id')
    recommend = list()

    numOfItems = len(items)
    if numOfItems <= 2:
        recommend = items
    else:
        num1 = random.randint(0, numOfItems - 1)
        num2 = random.randint(0, numOfItems - 1)
        while num2 == num1:
            num2 = random.randint(0, numOfItems - 1)
        recommend.append(items[num1])
        recommend.append(items[num2])

    context = {'item': item,
               'recommend': recommend}

    return render(request, 'goods/item_detail_demo.html', context)
