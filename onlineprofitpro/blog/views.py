# D:\Python\django\ONLINEPROFITPRO.RU\onlineprofitpro\blog\views.py



from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from django.views.generic import ListView

from .forms import AddPostForm, PostContentFormset, PostContentForm, RegisterUserForm

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.utils.text import slugify
from unidecode import unidecode

from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm

def slug_conversion(title):
    # Transliterate the title to ASCII characters
    ascii_title = unidecode(title)

    # Generate the initial slug from the transliterated title
    base_slug = slugify(ascii_title)

    # Check for existing slugs in the database
    existing_slugs = ModelPosts.objects.filter(slug__startswith=base_slug).values_list('slug', flat=True)

    # Find a unique slug by adding a number to the base slug
    counter = 1
    while True:
        new_slug = base_slug
        if new_slug in existing_slugs:
            new_slug = f"{base_slug}-{counter}"
            counter += 1
        else:
            break

    return new_slug


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


@login_required
def add_page(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        formset = PostContentFormset(request.POST, request.FILES, prefix='content')

        if form.is_valid() and formset.is_valid():
            title = form.cleaned_data['title']
            slug = slug_conversion(title)

            # Create the post instance with the generated slug and other fields
            post = form.save(commit=False)
            post.slug = slug
            post.user_first_name = request.user.first_name
            post.user_last_name = request.user.last_name
            post.user_username = request.user.username
            post.save()

            for sub_form in formset:
                content_part = sub_form.save(commit=False)
                content_part.post = post
                content_part.save()

            if 'add_block_button' in request.POST:
                return redirect('add_post_block', post_slug=slug)
            else:
                return redirect('home')

    else:
        form = AddPostForm()
        formset = PostContentFormset(prefix='content')

    # Determine the author display name
    user = request.user
    author_display_name = user.get_full_name() or user.username

    return render(request, 'blog/addpage.html', {'title': 'Add "Guest" Post', 'form': form, 'formset': formset, 'author_display_name': author_display_name})


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


class RegisterUser(FormView):
    form_class = RegisterUserForm
    template_name = 'blog/register.html'
    success_url = reverse_lazy('home')  # в дальнейшем доработать выход на страницу профиля

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)



# from django.urls import reverse_lazy
# from django.views.generic.edit import FormView
# from django.contrib.auth.forms import UserCreationForm
# from .models import CustomUser  # Замените на вашу модель пользователя, если используется другая
#
# class RegisterUser(FormView):
#     form_class = UserCreationForm  # Используем стандартную форму создания пользователя
#     template_name = 'register.html'
#     success_url = reverse_lazy('home')  # Или другой URL, куда перенаправлять после успешной регистрации
#
#     def form_valid(self, form):
#         # Создаем нового пользователя, используя данные из формы
#         user = form.save()
#
#         # Дополнительные действия, если необходимо
#         # Например, присвоение дополнительных полей вашей модели пользователя
#         custom_user = CustomUser.objects.create(user=user, additional_field='value')
#
#         # Дополнительные действия, если необходимо
#         # Например, отправка подтверждения на почту
#         # ...
#
#         return super().form_valid(form)



def home(request, category_slug=None, subcategory_slug=None):
    # Get all posts sorted in reverse order of update date
    posts = ModelPosts.objects.filter(is_published=True).order_by('-time_update')

    # Filter posts based on the selected category and subcategory
    if category_slug:
        selected_category = get_object_or_404(ModelCategories, slug=category_slug)
        posts = posts.filter(subcat__category=selected_category)

        if subcategory_slug:
            selected_subcategory = get_object_or_404(ModelSubcategories, slug=subcategory_slug,
                                                     category=selected_category)
            posts = posts.filter(subcat=selected_subcategory)
            selected_category = selected_subcategory.category  # Update selected_category to subcategory's category
        else:
            selected_subcategory = None
    else:
        selected_category = None
        selected_subcategory = None

    # Create a list to store post previews including author information
    post_previews = []
    for post in posts:
        first_part = post.content_parts.first()
        if first_part:
            if first_part.css_image.class_css == "img-large":
                css_image_style = "float: left; max-width: 120px;"
            else:
                css_image_style = "max-width: 120px;"

            post_previews.append({
                'post': post,
                'content_text': truncatewords_html(first_part.content_text, 50),
                'css_text_class': first_part.css_text.class_css if first_part.css_text else '',
                'image_file': first_part.image_file,
                'css_image_class': first_part.css_image.class_css if first_part.css_image else '',
                'css_image_style': css_image_style,
                'user': post.user,  # Add the user attribute for the post preview
            })

    context = {
        'post_previews': post_previews,
        'selected_category': selected_category,
        'selected_subcategory': selected_subcategory,
        'title': selected_subcategory.name if selected_subcategory else (
            selected_category.name if selected_category else "Elvand"),
    }

    return render(request, 'blog/home.html', context)


def post_detail(request, post_slug):
    post = get_object_or_404(ModelPosts, slug=post_slug, is_published=True)
    return render(request, 'blog/post_detail.html', {'post': post})



