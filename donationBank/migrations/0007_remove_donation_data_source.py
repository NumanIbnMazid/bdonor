# Generated by Django 2.2.1 on 2019-08-27 00:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donationBank', '0006_donation_data_source'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donation',
            name='data_source',
        ),
    ]
