from django.contrib import admin
from django.urls import path
from information import views
from goods import views as g_views

urlpatterns = [
    path('', views.myinfo, name='home'),
    path('register', views.register_action, name='register'),
    path('login', views.login_action, name='login'),
    path('profile', views.profile_page, name='profile'),
    path('myinfo', views.myinfo, name='myinfo'),
    path('cart', views.cart_page, name='cart'),
    path('photo/<int:id>', g_views.get_photo, name='photo'),
    path('logout', views.logout, name='logout'),
    path('addToCart', views.cart_add, name='addToCart'),
    path('pay', views.pay_page, name='pay'),

]
