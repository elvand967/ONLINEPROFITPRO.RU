# D:\Python\django\ONLINEPROFITPRO.RU\onlineprofitpro\blog\urls.py


from django.urls import path, re_path, include
from blog.views import *
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('guest_post/', guest_post, name='guest_post'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
]

