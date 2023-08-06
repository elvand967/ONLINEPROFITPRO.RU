# D:\Python\django\ONLINEPROFITPRO.RU\onlineprofitpro\blog\views.py

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import *


def contact(request):
    return HttpResponse("<h1>Обратная связь</h1>")


def about(request):
    return HttpResponse("<h1>О сайте</h1>")


def guest_post(request):
    return HttpResponse("<h1>Гостевой пост</h1>")


def login(request):
    return HttpResponse("<h1>login</h1>")


def user_profile(request, username):
    return HttpResponse(f"<h1>User profile for {username}</h1>")


def register(request):
    return HttpResponse("<h1>Регистрация</h1>")


def home(request, category_slug=None, subcategory_slug=None):
    # Get all posts sorted in reverse order of update date
    posts = ModelPosts.objects.filter(is_published=True).order_by('-time_update')


    if category_slug:
        selected_category = get_object_or_404(ModelCategories, slug=category_slug)
        posts = posts.filter(subcat__category=selected_category)

        if subcategory_slug:
            selected_subcategory = get_object_or_404(ModelSubcategories, slug=subcategory_slug, category=selected_category)
            posts = posts.filter(subcat=selected_subcategory)

    # Create a list to store the first part of each post with its picture
    post_previews = []
    for post in posts:
        # Get the first content part of the post
        first_part = ModelPostContent.objects.filter(post=post).first()
        if first_part:
            # Append the first part of the post along with the CSS classes to the list
            post_previews.append({
                'post': post,
                'content_text': first_part.content_text,
                'css_text_class': first_part.css_text.class_css if first_part.css_text else '',
                'media_file': first_part.media_file,
                'css_media_class': first_part.css_media.class_css if first_part.css_media else '',
            })

    # Pass the data to the template
    context = {
        'post_previews': post_previews,
        'title': "Главная страница",  # Set the desired title for the home page
    }

    return render(request, 'blog/home.html', context)




def post_detail(request, slug):
    post = get_object_or_404(ModelPosts, slug=slug)
    return render(request, 'blog/post_detail.html', {'post': post})

