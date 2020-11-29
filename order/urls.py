from django.contrib import admin
from django.urls import path

from order import views

urlpatterns = [
    path('', views.showOrder),
    path('addOrder', views.createOrder),
    path('showOrder', views.showOrder),
    path('showAllOrder', views.showAllOrder),
    path('photo/<int:id>', views.get_photo_goods, name='photoDetail'),
]