
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import *

menu = [{'title': "Главная", 'url_name': 'home'},
        {'title': "О нас", 'url_name': 'about'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Блог", 'url_name': 'posts'},
]


def index(request):
    return HttpResponse("<h1>Главная</h1>")


def about(request):
    return HttpResponse("<h1>Обратная связь</h1>")

def post_detail(request, modelposts_slug):
    post = get_object_or_404(ModelPosts, slug=modelposts_slug)
    return render(request, 'blog/post.html', {'post': post})