from django import forms
from .widgets import ImagePreviewWidget, CssClassRadioSelect
from .models import ModelPostContent

class ModelPostContentAdminForm(forms.ModelForm):
    class Meta:
        model = ModelPostContent
        fields = '__all__'
        widgets = {
            'text_css_class': CssClassRadioSelect(),
            'media_file': ImagePreviewWidget(),
        }
