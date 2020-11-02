from django.contrib import admin
from django.urls import path
from eCommerce import views

urlpatterns = [
    path('', views.stream_action, name='home'),
    path('register', views.register_action, name='register'),
    path('login', views.login_action, name='login'),
    path('home', views.home_page),
    path('seller', views.seller_profile, name='seller'),
]
