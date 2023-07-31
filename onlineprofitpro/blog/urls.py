# D:\Python\django\ONLINEPROFITPRO.RU\onlineprofitpro\blog\urls.py


from django.urls import path, re_path, include
from blog.views import *


urlpatterns = [
    path('post/<slug:post_slug>/', post_detail, name='post_detail'),
    path('home/', index, name='home'),
    path('about/', about, name='about'),
]

