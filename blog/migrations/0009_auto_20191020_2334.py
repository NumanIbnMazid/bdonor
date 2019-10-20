# Generated by Django 2.2.1 on 2019-10-20 23:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0008_auto_20191015_1009'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='category',
            field=models.CharField(choices=[('article', 'Article'), ('story', 'Personal Story'), ('help', 'Help Post'), ('question', 'Questionnaire'), ('research', 'Research Activity'), ('issue', 'Issue'), ('other', 'Other')], default='Article', max_length=250, verbose_name='title'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=1000, verbose_name='comment')),
                ('is_selected', models.BooleanField(default=False, verbose_name='is selected')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_comment', to='blog.Blog', verbose_name='blog')),
                ('commented_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comment', to=settings.AUTH_USER_MODEL, verbose_name='commented by')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
                'ordering': ['-updated_at'],
            },
        ),
    ]