from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from information.forms import LoginForm, RegisterForm



def myinfo(request):
    # if request.method == 'GET':

    return render(request, 'information/myinfo.html', {})

def profile_page(request):
    return render(request, 'information/profile.html', {})


def login_action(request):
    context = {}

    if request.method == 'GET':
        context['login_form'] = LoginForm()
        context['register_form'] = RegisterForm()
        return render(request, 'eCommerce/login.html', context)

    # login page
    if request.POST.get("submit") == "Login":
        form = LoginForm(request.POST)
        context['form'] = form
        if not form.is_valid():
            context['error_msg_login'] = form.errors['__all__']
            context['login_form'] = LoginForm()
            context['register_form'] = RegisterForm()
            return render(request, 'eCommerce/login.html', context)

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
            return render(request, 'eCommerce/login.html', context)

        # At this point, the form data is valid.  Register and login the user.
        new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                            password=form.cleaned_data['password'],
                                            email=form.cleaned_data['email'])
        new_user.save()

        new_user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])

        login(request, new_user)
        return redirect(reverse('home'))
    else:
        return redirect(reverse('home'))


def logout_action(request):
    logout(request)
    return redirect(reverse('login'))


def register_action(request):
    context = {}
    if request.method == "GET":
        context['form'] = RegisterForm()
        return render(request, 'socialnetwork/register.html', context)
    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
    form = RegisterForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'socialnetwork/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('home'))