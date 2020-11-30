from django.urls import path
from information import views

urlpatterns = [
    path('', views.myinfo, name='home'),
    path('register', views.register_action, name='register'),
    path('login', views.login_action, name='login'),
    path('profile', views.profile_page, name='profile'),
    path('myinfo', views.myinfo, name='myinfo'),
    path('cart', views.cart_page, name='cart'),
    path('photo/<int:id>', views.get_photo_goods, name='photoProfile'),
    path('logout', views.logout_action, name='logout'),
    path('addToCart', views.cart_add, name='addToCart'),
    path('pay', views.pay_page, name='pay'),
    path('create', views.create_order_pre_pay, name='create'),
    # path('create_seller', views.create_seller, name='create_seller'),
    path('delete_item_in_cart', views.delete, name='delete_item_in_cart')

]
