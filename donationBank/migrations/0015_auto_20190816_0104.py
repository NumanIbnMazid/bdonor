# Generated by Django 2.2.1 on 2019-08-16 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donationBank', '0014_auto_20190815_0605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='quantity',
            field=models.PositiveIntegerField(blank=True, default=1, null=True, verbose_name='quantity'),
        ),
    ]
