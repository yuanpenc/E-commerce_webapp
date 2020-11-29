from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from goods.models import Items


# Create your views here.


def makeOrder(request):
    context = {}
    if request.method == 'GET':
        itemId = request.GET.get('itemId', default=1)
        item = Items.objects.get(id=itemId)
        seller = item.created_by
        number = 1
        context['item'] = item
        context['seller'] = seller
        context['number'] = number
        return render(request, 'order/orderPage.html', context)

    return render(request, 'order/orderPage.html', {})


def get_photo_goods(request, id):
    item = get_object_or_404(Items, id=id)
    # print('Picture #{} fetched from db: {} (type={})'.format(id, item.image, type(item.image)))

    # Maybe we don't need this check as form validation requires a picture be uploaded.
    # But someone could have delete the picture leaving the DB with a bad references.
    if not item.image:
        raise Http404

    return HttpResponse(item.image, content_type=item.content_type)
