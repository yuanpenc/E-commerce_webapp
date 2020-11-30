import json
import math

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404

from goods.models import Items
import random

# The number of items in one page
from information.models import Cart, Profile
from order.views import createOrder

ITEMS_IN_ONE_PAGE = 15


# get photo through an url
@login_required
def get_photo(request, id):
    item = get_object_or_404(Items, id=id)
    print('Picture #{} fetched from db: {} (type={})'.format(id, item.image, type(item.image)))

    # Maybe we don't need this check as form validation requires a picture be uploaded.
    # But someone could have delete the picture leaving the DB with a bad references.
    if not item.image:
        raise Http404

    return HttpResponse(item.image, content_type=item.content_type)


# for ajax request, return items whose name including user input based on a specific category
@login_required
def get_related(request):
    # filter item names based on related input information
    category = request.GET.get('category', default='all')
    if category == "all":
        items = Items.objects.all()
    else:
        items = Items.objects.all().filter(category=category)
    response_data = []

    for item in items:
        response_data.append(item.name)

    # organize item names in json format
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type='application/json')


# list items in market by a specific order
@login_required
def list_items(request):
    pageNum = request.GET.get('pageNum', default=1)
    orderBy = request.GET.get('orderBy', default='id')
    category = request.GET.get('category', default='all')
    searchItem = request.GET.get('search', default='noSearch')

    # filter items based on related input information
    if category == "all":
        items = Items.objects.all().order_by(orderBy)
    else:
        items = Items.objects.all().order_by(orderBy).filter(category=category)
    if searchItem != "noSearch":
        searchItem = str(searchItem).lower()
        newItems = []
        for item in items:
            name = item.name
            if searchItem in name.lower():
                newItems.append(item)
        items = newItems

    recommend = list()

    # get recommend items
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

    lastPageNum = math.ceil(numOfItems / ITEMS_IN_ONE_PAGE)

    # numbers show on page directory
    numOfPagesList = []
    if 1 <= int(pageNum) <= 3:
        count = 1
        while count <= lastPageNum and count <= 5:
            numOfPagesList.append(count)
            count = count + 1
    elif int(pageNum) == 4:
        if int(pageNum) < lastPageNum:
            numOfPagesList = [1, 2, 3, 4, 5]
        else:
            numOfPagesList = [1, 2, 3, 4]
    else:
        if int(pageNum) + 2 <= lastPageNum:
            numOfPagesList = [int(pageNum) - 2, int(pageNum) - 1, int(pageNum), int(pageNum) + 1, int(pageNum) + 2]
        else:
            numOfPagesList = [lastPageNum - 4, lastPageNum - 3, lastPageNum - 2, lastPageNum - 1, lastPageNum]

    # organize response context
    start = (int(pageNum) - 1) * ITEMS_IN_ONE_PAGE
    end = start + ITEMS_IN_ONE_PAGE

    context = {'items': items[start:end],
               'user': request.user.username,
               'recommend': recommend,
               'nums': numOfItems,
               'prePage': int(pageNum) - 1,
               'nextPage': int(pageNum) + 1,
               'showPre': not int(pageNum) == 1,
               'showNext': not int(pageNum) == lastPageNum,
               'numOfPagesList': numOfPagesList,
               'orderBy': orderBy,
               'search': searchItem,
               'category': category,
               'isHome': True,
               'cartNum': cart_size(request),
               'curPage': int(pageNum)}

    return render(request, 'goods/list_items_demo.html', context)


# show an item detail
@login_required
def detail(request):
    itemId = request.GET.get('itemId', default=1)
    item = Items.objects.get(id=itemId)
    category = request.GET.get('category', default='all')

    # filter items based on related input information
    if category == "all":
        items = Items.objects.all().order_by('id')
    else:
        items = Items.objects.all().order_by('id').filter(category=category)
    recommend = list()

    # get recommend items
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

    # organize response context
    context = {'item': item,
               'cartNum': cart_size(request),
               'user': request.user.username,
               'recommend': recommend}

    return render(request, 'goods/item_detail_demo.html', context)


# show the service page
@login_required
def service(request):
    return render(request, 'goods/service.html', {'isService': True,
                                                  'user': request.user.username,
                                                  'cartNum': cart_size(request)})


# buy an item directly
@login_required
def buy_now(request):
    itemId = request.GET.get('itemId')
    quantity = request.GET.get('quantity')
    totalPrice = request.GET.get('totalPrice')

    content = {
        str(itemId): int(quantity)
    }

    orderId = createOrder(request, json.dumps(content), float(totalPrice), "", request.user)

    response_json = json.dumps({"orderId": orderId, "totalPrice": totalPrice})

    return HttpResponse(response_json, content_type='application/json')


# return the size of cart for current user
def cart_size(request):
    cart_item = Cart.objects.filter(user_id=request.user)
    return len(cart_item)
