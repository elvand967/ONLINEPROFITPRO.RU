from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import TextInput, Select, Textarea, FileInput
from django import forms
from django.forms import formset_factory
from .models import ModelPosts, ModelPostContent, ModelCssClass, ModelSubcategories
from django.contrib.auth.models import Group


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True  # Устанавливаем статус персонала
        if commit:
            user.save()
            # # Присвоение пользователя группе "Пользователи"
            # user_group = Group.objects.get(name='Авторы постов и комментариев')
            # user.groups.add(user_group)
        return user

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
    # slug = forms.SlugField(widget=CustomTextInput())
    subcat = forms.ModelChoiceField(queryset=ModelSubcategories.objects.all(), widget=CustomSelect())
    class Meta:
        model = ModelPosts
        fields = ['title', 'subcat', 'is_published']

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

        self.fields['media_file'].required = False
        self.fields['content_text'].required = False

    class Meta:
        model = ModelPostContent
        fields = ['media_file', 'css_media', 'css_text', 'content_text']

PostContentFormset = formset_factory(PostContentForm, extra=1, can_delete=True)

