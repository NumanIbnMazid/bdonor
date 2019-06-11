# Generated by Django 2.2.1 on 2019-05-25 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20190512_0559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='facebook',
            field=models.URLField(blank=True, max_length=300, null=True, verbose_name='facebook'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='linkedin',
            field=models.URLField(blank=True, max_length=300, null=True, verbose_name='linkedin'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='website',
            field=models.URLField(blank=True, max_length=300, null=True, verbose_name='website'),
        ),
    ]
