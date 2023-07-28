from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import AdminTextareaWidget
from django.forms import RadioSelect
from django.utils.html import format_html
from .models import ModelCategories, ModelSubcategories, ModelCssClass, ModelPosts, ModelPostContent, Rating
from django.utils.safestring import mark_safe
from .admin_forms import ModelPostContentAdminForm

class CssClassRadioSelect(forms.RadioSelect):
    template_name = 'admin/widgets/radio_inline.html'  # Path to the custom template


# Define the inline for ModelPostContent
class ModelPostContentInline(admin.TabularInline):
    model = ModelPostContent
    extra = 1

# Register the ModelCategories model
class ModelCategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(ModelCategories, ModelCategoriesAdmin)

# Register the ModelSubcategories model
class ModelSubcategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(ModelSubcategories, ModelSubcategoriesAdmin)

# Register the ModelCssClass model
class ModelCssClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'css_class', 'icon')
    prepopulated_fields = {'css_class': ('name',)}

admin.site.register(ModelCssClass, ModelCssClassAdmin)

# Register the ModelPosts model
class ModelPostsAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'time_create', 'is_published', 'subcat')
    list_filter = ('is_published', 'subcat')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModelPostContentInline]

admin.site.register(ModelPosts, ModelPostsAdmin)

# Register the Rating model
class RatingAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'value')

admin.site.register(Rating, RatingAdmin)


# class ModelPostContentAdmin(admin.ModelAdmin):
#     form = ModelPostContentAdminForm  # Use the custom form
#     list_display = ('post', 'content_text', 'text_css_class', 'media_file', 'media_css_class')
#     list_filter = ('post', 'text_css_class', 'media_css_class')
#     search_fields = ('content_text',)
#
# admin.site.register(ModelPostContent, ModelPostContentAdmin)

# Register the ModelPostContent model with the custom admin class and form
class ModelPostContentAdmin(admin.ModelAdmin):
    form = ModelPostContentAdminForm
    list_display = ('post', 'content_text', 'text_css_class', 'get_media_file_thumbnail', 'media_css_class')
    list_filter = ('post', 'text_css_class', 'media_css_class')
    search_fields = ('content_text',)

    def get_media_file_thumbnail(self, obj):
        if obj.media_file:
            return mark_safe(f'<img src="{obj.media_file.url}" style="max-height: 100px; max-width: 100px;" />')
        return None

    get_media_file_thumbnail.short_description = 'Media File Thumbnail'

admin.site.register(ModelPostContent, ModelPostContentAdmin)