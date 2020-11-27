from django.contrib import admin
from django.urls import path
from seller import views

urlpatterns = [
    path('', views.sellerinfo),
    path('sellerinfo', views.sellerinfo, name='sellerinfo'),
    path('sellersetting', views.sellersetting, name='sellersetting'),
    path('addItems', views.addItems, name='addItems'),


]