from django.urls import path, include
from .views import *


urlpatterns = [
    path('',home, name='home'),
    path('product/<slug>/',product_view, name='product'),
    path('login/',login_page, name='login_page'),
    path('signup/',register, name='register'),
]
