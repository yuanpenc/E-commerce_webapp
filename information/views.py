from django.shortcuts import render

# Create your views here.


def myinfo(request):
    return render(request, 'information/myinfo.html', {})

def profile_page(request):
    return render(request, 'information/profile.html', {})