from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import AdminTextareaWidget
from django import forms
from .models import ModelPostContent, ModelCssClass




from django.forms import RadioSelect
from django.utils.html import format_html
from .models import ModelCategories, ModelSubcategories, ModelCssClass, ModelPosts, ModelPostContent, Rating
from django.utils.safestring import mark_safe
from .admin_forms import ModelPostContentAdminForm



from django import forms
from .models import ModelPostContent, ModelCssClass

class ModelPostContentInlineForm(forms.ModelForm):
    class Meta:
        model = ModelPostContent
        fields = '__all__'
        widgets = {
            'css_text': forms.Select(choices=[(obj.id, obj.name) for obj in ModelCssClass.objects.filter(css_type='text')]),
            'css_media': forms.Select(choices=[(obj.id, obj.name) for obj in ModelCssClass.objects.filter(css_type='media')]),
        }


class ModelPostContentInline(admin.TabularInline):
    model = ModelPostContent
    extra = 1
    form = ModelPostContentInlineForm
    fields = ['content_text', 'css_text', 'media_file', 'css_media', 'thumbnail']
    readonly_fields = ['thumbnail']

    def thumbnail(self, obj):
        if obj.media_file:
            return mark_safe(f'<img src="{obj.media_file.url}" style="max-height: 100px; max-width: 100px;" />')
        return None



class ModelCategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(ModelCategories, ModelCategoriesAdmin)


class ModelSubcategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(ModelSubcategories, ModelSubcategoriesAdmin)


class ModelCssClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'css_code', 'icon')
    prepopulated_fields = {'name': ('name',)}

admin.site.register(ModelCssClass, ModelCssClassAdmin)


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


class ModelPostContentAdmin(admin.ModelAdmin):
    list_display = ('post', 'content_text', 'css_text', 'get_media_file_thumbnail', 'css_media')
    list_filter = ('post', 'css_text__css_type', 'css_media__css_type')  # Use 'css_text__css_type' and 'css_media__css_type'
    search_fields = ('content_text',)

    def get_media_file_thumbnail(self, obj):
        if obj.media_file:
            return mark_safe(f'<img src="{obj.media_file.url}" style="max-height: 100px; max-width: 100px;" />')
        return None

    get_media_file_thumbnail.short_description = 'Media File Thumbnail'

admin.site.register(ModelPostContent, ModelPostContentAdmin)
