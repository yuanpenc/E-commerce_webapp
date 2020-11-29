import datetime

from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from goods.models import Items
import json

# Create your views here.


# def makeOrder(request):
#     context = {}
#     if request.method == 'GET':
#         itemId = request.GET.get('itemId', default=1)
#         item = Items.objects.get(id=itemId)
#         seller = item.created_by
#         number = 1
#         context['item'] = item
#         context['seller'] = seller
#         context['number'] = number
#         return render(request, 'order/orderPage.html', context)
#
#     return render(request, 'order/orderPage.html', {})
from order.forms import OrderForm
from order.models import Order


# def showOrder(request):
#     orderid = 7
#     order = Order.objects.get(id=orderid)
#     asd = order.content
#     print(asd)
#     print("-0-0--0-0--0-")
#     desc = json.loads(asd)
#     for i in desc.keys():
#         print(i)
#         print(desc[i])
#     context = {}
#     return render(request, 'order/showOrderDetail.html', context)

def showOrderDetail(request, orderid=7):
    context = {}
    # orderid = 7
    # !!!!!!!!!!!
    orderid = request.GET.get('orderid')
    order = Order.objects.get(orderid=orderid)
    list = json.loads(order.content)
    order_item = []
    for i in list.keys():
        item = {}
        item['item'] = Items.objects.get(id=i)
        item['quantity'] = list.get(i)
        item['price'] = item['item'].price * item['quantity']
        order_item.append(item)
    context['order_item'] = order_item
    context['order'] = order
    confirmOrder(request)
    return render(request, 'order/showOrderDetail.html', context)


def showAllOrder(request):
    context = {}
    # !!!!!
    # order = Order.objects.all().filter(user=user)
    order = Order.objects.all().filter(comment="asdsad")
    print(order.count())
    context['order_list'] = order
    context['isOrder'] = True
    return render(request, 'order/showAllOrder.html', context)


def confirmOrder(request, orderid=7):
    order = Order.objects.get(id=orderid)
    order.status = 1
    order.save()
    return


## list['itemId'] = quantity
## content = json.dumps(list)
# content: 对应商品和数量
# total_price: 对应总价
# comment: 订单评论
# user: 总的user
def createOrder(request, content, total_price, comment, user):
    new_order = Order(
        # !!!!!!!!!!!!
        customer=user,
        orderid=str(datetime.datetime.utcnow().timestamp()).replace(".", ""),
        content=content,
        total_price=total_price,
        comment=comment)
    new_order.save()
    return new_order.orderid


def get_photo_goods(request, id):
    item = get_object_or_404(Items, id=id)
    # print('Picture #{} fetched from db: {} (type={})'.format(id, item.image, type(item.image)))

    # Maybe we don't need this check as form validation requires a picture be uploaded.
    # But someone could have delete the picture leaving the DB with a bad references.
    if not item.image:
        raise Http404

    return HttpResponse(item.image, content_type=item.content_type)
