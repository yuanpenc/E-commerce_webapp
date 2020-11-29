from django.contrib import admin
from django.urls import path

from order import views

urlpatterns = [
    path('', views.addOrder),
    path('addOrder', views.addOrder),
    path('showOrder', views.showOrder),
]