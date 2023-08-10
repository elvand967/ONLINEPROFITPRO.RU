# D:\Python\django\ONLINEPROFITPRO.RU\onlineprofitpro\blog\views.py


from .forms import AddPostForm, PostContentFormset, PostContentForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import *


def contact(request):
    context = {
        'title': 'Контакт',
        'page_content': 'Это о содержании страницы "Обратная связь".',
    }
    return render(request, 'blog/contact.html', context)


def about(request):
    context = {
        'title': 'О сайте',
        'page_content': 'Это о содержании страницы "О сайте".',
    }
    return render(request, 'blog/about.html', context)


def add_page(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        formset = PostContentFormset(request.POST, request.FILES, prefix='content')

        if form.is_valid() and formset.is_valid():
            post = form.save()
            for sub_form in formset:
                content_part = sub_form.save(commit=False)
                content_part.post = post
                content_part.save()

            if 'add_block_button' in request.POST:
                return redirect('add_post_block', post.slug)
            else:
                return redirect('home')  # Redirect to home page after successful submission

    else:
        form = AddPostForm()
        formset = PostContentFormset(prefix='content')

    return render(request, 'blog/addpage.html', {'title': 'Добавить "Гостевой" пост', 'form': form, 'formset': formset})


def add_post_block(request, post_slug):
    post = get_object_or_404(ModelPosts, slug=post_slug)

    if request.method == 'POST':
        post_content_form = PostContentForm(request.POST, request.FILES)
        if post_content_form.is_valid():
            post_content = post_content_form.save(commit=False)
            post_content.post = post
            post_content.save()

            if 'add_post_block' in request.POST:
                return redirect('add_post_block', post_slug=post_slug)
            elif 'submit' in request.POST:
                return redirect('home')
    else:
        post_content_form = PostContentForm()

    return render(request, 'blog/addpostblock.html', {'post': post, 'post_content_form': post_content_form})


def login(request):
    return HttpResponse("<h1>login</h1>")


def user_profile(request, username):
    return HttpResponse(f"<h1>User profile for {username}</h1>")


def register(request):
    context = {
        'title': 'Регистрация',
        'page_content': 'Это о содержании страницы "Регистрация".',
    }
    return render(request, 'blog/register.html', context)


def home(request, category_slug=None, subcategory_slug=None):
    # Get all posts sorted in reverse order of update date
    posts = ModelPosts.objects.filter(is_published=True).order_by('-time_update')

    # Filter posts based on the selected category and subcategory
    if category_slug:
        selected_category = get_object_or_404(ModelCategories, slug=category_slug)
        posts = posts.filter(subcat__category=selected_category)

        if subcategory_slug:
            selected_subcategory = get_object_or_404(ModelSubcategories, slug=subcategory_slug, category=selected_category)
            posts = posts.filter(subcat=selected_subcategory)
        else:
            selected_subcategory = None
    else:
        selected_category = None
        selected_subcategory = None

    # Create a list to store the first part of each post with its picture
    post_previews = []
    for post in posts:
        # Get the first content part of the post
        first_part = post.content_parts.first()
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
        'selected_category': selected_category,
        'selected_subcategory': selected_subcategory,
        'title': selected_subcategory.name if selected_subcategory else (selected_category.name if selected_category else "Elvand"),
    }

    return render(request, 'blog/home.html', context)




# def home(request, category_slug=None, subcategory_slug=None):
#     # Get all posts sorted in reverse order of update date
#     posts = ModelPosts.objects.filter(is_published=True).order_by('-time_update')
#
#     # Filter posts based on the selected category and subcategory
#     if category_slug:
#         selected_category = get_object_or_404(ModelCategories, slug=category_slug)
#         posts = posts.filter(subcat__category=selected_category)
#
#         if subcategory_slug:
#             selected_subcategory = get_object_or_404(ModelSubcategories, slug=subcategory_slug, category=selected_category)
#             posts = posts.filter(subcat=selected_subcategory)
#             title = selected_subcategory.name
#         else:
#             selected_subcategory = None
#             title = selected_category.name
#     else:
#         selected_category = None
#         selected_subcategory = None
#         title = "Elvand"
#
#     # Create a list to store the first part of each post with its picture
#     post_previews = []
#     for post in posts:
#         # Get the first content part of the post
#         first_part = ModelPostContent.objects.filter(post=post).first()
#         if first_part:
#             # Append the first part of the post along with the CSS classes to the list
#             post_previews.append({
#                 'post': post,
#                 'content_text': first_part.content_text,
#                 'css_text_class': first_part.css_text.class_css if first_part.css_text else '',
#                 'media_file': first_part.media_file,
#                 'css_media_class': first_part.css_media.class_css if first_part.css_media else '',
#             })
#
#     # Pass the data to the template
#     context = {
#         'post_previews': post_previews,
#         'title': title,
#     }
#
#     return render(request, 'blog/home.html', context)


# def post_detail(request, slug):
#     post = get_object_or_404(ModelPosts, slug=slug)
#     return render(request, 'blog/post_detail.html', {'post': post})
def post_detail(request, post_slug):
    post = get_object_or_404(ModelPosts, slug=post_slug, is_published=True)
    return render(request, 'blog/post_detail.html', {'post': post})
