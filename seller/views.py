from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from seller.forms import *

@login_required
def sellerProfile(request):
    context = {}
    sellerId = request.GET.get('userId')
    seller = Seller.objects.get(user_id=sellerId)
    items = Items.objects.all().filter(created_by=sellerId)
    context['items'] = items
    context['sellerId'] = sellerId
    context['seller'] = seller
    return render(request, 'seller/sellerProfile.html', context)

@login_required
def createSeller(request):
    userId = request.GET.get('userId')
    user = User.objects.get(id=userId)
    new_Seller = Seller(user=user,
                        name=user.username)
    new_Seller.save()
    return sellerProfile(request)

@login_required
def get_photo_goods(request, id):
    seller = get_object_or_404(Seller, id=id)
    # print('Picture #{} fetched from db: {} (type={})'.format(id, item.image, type(item.image)))

    # Maybe we don't need this check as form validation requires a picture be uploaded.
    # But someone could have delete the picture leaving the DB with a bad references.
    if not seller.image:
        raise Http404

    return HttpResponse(seller.image, content_type=seller.image_content_type)

@login_required
def sellerSetting(request):
    context = {}
    sellerId = request.GET.get('sellerId')
    seller = Seller.objects.get(id = sellerId)
    if request.method == 'GET':
        context['sellerId'] = sellerId
        context['seller'] = seller
        context['form'] = SellerForm(instance=seller)
        return render(request, 'seller/sellerSetting.html', context)

    form = SellerForm(request.POST, request.FILES)

    if not form.is_valid():
        context['form'] = form
        context['sellerId'] = sellerId
        return render(request, 'seller/sellerSetting.html', context)

    image = form.cleaned_data['image']
    if image is None:
        seller.image = seller.image
        seller.image_content_type = seller.image_content_type
    else:
        seller.image_content_type = form.cleaned_data['image'].content_type
        seller.image = image

    qrcode = form.cleaned_data['qrcode']
    if qrcode is None:
        seller.qrcode = seller.qrcode
        seller.qrcode_content_type = seller.qrcode_content_type
    else:
        seller.qrcode_content_type = form.cleaned_data['qrcode'].content_type
        seller.qrcode = qrcode

    seller.name = form.cleaned_data['name']
    seller.address = form.cleaned_data['address']
    seller.zip = form.cleaned_data['zip']
    seller.desc = form.cleaned_data['desc']
    seller.save()

    context['sellerId'] = sellerId
    context['seller'] = seller
    context['form'] = SellerForm(instance=Seller.objects.get(id=sellerId))
    return render(request, 'seller/sellerSetting.html', context)

@login_required
def addItems(request):
    context = {}
    sellerId = request.GET.get('sellerId')
    seller = Seller.objects.get(id = sellerId)
    if request.method == 'GET':
        context['sellerId'] = sellerId
        context['form'] = ItemForm()
        context['seller'] = seller
        return render(request, 'seller/addItem.html', context)

    form = ItemForm(request.POST, request.FILES)
    if not form.is_valid():
        context['form'] = form
        context['sellerId'] = sellerId
        seller = Seller.objects.get(id=sellerId)
        context['seller'] = seller
        return render(request, 'seller/addItem.html', context)

    new_item = Items(name=form.cleaned_data['name'],
                 desc=form.cleaned_data['desc'],
                 price=form.cleaned_data['price'],
                 unit=form.cleaned_data['unit'],
                 stocks=form.cleaned_data['stocks'],
                 sales=0,
                 detail=form.cleaned_data['detail'],
                 image=form.cleaned_data['image'],
                 status=1,
                 created_by=Seller.objects.get(id=sellerId),
                 category=form.cleaned_data['category'])
    print(form.cleaned_data['name'])
    print('Uploaded picture: {} (type={})'.format(form.cleaned_data['image'], type(form.cleaned_data['image'])))


    new_item.content_type = form.cleaned_data['image'].content_type
    new_item.save()

    context = {}
    seller = Seller.objects.get(user=request.user.id)
    items = Items.objects.all().filter(created_by=sellerId)
    context['items'] = items
    context['sellerId'] = sellerId
    context['seller'] = seller
    return render(request, 'seller/sellerProfile.html', context)



@login_required
def deleteItems(request):
    itemId = request.GET.get('itemId')
    item = get_object_or_404(Items, id=itemId)
    item.image.delete()
    item.delete()
    return sellerProfile(request)


@login_required
def sellerItemDetail(request):
    context = {}
    itemId = request.GET.get('itemId')
    item = Items.objects.get(id=itemId)
    sellerId = item.created_by_id
    if request.method == 'GET':
        # form = ItemDetailForm(initial={'name': item.name, 'desc': item.desc, 'price': item.price,
        #                                'unit': item.unit, 'stocks': item.stocks, 'sales': item.sales,
        #                                'detail': item.detail, 'image': item.image, 'status': item.status,
        #                                'category': item.category})
        form = ItemDetailForm(instance=Items.objects.get(id=itemId))
        context['form'] = form
        context['itemId'] = itemId
        context['sellerId'] = sellerId
        seller = Seller.objects.get(id=sellerId)
        context['seller'] = seller
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
    seller = Seller.objects.get(id=sellerId)
    context['seller'] = seller
    return render(request, 'seller/itemDetail.html', context)
