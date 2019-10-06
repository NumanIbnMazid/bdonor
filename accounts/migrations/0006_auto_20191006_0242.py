# Generated by Django 2.2.1 on 2019-10-06 02:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0005_userreport'),
    ]

    operations = [
        migrations.AddField(
            model_name='userreport',
            name='reported_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_reported_by', to=settings.AUTH_USER_MODEL, verbose_name='reported by'),
        ),
        migrations.AlterField(
            model_name='userreport',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_report', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]
