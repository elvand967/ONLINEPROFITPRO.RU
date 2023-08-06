# D:\Python\django\ONLINEPROFITPRO.RU\onlineprofitpro\blog\utils.py
import os
import uuid
from django.utils import timezone  # Import 'timezone' from 'django.utils' instead of 'datetime'




def get_media_file_path(instance, filename):
    post_slug = instance.post.slug
    ext = os.path.splitext(filename)[1]
    year_month = timezone.now().strftime('%Y/%m')
    random_str = str(uuid.uuid4().hex[:6])
    new_filename = f"{post_slug}_{random_str}{ext}"
    return os.path.join('post_media', year_month, new_filename)
