from django.urls import path, include
from shophouse.views import *


urlpatterns = [
    path('',home, name='home'),
    path('short/<short_id>', short_request, name='short_request'),

    path('product/<slug>/',product_view, name='product'),


    path('cart/',cart, name='cart'),
    path('addcart/<product_slug>',add_cart, name='add_cart'),
    path('rmvcart/<product_slug>',rmv_cart, name='rmv_cart'),


    path('checkout/',checkout, name='checkout'),
    path('history/',history_view, name='history_view'),


    path('dashboard/',dashboard, name='dashboard'),
    path('upload/',product_upload, name='product_upload'),
    path('profile_change/',profile_change, name='profile_change'),



]
