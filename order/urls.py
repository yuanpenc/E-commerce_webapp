from django.contrib import admin
from django.urls import path

from order import views

urlpatterns = [
    path('', views.showAllOrder),
    path('addOrder', views.createOrder),
    path('showOrderDetail', views.showOrderDetail),
    path('showAllOrder', views.showAllOrder),
    path('photo/<int:id>', views.get_photo_goods, name='photoDetail'),
]