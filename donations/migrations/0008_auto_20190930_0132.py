# Generated by Django 2.2.1 on 2019-09-30 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0007_auto_20190925_2132'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donationprogress',
            name='respondent',
        ),
        migrations.AddField(
            model_name='donationprogress',
            name='respondent',
            field=models.ManyToManyField(blank=True, null=True, related_name='donation_progress_respondent', to='donations.DonationRespond', verbose_name='respondent'),
        ),
    ]
