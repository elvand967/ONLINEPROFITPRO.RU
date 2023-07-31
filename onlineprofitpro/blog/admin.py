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


# Inline class for ModelPostContent
class ModelPostContentInline(admin.TabularInline):
    model = ModelPostContent
    extra = 1
    fields = ['content_text', 'css_text', 'media_file', 'css_media', 'thumbnail']
    readonly_fields = ['thumbnail']

    def thumbnail(self, obj):
        if obj.media_file:
            return mark_safe(f'<img src="{obj.media_file.url}" style="max-height: 100px; max-width: 100px;" />')
        return None

# Admin class for ModelPosts
class ModelPostsAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'time_create', 'time_update', 'is_published', 'subcat')
    list_filter = ('time_create', 'time_update', 'is_published', 'subcat')
    search_fields = ('title', 'slug', 'subcat__name')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('time_create', 'time_update')
    inlines = [ModelPostContentInline]

# Register ModelPosts with the admin class
admin.site.register(ModelPosts, ModelPostsAdmin)


# Admin class for ModelPostContent
class ModelPostContentAdmin(admin.ModelAdmin):
    list_display = ('post', 'get_text_css_class', 'get_media_css_class')
    list_filter = ('post', 'css_text', 'css_media')
    search_fields = ('post__title', 'content_text', 'css_text__name_css_class', 'css_media__name_css_class')

    autocomplete_fields = ('post',)  # выподающий список имеющихся постов
    # raw_id_fields = ('post',)  # поле ввода id поста и лупа для выбора имеющихся постов

    def get_text_css_class(self, obj):
        return obj.get_text_css_class()

    get_text_css_class.short_description = 'CSS Class for Text'

    def get_media_css_class(self, obj):
        return obj.get_media_css_class()

    get_media_css_class.short_description = 'CSS Class for Media'

# Register ModelPostContent with the admin class
admin.site.register(ModelPostContent, ModelPostContentAdmin)

