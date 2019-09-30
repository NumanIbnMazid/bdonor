# Generated by Django 2.2.1 on 2019-09-22 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donationBank', '0019_remove_donationrequest_blood_bag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donationrequest',
            name='blood_group',
            field=models.CharField(blank=True, choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('Any Blood Group', 'Any Blood Group')], max_length=20, null=True, verbose_name='blood group'),
        ),
    ]
