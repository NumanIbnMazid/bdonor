# Generated by Django 2.2.1 on 2019-10-15 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20191015_0753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='details',
            field=models.TextField(max_length=20000, verbose_name='details'),
        ),
    ]
