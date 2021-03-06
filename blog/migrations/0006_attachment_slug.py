# Generated by Django 2.2.1 on 2019-10-15 07:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_blog_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachment',
            name='slug',
            field=models.SlugField(default=django.utils.timezone.now, max_length=255, unique=True, verbose_name='slug'),
            preserve_default=False,
        ),
    ]
