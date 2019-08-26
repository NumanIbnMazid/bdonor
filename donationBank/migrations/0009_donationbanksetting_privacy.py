# Generated by Django 2.2.1 on 2019-08-27 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donationBank', '0008_remove_campaign_volunteer_request'),
    ]

    operations = [
        migrations.AddField(
            model_name='donationbanksetting',
            name='privacy',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Public'), (1, 'Private')], default=0, verbose_name='privacy'),
        ),
    ]
