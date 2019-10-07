# Generated by Django 2.2.1 on 2019-10-06 23:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0007_auto_20191006_0242'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('can_browse', models.BooleanField(default=True, verbose_name='can browse')),
                ('can_donate', models.BooleanField(default=True, verbose_name='can donate')),
                ('can_ask_for_a_donor', models.BooleanField(default=True, verbose_name='can ask for a donor')),
                ('can_manage_bank', models.BooleanField(default=True, verbose_name='can manage bank')),
                ('can_chat', models.BooleanField(default=True, verbose_name='can chat')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_permissions_user', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'User Permission',
                'verbose_name_plural': 'User Permissions',
                'ordering': ['-created_at'],
            },
        ),
    ]
