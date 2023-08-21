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
    path('add_post_block/<slug:post_slug>/', views.add_post_block, name='add_post_block'),
    path('post/<slug:post_slug>/', views.post_detail, name='post_detail'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('addpage/', views.add_page, name='addpage'),
    path('login/', views.login, name='login'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('user_profile/<str:username>/', views.user_profile, name='user_profile'),
    path('category/<slug:category_slug>/', views.home, name='home_category'),
]
