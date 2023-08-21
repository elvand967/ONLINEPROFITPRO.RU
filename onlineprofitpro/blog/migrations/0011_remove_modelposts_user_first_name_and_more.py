# Generated by Django 4.1.10 on 2023-08-18 13:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0010_modelpostcontent_code_modelpostcontent_css_code_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modelposts',
            name='user_first_name',
        ),
        migrations.RemoveField(
            model_name='modelposts',
            name='user_last_name',
        ),
        migrations.RemoveField(
            model_name='modelposts',
            name='user_username',
        ),
        migrations.AddField(
            model_name='modelposts',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
    ]
