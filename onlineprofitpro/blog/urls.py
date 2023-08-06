# D:\Python\django\ONLINEPROFITPRO.RU\onlineprofitpro\blog\urls.py

from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views
from . import views
from blog.views import *


urlpatterns = [
    path('', home, name='home'),
    path('post/<slug:slug>/', post_detail, name='post_detail'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('guest_post/', guest_post, name='guest_post'),
    path('login/', login, name='login'),
    path('user_profile/<str:username>/', user_profile, name='user_profile'),
    path('register/', register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    re_path(r'^(?:(?P<category_slug>[\w-]+)/)?(?P<subcategory_slug>[\w-]+)?/$', home, name='home'),
]
