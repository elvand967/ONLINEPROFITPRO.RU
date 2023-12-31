
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from .utils import *
from .utils import extract_youtube_id

class ModelCategories(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']


class ModelSubcategories(models.Model):
    category = models.ForeignKey(ModelCategories, on_delete=models.CASCADE, related_name='subcategories', verbose_name="Категория")
    name = models.CharField(max_length=100, db_index=True, verbose_name="Подкатегория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return f"{self.category} - {self.name}"

    def get_absolute_url(self):
        return reverse('subcategory', kwargs={'cat_slug': self.category.slug, 'subcat_slug': self.slug})

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        ordering = ['id']


class ModelPosts(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    subcat = models.ForeignKey('ModelSubcategories', on_delete=models.PROTECT, verbose_name="ПодКатегории")
    # User information
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Author"
    )


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'  # уточнить названия
        ordering = ['-time_create', 'title']  # сортировка по дате убывания


class ModelCssClass(models.Model):
    CSS_TYPE_CHOICES = (
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('code', 'Code'),
        ('youtube', 'YouTube'),
        ('audio', 'Audio'),
        ('media', 'Media'),
        # Add more choices if needed for different types
    )
    css_type = models.CharField(
        max_length=10,
        choices=CSS_TYPE_CHOICES,
        default='text',
        verbose_name="CSS Class Type"
    )
    name_css_class = models.CharField(max_length=50, verbose_name="Класс CSS (название)", default='')
    description = models.TextField(verbose_name="Описание")
    class_css = models.CharField(max_length=50, verbose_name="CSS Class", default='')
    class_css_code = models.TextField(verbose_name="Код Class-CSS")
    icon = models.CharField(max_length=100, blank=True, null=True, verbose_name="Icon URL")

    def __str__(self):
        return self.name_css_class

    class Meta:
        verbose_name = "CSS Class"
        verbose_name_plural = "CSS Classes"


class ModelPostContent(models.Model):
    post = models.ForeignKey(ModelPosts, on_delete=models.CASCADE, related_name='content_parts')
    content_text = models.TextField(blank=True, null=True, verbose_name="Post Text Part")
    css_text = models.ForeignKey(
        ModelCssClass,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='text_content',
        verbose_name="CSS Class for Text"
    )
    image_file = models.FileField(upload_to=get_image_file_path, blank=True, null=True, verbose_name="Post Image Part")
    css_image = models.ForeignKey(
        ModelCssClass,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='image_content',
        verbose_name="CSS Class for Image"
    )
    media_file = models.FileField(upload_to=get_media_file_path, blank=True, null=True, verbose_name="Post Media Part")
    css_media = models.ForeignKey(
        ModelCssClass,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='media_content',
        verbose_name="CSS Class for Media"
    )
    youtube_video = models.URLField(blank=True, null=True, verbose_name="YouTube Video URL")
    css_youtube = models.ForeignKey(
        ModelCssClass,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='youtube_content',
        verbose_name="CSS Class for YouTube Video"
    )
    code = models.TextField(blank=True, null=True, verbose_name="Code")
    css_code = models.ForeignKey(
        ModelCssClass,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='code_content',
        verbose_name="CSS Class for Code"
    )


    def __str__(self):
        return f"{self.post} - Part{self.pk}"

    def save(self, *args, **kwargs):
        if self.youtube_video:
            youtube_id = extract_youtube_id(self.youtube_video)
            if youtube_id:
                self.youtube_video = f"https://www.youtube.com/embed/{youtube_id}"

        super().save(*args, **kwargs)

    def get_text_css_class(self):
        return self.css_text.name_css_class if self.css_text else ""

    def get_image_css_class(self):
        return self.css_image.name_css_class if self.css_image else ""

    def get_media_css_class(self):
        return self.css_media.name_css_class if self.css_media else ""

    def get_youtube_css_class(self):
        return self.css_youtube.name_css_class if self.css_youtube else ""

    def get_code_css_class(self):
        return self.css_code.name_css_class if self.css_code else ""


class ModelComments(models.Model):  # Комментарии к посту
    post = models.ForeignKey(ModelPosts, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    comment_text = models.TextField(blank=True, verbose_name="Текст коментария")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.post.title}"


class Rating(models.Model):
    post = models.ForeignKey(ModelPosts, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])

    def __str__(self):
        return f"Rating by {self.user} on {self.post.title}"

