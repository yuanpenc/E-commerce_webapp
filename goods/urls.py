from django.contrib import admin
from django.urls import path
from goods import views

urlpatterns = [
    path('item_detail', views.detail, name='item_detail'),
    path('list_items', views.list_items, name='list_items'),
    path('photo/<int:id>', views.get_photo, name='photo'),
]
