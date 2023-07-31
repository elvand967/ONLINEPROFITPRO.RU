
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("<h1>Главная</h1>")


def about(request):
    return HttpResponse("<h1>Обратная связь</h1>")
