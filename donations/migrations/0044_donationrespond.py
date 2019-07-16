# Generated by Django 2.2.1 on 2019-07-06 01:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('donations', '0043_donation_contact_privacy'),
    ]

    operations = [
        migrations.CreateModel(
            name='DonationRespond',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.CharField(blank=True, max_length=17, null=True, verbose_name='contact')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('donation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donation_respond', to='donations.Donation', verbose_name='donation')),
                ('respondent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donation_respondent', to=settings.AUTH_USER_MODEL, verbose_name='respondent')),
            ],
            options={
                'verbose_name': 'Donation Respond',
                'verbose_name_plural': 'Donation Responds',
                'ordering': ['-updated_at'],
            },
        ),
    ]
