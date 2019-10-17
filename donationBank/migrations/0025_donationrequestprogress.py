# Generated by Django 2.2.1 on 2019-10-17 05:11

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('donationBank', '0024_auto_20190924_0343'),
    ]

    operations = [
        migrations.CreateModel(
            name='DonationRequestProgress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('progress_status', models.PositiveSmallIntegerField(choices=[(0, 'Pending'), (1, 'Completed')], default=0, verbose_name='progress status')),
                ('completion_date', models.DateField(blank=True, null=True, verbose_name='completion date')),
                ('first_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='last name')),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], max_length=10, null=True, verbose_name='gender')),
                ('blood_group', models.CharField(blank=True, choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')], max_length=10, null=True, verbose_name='blood group')),
                ('dob', models.DateField(blank=True, null=True, verbose_name='Date of Birth')),
                ('contact', models.CharField(blank=True, max_length=20, null=True, verbose_name='contact')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='email')),
                ('address', models.CharField(blank=True, max_length=250, null=True, verbose_name='address')),
                ('city', models.CharField(blank=True, max_length=100, null=True, verbose_name='city')),
                ('state', models.CharField(blank=True, max_length=100, null=True, verbose_name='state/province')),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('details', models.TextField(blank=True, max_length=500, null=True, verbose_name='details')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('donation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='donation_request_progress', to='donationBank.DonationRequest', verbose_name='donation')),
            ],
            options={
                'verbose_name': 'Donation Request Progress',
                'verbose_name_plural': 'Donation Request Progresses',
                'ordering': ['-updated_at'],
            },
        ),
    ]
