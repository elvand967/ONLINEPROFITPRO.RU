from django import forms
from django.forms import RadioSelect
from django.utils.safestring import mark_safe

class ImagePreviewWidget(forms.FileInput):
    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        if value and hasattr(value, 'url'):
            image_url = value.url
            preview_html = mark_safe(f'<img src="{image_url}" style="max-height: 100px; max-width: 100px;" />')
            html = f'{preview_html}<br>{html}'
        return mark_safe(html)

class CssClassRadioSelect(RadioSelect):
    template_name = 'admin/widgets/css_class_radio.html'
