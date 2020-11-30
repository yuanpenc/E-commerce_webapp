from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse

from goods.models import Items
from information.forms import LoginForm, RegisterForm, EditProfileForm
from information.models import Profile, Cart

from order.views import createOrder
import json

from seller.views import createSeller, Seller

from seller.models import Seller

def logout_action(request):
    logout(request)
    return redirect(reverse('login'))

@login_required
def delete(request):
    itemId = request.GET.get('itemId')
    Cart.objects.filter(user=request.user.id).get(goods_id=int(itemId)).delete()
    return HttpResponse()


@login_required
def myinfo(request):
    if request.method == 'GET':

        form = EditProfileForm(instance=request.user.profile)
        profile = Profile.objects.get(user_id=request.user.id)
        if profile is None:
            pic = ''
            birthday = '01-01-1980'
            gender = 'male'
            address = "No specific address"
        else:
            pic = profile.picture
            birthday = profile.birthday
            gender = profile.gender
            address = profile.address
        context = {
            'my_profileForm': form,
            'pic': pic,
            'birthday': birthday,
            'gender': gender,
            'address': address,
            'cartNum': cart_size(request),
            'userId': request.user.id,
        }
        if Seller.objects.filter(user_id__exact = request.user.id):
            context['isSeller'] = True
        else:
            context['isSeller'] = False
        return render(request, 'information/myinfo.html', context)
    else:
        form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if not form.is_valid():
            pic = request.user.profile.picture
            birthday = request.user.profile.birthday
            gender = request.user.profile.gender
            address = request.user.profile.address
            context = {
                'my_profileForm': form,
                'pic': pic,
                'birthday': birthday,
                'gender': gender,
                'address': address,
                'cartNum': cart_size(request),
                'userId': request.user.id,
            }
            return render(request, 'information/myinfo.html', context)

        request.user.profile.birthday = form.cleaned_data['birthday']
        request.user.profile.gender = form.cleaned_data['gender']
        request.user.profile.address = form.cleaned_data['address']
        request.user.profile.picture = form.cleaned_data['picture']
        request.user.profile.content_type = form.cleaned_data['picture'].content_type
        request.user.profile.save()
        form.save()
        return redirect(reverse('myinfo'))


@login_required
def get_photo_goods(request, id):
    customer = get_object_or_404(Profile, id=id)
    # print('Picture #{} fetched from db: {} (type={})'.format(id, item.image, type(item.image)))

    # Maybe we don't need this check as form validation requires a picture be uploaded.
    # But someone could have delete the picture leaving the DB with a bad references.
    if not customer.picture:
        raise Http404

    return HttpResponse(customer.picture, content_type=customer.content_type)


def profile_page(request):
    context = {
        'userId':request.user.id
    }
    return render(request, 'information/profile.html', context)


def create_seller(request):
    createSeller(request)
    return render(request, 'seller/sellerProfile.html', {})



def create_order_pre_pay(request):
    total_price = request.GET.get("total_price")
    content = request.GET.get("content")
    if content is None:
        content = {}
    orderId = createOrder(request, content, float(total_price),"",request.user)
    response_json = json.dumps({'orderId': orderId, 'totalPrice': int(total_price)})
    return HttpResponse(response_json, content_type='application/json')


def pay_page(request):

    orderId = request.GET.get("orderId")
    total_price = request.GET.get("total_price")
    address = request.user.profile.address
    content = {
        'cartNum': len(Cart.objects.filter(user_id=request.user)),
        'orderId':orderId,
        'total_price':total_price,
        'address': address,
        'userId': request.user.id
    }
    return render(request, 'information/pay.html', content)



def cart_add(request):
    itemId = request.GET.get('itemId')
    cart_item = Cart.objects.filter(user_id=request.user)
    for item in cart_item:
        if int(item.goods_id) == int(itemId):
            return
    new_cart_item = Cart(user=request.user, goods=Items.objects.get(id=itemId))
    new_cart_item.save()

    return HttpResponse()


def cart_size(request):
    cart_item = Cart.objects.filter(user_id=request.user)
    return len(cart_item)


def cart_page(request):
    context = {}
    if request.method == 'GET':
        cart_item = Cart.objects.filter(user_id=request.user)
        context = {'cart_item': cart_item,
                   'cartNum': cart_size(request),
                   'isCart': True}
        return render(request, 'information/cart.html', context)


def login_action(request):
    context = {}

    if request.method == 'GET':
        context['login_form'] = LoginForm()
        context['register_form'] = RegisterForm()
        return render(request, 'information/login.html', context)

    # login page
    if request.POST.get("submit") == "Login":
        form = LoginForm(request.POST)
        context['form'] = form
        if not form.is_valid():
            context['error_msg_login'] = form.errors['__all__']
            context['login_form'] = LoginForm()
            context['register_form'] = RegisterForm()
            return render(request, 'information/login.html', context)

        # Persist a user id and a backend in the request.
        new_user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
        login(request, new_user)

        return redirect(reverse("home"))

    # registration page
    elif request.POST.get("submit") == "SignUp":
        form = RegisterForm(request.POST)
        context['form'] = form

        # Validates the form.
        if not form.is_valid():
            context['error_msg_register'] = "Parameters errors"
            context['login_form'] = LoginForm()
            context['register_form'] = RegisterForm()
            return render(request, 'information/login.html', context)

        # At this point, the form data is valid.  Register and login the user.
        new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                            password=form.cleaned_data['password'],
                                            email=form.cleaned_data['email'])
        new_user.save()

        new_user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])

        # createSeller(request, new_user)

        login(request, new_user)
        return redirect(reverse('home'))
    else:
        return redirect(reverse('home'))





def register_action(request):
    context = {}
    if request.method == "GET":
        context['form'] = RegisterForm()
        return render(request, 'information/register.html', context)
    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
    form = RegisterForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'information/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()
    #
    # print("Here!!!!!!!!!!!!!!!")
    #
    # createSeller(request, new_user)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('home'))

