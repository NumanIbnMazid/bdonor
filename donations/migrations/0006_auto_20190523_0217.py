# Generated by Django 2.2.1 on 2019-05-23 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0005_auto_20190523_0202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='location',
            field=models.TextField(blank=True, max_length=200, null=True, verbose_name='preferred location'),
        ),
    ]
