# Generated by Django 2.2.1 on 2019-10-05 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0013_donationrespond_is_applied_for_selection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donationprogress',
            name='management_status',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(0, 'BDonar'), (1, 'Somewhere else')], default=0, null=True, verbose_name='managed on'),
        ),
    ]