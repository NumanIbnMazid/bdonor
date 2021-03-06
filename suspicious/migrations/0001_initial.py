# Generated by Django 2.2.1 on 2019-08-21 02:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Suspicious',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attempt', models.PositiveSmallIntegerField(default=1, verbose_name='attempt')),
                ('first_attempt', models.DateTimeField(auto_now_add=True, verbose_name='first attempt')),
                ('last_attempt', models.DateTimeField(auto_now=True, verbose_name='last attempt')),
                ('ip', models.CharField(blank=True, max_length=150, null=True, verbose_name='ip address')),
                ('mac', models.CharField(blank=True, max_length=150, null=True, verbose_name='mac address')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suspicious', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Suspicious User',
                'verbose_name_plural': 'Suspicious Users',
                'ordering': ['-last_attempt'],
            },
        ),
    ]
