from django.contrib import admin
from django.urls import path

from order import views

urlpatterns = [
    path('', views.makeOrder),
]