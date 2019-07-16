# Generated by Django 2.2.1 on 2019-07-07 00:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('utils', '0008_auto_20190626_0328'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(blank=True, max_length=255, null=True, verbose_name='category')),
                ('identifier', models.CharField(blank=True, max_length=255, null=True, verbose_name='identifier')),
                ('slug', models.SlugField(unique=True, verbose_name='slug')),
                ('subject', models.CharField(blank=True, max_length=255, null=True, verbose_name='subject')),
                ('message', models.TextField(blank=True, max_length=1000, null=True, verbose_name='message')),
                ('is_seen', models.BooleanField(default=False, verbose_name='is seen')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('receiver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification_receiver', to=settings.AUTH_USER_MODEL, verbose_name='receiver')),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification_sender', to=settings.AUTH_USER_MODEL, verbose_name='sender')),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
                'ordering': ['-updated_at'],
            },
        ),
    ]
