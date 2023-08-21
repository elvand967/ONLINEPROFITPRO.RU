

from django.utils.html import format_html
from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import ModelCategories, ModelSubcategories, ModelCssClass, ModelPostContent, ModelPosts


# Admin class for ModelCategories
class ModelCategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(ModelCategories, ModelCategoriesAdmin)

# Admin class for ModelSubcategories
class ModelSubcategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug')
    prepopulated_fields = {'slug': ('name',)}

# Register ModelCategories and ModelSubcategories with their respective admin classes
admin.site.register(ModelSubcategories, ModelSubcategoriesAdmin)


# Admin class for ModelCssClass
class ModelCssClassAdmin(admin.ModelAdmin):
    list_display = ('name_css_class', 'css_type', 'class_css', 'class_css_code', 'icon')
    list_filter = ('css_type',)
    search_fields = ('name_css_class', 'description', 'class_css')

# Register ModelCssClass with the admin class
admin.site.register(ModelCssClass, ModelCssClassAdmin)



class ModelPostContentInlineForm(forms.ModelForm):
    class Meta:
        model = ModelPostContent
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit the choices for css_text to 'Text' classes
        self.fields['css_text'].queryset = ModelCssClass.objects.filter(css_type='text')
        # Limit the choices for css_image to 'Image' classes
        self.fields['css_image'].queryset = ModelCssClass.objects.filter(css_type='image')
        # Limit the choices for css_media to 'Video' and 'Audio' classes
        self.fields['css_media'].queryset = ModelCssClass.objects.filter(css_type__in=['video', 'audio'])
        # Limit the choices for css_youtube to 'YouTube' classes
        self.fields['css_youtube'].queryset = ModelCssClass.objects.filter(css_type='youtube')

        # Set default values for the dropdown lists
        if not self.instance.css_text:
            # Get the first 'Text' class as the default for css_text
            default_text_class = ModelCssClass.objects.filter(css_type='text').first()
            if default_text_class:
                self.initial['css_text'] = default_text_class

        if not self.instance.css_image:
            # Get the first 'Image' class as the default for css_image
            default_image_class = ModelCssClass.objects.filter(css_type='image').first()
            if default_image_class:
                self.initial['css_image'] = default_image_class

        if not self.instance.css_media:
            # Get the first 'Video' or 'Audio' class as the default for css_media
            default_media_class = ModelCssClass.objects.filter(css_type__in=['video', 'audio']).first()
            if default_media_class:
                self.initial['css_media'] = default_media_class

        if not self.instance.css_youtube:
            # Get the first 'YouTube' class as the default for css_youtube
            default_youtube_class = ModelCssClass.objects.filter(css_type__in=['youtube']).first()
            if default_youtube_class:
                self.initial['css_youtube'] = default_youtube_class

'''
# Inline class for ModelPostContent
# class ModelPostContentInline(admin.TabularInline):  # поля в линию
# class ModelPostContentInline(admin.StackedInline):  # поля в столбец
'''

class ModelPostContentInline(admin.StackedInline):
    model = ModelPostContent
    extra = 1
    form = ModelPostContentInlineForm
    fields = ['css_text', 'content_text', 'css_image', 'thumbnail',  'image_file','css_media', 'media_file', 'css_youtube', 'youtube_video', 'css_code', 'code']
    readonly_fields = ['thumbnail']

    def thumbnail(self, obj):
        if obj.image_file:
            return mark_safe(f'<img src="{obj.image_file.url}" style="max-height: 100px; max-width: 100px;" />')
        return None


# Admin class for ModelPosts
class ModelPostsAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'time_create', 'time_update', 'is_published', 'subcat')
    list_filter = ('time_create', 'time_update', 'is_published', 'subcat')
    search_fields = ('title', 'slug', 'subcat__name')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('time_create', 'time_update')
    inlines = [ModelPostContentInline]

    def save_model(self, request, obj, form, change):
        if not obj.user:  # Only set the user if it's not already set
            obj.user = request.user
        super().save_model(request, obj, form, change)

# Register ModelPosts with the admin class
admin.site.register(ModelPosts, ModelPostsAdmin)


# Admin class for ModelPostContent
class ModelPostContentForm(forms.ModelForm):
    class Meta:
        model = ModelPostContent
        fields = '__all__'


class ModelPostContentAdmin(admin.ModelAdmin):
    form = ModelPostContentForm
    list_display = ('post', 'get_text_css_class', 'get_image_css_class', 'get_media_css_class', 'get_youtube_video', 'get_youtube_css_class')
    list_filter = ('post', 'css_text', 'css_image', 'css_media', 'css_youtube')
    search_fields = ('post__title', 'content_text', 'css_text__name_css_class', 'css_image__name_css_class', 'css_media__name_css_class', 'css_youtube__name_css_class')

    autocomplete_fields = ('post', 'css_text', 'css_image', 'css_media', 'css_youtube')

    def get_text_css_class(self, obj):
        return obj.get_text_css_class()

    get_text_css_class.short_description = 'CSS Class for Text'

    def get_image_css_class(self, obj):
        return obj.get_image_css_class()

    get_image_css_class.short_description = 'CSS Class for Image'

    def get_media_css_class(self, obj):
        return obj.get_media_css_class()

    get_media_css_class.short_description = 'CSS Class for Media'

    def get_youtube_video(self, obj):
        return format_html('<a href="{}" target="_blank">Link</a>', obj.youtube_video) if obj.youtube_video else None

    get_youtube_video.short_description = 'YouTube Video URL'

    def get_youtube_css_class(self, obj):
        return obj.get_youtube_css_class()

    get_youtube_css_class.short_description = 'CSS Class for YouTube Video'

# Register ModelPostContent with the updated admin class


