# Generated by Django 2.2.1 on 2019-09-22 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donationBank', '0013_auto_20190922_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donationbank',
            name='services',
            field=models.CharField(choices=[('Blood', 'Blood'), ('Organ', 'Organ'), ('Tissue', 'Tissue')], max_length=100, verbose_name='services'),
        ),
    ]
