from django.contrib import admin
from django.urls import path
from eCommerce import views

urlpatterns = [
    path('', views.stream_action, name='home'),
    path('register', views.register_action, name='register'),
    path('login', views.login_action, name='login'),
    # path('item_detail', views.detail, name='item_detail'),
    # path('list_items', views.list, name='list_items'),
    path('profile', views.profile, name='profile'),
    path('myinfo', views.myinfo, name='myinfo'),
    path('cart', views.cart, name='cart'),
    # This path is for demo
    path('nav_list', views.stream_action, name='nav_list'),
# path('home', views.home_page),
    path('order', views.seller_profile, name='order'),
]
