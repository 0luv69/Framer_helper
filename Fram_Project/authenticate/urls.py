from django.urls import path
from authenticate.views import *


urlpatterns = [
    path('activate/<emailtoken>',activate_email, name='activate_user'),

    path('login/',login_page, name='login_page'),
    path('logout/',logout_page, name='logout'),
    path('signup/',register, name='register'),
]
