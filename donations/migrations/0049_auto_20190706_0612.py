# Generated by Django 2.2.1 on 2019-07-06 06:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0048_auto_20190706_0539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donationrespond',
            name='respondent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donation_respondent', to=settings.AUTH_USER_MODEL, verbose_name='respondent'),
        ),
    ]
