from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from seller.forms import *


def sellerinfo(request):
    context = {}
    items = Items.objects.all().filter(created_by=1)
    context['items'] = items
    return render(request, 'seller/sellerinfo.html', context)


def get_photo(request, id):
    item = get_object_or_404(Items, id=id)
    # print('Picture #{} fetched from db: {} (type={})'.format(id, item.image, type(item.image)))

    # Maybe we don't need this check as form validation requires a picture be uploaded.
    # But someone could have delete the picture leaving the DB with a bad references.
    if not item.image:
        raise Http404

    return HttpResponse(item.image, content_type=item.content_type)


def sellersetting(request):
    context = {}
    sellerId = request.GET.get('sellerId', default='1')
    seller = Seller.objects.get(id = sellerId)
    if request.method == 'GET':
        context['form'] = SellerForm()
        return render(request, 'seller/sellersetting.html', context)

    form = SellerForm(request.POST, request.FILES)

    return render(request, 'seller/sellerinfo.html', {})


def addItems(request):
    context = {}
    if request.method == 'GET':
        context['form'] = ItemForm()
        return render(request, 'seller/addItem.html', context)

    return render(request, 'seller/addItem.html', {})


def sellerItemDetail(request):
    context = {}
    itemId = request.GET.get('itemId', default='1')
    item = Items.objects.get(id=itemId)

    if request.method == 'GET':
        # form = ItemDetailForm(initial={'name': item.name, 'desc': item.desc, 'price': item.price,
        #                                'unit': item.unit, 'stocks': item.stocks, 'sales': item.sales,
        #                                'detail': item.detail, 'image': item.image, 'status': item.status,
        #                                'category': item.category})
        form = ItemDetailForm(instance=Items.objects.get(id=itemId))
        context['form'] = form
        context['itemId'] = itemId
        return render(request, 'seller/itemDetail.html', context)

    form = ItemDetailForm(request.POST, request.FILES)

    if not form.is_valid():
        context = {'form': form, 'itemId': itemId}
        return render(request, 'seller/itemDetail.html', context)

    image = form.cleaned_data['image']

    if image is None:
        item.content_type = item.content_type
        item.image = item.image
    else:
        item.content_type = form.cleaned_data['image'].content_type
        item.image = image

    item.name = form.cleaned_data['name']
    item.desc = form.cleaned_data['desc']
    item.price = form.cleaned_data['price']
    item.unit = form.cleaned_data['unit']
    item.stocks = form.cleaned_data['stocks']
    item.sales = form.cleaned_data['sales']
    item.detail = form.cleaned_data['detail']
    item.status = form.cleaned_data['status']
    item.category = form.cleaned_data['category']
    item.save()

    context = {'itemId': itemId,
               'form': ItemDetailForm(instance=Items.objects.get(id=itemId))}
    return render(request, 'seller/itemDetail.html', context)
