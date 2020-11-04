from django.contrib import admin
from django.urls import path
from eCommerce import views

urlpatterns = [
    path('', views.stream_action, name='home'),
    path('register', views.register_action, name='register'),
    path('login', views.login_action, name='login'),
    path('listItem', views.list_items, name='listItem'),
    path('itemDetail', views.item_detail, name='itemDetail')
]
