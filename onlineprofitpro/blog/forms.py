from django.forms.widgets import TextInput, Select, Textarea, FileInput
from django import forms
from django.forms import formset_factory
from .models import ModelPosts, ModelPostContent, ModelCssClass, ModelSubcategories


class CustomTextarea(Textarea):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {}).update({'class': 'form-control'})
        super().__init__(*args, **kwargs)

class CustomTextInput(TextInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {}).update({'class': 'form-control'})
        super().__init__(*args, **kwargs)

class CustomSelect(Select):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {}).update({'class': 'form-select'})
        super().__init__(*args, **kwargs)

class CustomFileInput(FileInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {}).update({'class': 'form-control'})
        super().__init__(*args, **kwargs)


class AddPostForm(forms.ModelForm):
    title = forms.CharField(widget=CustomTextInput())
    slug = forms.SlugField(widget=CustomTextInput())
    subcat = forms.ModelChoiceField(queryset=ModelSubcategories.objects.all(), widget=CustomSelect())
    class Meta:
        model = ModelPosts
        fields = ['title', 'slug', 'subcat', 'is_published']

class PostContentForm(forms.ModelForm):
    content_text = forms.CharField(widget=CustomTextarea())
    media_file = forms.FileField(widget=CustomFileInput())
    def __init__(self, *args, **kwargs):
        super(PostContentForm, self).__init__(*args, **kwargs)
        css_text_default = ModelCssClass.objects.filter(css_type='text').first()
        css_media_default = ModelCssClass.objects.filter(css_type='media').first()
        self.fields['css_text'].initial = css_text_default
        self.fields['css_media'].initial = css_media_default

        # Filter choices for 'css_text' and 'css_media'
        self.fields['css_text'].queryset = ModelCssClass.objects.filter(css_type='text')
        self.fields['css_media'].queryset = ModelCssClass.objects.filter(css_type='media')

    class Meta:
        model = ModelPostContent
        fields = ['content_text', 'css_text', 'media_file', 'css_media']

PostContentFormset = formset_factory(PostContentForm, extra=1, can_delete=True)

