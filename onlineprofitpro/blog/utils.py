# D:\Python\django\ONLINEPROFITPRO.RU\onlineprofitpro\blog\utils.py
import os
import uuid
from django.utils import timezone  # Import 'timezone' from 'django.utils' instead of 'datetime'

menu = [{'title': "Главная", 'url_name': 'home'},
        {'title': "О нас", 'url_name': 'about'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Гостевой пост", 'url_name': 'guest_post'},
        {'title': "Войти/", 'url_name': 'login'},
        {'title': "Зарегистрироваться", 'url_name': 'register'},
]


def get_media_file_path(instance, filename):
    post_slug = instance.post.slug
    ext = os.path.splitext(filename)[1]
    year_month = timezone.now().strftime('%Y/%m')
    random_str = str(uuid.uuid4().hex[:6])
    new_filename = f"{post_slug}_{random_str}{ext}"
    return os.path.join('post_media', year_month, new_filename)
