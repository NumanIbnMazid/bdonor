# Generated by Django 2.2.1 on 2019-10-20 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20191020_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='category',
            field=models.CharField(choices=[('article', 'Article'), ('story', 'Personal Story'), ('help', 'Help Post'), ('question', 'Questionnaire'), ('research', 'Research Activity'), ('issue', 'Issue'), ('other', 'Other')], default='article', max_length=250, verbose_name='category'),
        ),
    ]
