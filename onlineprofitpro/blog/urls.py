# D:\Python\django\ONLINEPROFITPRO.RU\onlineprofitpro\blog\urls.py

from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),  # The base home view without filtering
    re_path(r'^home/(?:(?P<category_slug>[\w-]+)/)(?P<subcategory_slug>[\w-]+)/$', views.home, name='home'),
    re_path(r'^home/(?P<category_slug>[\w-]+)/$', views.home, name='home'),
    re_path(r'^home/$', views.home, name='home'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('guest_post/', views.guest_post, name='guest_post'),
    path('login/', views.login, name='login'),
    path('user_profile/<str:username>/', views.user_profile, name='user_profile'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),


]
