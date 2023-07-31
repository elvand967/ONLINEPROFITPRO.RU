# D:\Python\django\ONLINEPROFITPRO.RU\onlineprofitpro\blog\urls.py


from django.urls import path, re_path, include
from blog.views import *
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('home/', index, name='home'),
    path('about/', about, name='about'),
]

