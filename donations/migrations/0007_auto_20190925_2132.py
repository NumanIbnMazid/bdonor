# Generated by Django 2.2.1 on 2019-09-25 21:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0006_auto_20190925_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donationprogress',
            name='respondent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='donation_progress_respondent', to='donations.DonationRespond', verbose_name='respondent'),
        ),
    ]