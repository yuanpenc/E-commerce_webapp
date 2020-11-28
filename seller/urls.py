from django.contrib import admin
from django.urls import path
from seller import views

urlpatterns = [
    path('', views.sellerProfile),
    path('sellerinfo', views.sellerProfile, name='sellerinfo'),
    path('sellerSetting', views.sellerSetting, name='sellerSetting'),
    path('addItems', views.addItems, name='addItems'),
    path('itemDetail', views.sellerItemDetail, name='sellerItems'),
    path('photo/<int:id>', views.get_photo, name='photoDetail'),
]