# from django.contrib import admin
# from .models import ModelCategories, ModelSubcategories, ModelCssClass, ModelPosts, ModelPostContent, Rating
#
# # Register the ModelCategories model
# class ModelCategoriesAdmin(admin.ModelAdmin):
#     list_display = ('name', 'slug')
#     prepopulated_fields = {'slug': ('name',)}
#
# admin.site.register(ModelCategories, ModelCategoriesAdmin)
#
# # Register the ModelSubcategories model
# class ModelSubcategoriesAdmin(admin.ModelAdmin):
#     list_display = ('name', 'slug', 'category')
#     prepopulated_fields = {'slug': ('name',)}
#
# admin.site.register(ModelSubcategories, ModelSubcategoriesAdmin)
#
# # Register the ModelCssClass model
# class ModelCssClassAdmin(admin.ModelAdmin):
#     list_display = ('name', 'description', 'css_class', 'icon')
#     prepopulated_fields = {'css_class': ('name',)}
#
# admin.site.register(ModelCssClass, ModelCssClassAdmin)
#
# # Register the ModelPosts model
# class ModelPostsAdmin(admin.ModelAdmin):
#     list_display = ('title', 'slug', 'time_create', 'is_published', 'subcat')
#     list_filter = ('is_published', 'subcat')
#     prepopulated_fields = {'slug': ('title',)}
#
# admin.site.register(ModelPosts, ModelPostsAdmin)
#
# # Register the ModelPostContent model
# class ModelPostContentAdmin(admin.ModelAdmin):
#     list_display = ('post', 'content_text', 'text_css_class', 'media_file', 'media_css_class')
#     list_filter = ('post', 'text_css_class', 'media_css_class')
#     search_fields = ('content_text',)
#
# admin.site.register(ModelPostContent, ModelPostContentAdmin)
#
# # Register the Rating model
# class RatingAdmin(admin.ModelAdmin):
#     list_display = ('post', 'user', 'value')
#
# admin.site.register(Rating, RatingAdmin)


from django import forms
from django.contrib import admin
from django.forms import RadioSelect
from django.utils.html import format_html
from .models import ModelCategories, ModelSubcategories, ModelCssClass, ModelPosts, ModelPostContent, Rating
from django.utils.safestring import mark_safe




# class CssClassRadioSelect(RadioSelect):
#     template_name = 'blog/admin/widgets/css_class_radio.html'
#
#     def get_context(self, name, value, attrs=None):
#         context = super().get_context(name, value, attrs)
#         css_classes = ModelCssClass.objects.all()
#         context['choices'] = [
#             (css_class.name, {
#                 'icon': f'blog/icons/{css_class.icon}',
#                 'label': css_class.name,
#                 'selected': css_class.name == value,
#                 'value': css_class.name,
#             }) for css_class in css_classes
#         ]
#         return context

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


# # Custom radio select widget for CSS classes
# class ModelPostContentAdminForm(forms.ModelForm):
#     class CssClassRadioSelect(RadioSelect):
#         template_name = 'your_app/admin/widgets/css_class_radio.html'
#
#         def get_context(self, name, value, attrs=None):
#             context = super().get_context(name, value, attrs)
#             css_classes = ModelCssClass.objects.all()
#             context['choices'] = [
#                 (css_class.name, {
#                     'icon': f'your_app/icons/{css_class.icon}',
#                     'label': css_class.name,
#                     'selected': css_class.name == value,
#                     'value': css_class.name,
#                 }) for css_class in css_classes
#             ]
#             return context
#
#     text_css_class = forms.ChoiceField(
#         widget=CssClassRadioSelect(),
#         required=False,
#     )
#
#     class Meta:
#         model = ModelPostContent
#         fields = '__all__'
#
# # Register the ModelPostContent model
# class ModelPostContentAdmin(admin.ModelAdmin):
#     list_display = ('post', 'content_text', 'text_css_class', 'content_image', 'media_file', 'media_css_class')
#     list_filter = ('post', 'text_css_class', 'media_css_class')
#     search_fields = ('content_text',)
#
#     def content_image(self, obj):
#         if obj.media_file:
#             return format_html('<img src="{}{}" height="50" />'.format(settings.MEDIA_URL, obj.media_file))
#         return ""
#
#     content_image.short_description = "Media File Avatar"
#
# admin.site.register(ModelPostContent, ModelPostContentAdmin)

# class ModelPostContentAdminForm(forms.ModelForm):
#     class Meta:
#         model = ModelPostContent
#         fields = '__all__'
#         widgets = {
#             'text_css_class': CssClassRadioSelect(),
#         }

class ModelPostContentAdminForm(forms.ModelForm):
    class Meta:
        model = ModelPostContent
        fields = '__all__'
        widgets = {
            'text_css_class': CssClassRadioSelect(),
        }


class ModelPostContentAdmin(admin.ModelAdmin):
    form = ModelPostContentAdminForm
    list_display = ('post', 'content_text', 'text_css_class', 'media_file', 'media_css_class', 'get_media_preview')
    list_filter = ('post', 'text_css_class', 'media_css_class')
    search_fields = ('content_text',)

    def get_media_preview(self, obj):
        if obj.media_file:
            return mark_safe(f'<img src="{obj.media_file.url}" width="50" height="50" />')
        return ""
    get_media_preview.short_description = "Media Preview"

    class Media:
        css = {
            'all': ('blog/css/admin_icons.css',),  # Path to your custom CSS file with icon styles
        }

admin.site.register(ModelPostContent, ModelPostContentAdmin)