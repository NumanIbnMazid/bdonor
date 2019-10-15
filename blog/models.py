from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from accounts.utils import time_str_mix_slug, unique_slug_generator
from .utils import upload_blog_files_path
from django.urls import reverse
import os


class Blog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_blog', verbose_name='user'
    )
    slug = models.SlugField(max_length=255, unique=True, verbose_name='slug')
    title = models.CharField(max_length=250, verbose_name='title')
    details = models.TextField(max_length=5000, verbose_name='details')
    tags = models.CharField(max_length=150, blank=True, null=True, verbose_name='tags')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    class Meta:
        verbose_name = ("Blog")
        verbose_name_plural = ("Blogs")
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Attachment(models.Model):
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name='blog_attachments', verbose_name='blog'
    )
    slug = models.SlugField(max_length=255, unique=True, verbose_name='slug')
    file = models.FileField(
        upload_to=upload_blog_files_path, blank=True, null=True, verbose_name='attachments')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')
    
    class Meta:
        verbose_name = ("Attachment")
        verbose_name_plural = ("Attachments")
        ordering = ["-blog__created_at"]

    def __str__(self):
        return self.blog.title

    def get_file_type(self):
        file_type = None
        name, extension = os.path.splitext(self.file.name)
        if extension in settings.ALLOWED_IMAGE_TYPES:
            file_type = 'image'
        if extension in settings.ALLOWED_DOCUMENT_TYPES:
            file_type = 'document'
        return file_type

    def get_file_extension(self):
        extension = None
        name, extension = os.path.splitext(self.file.name)
        return extension


def blog_slug_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(blog_slug_pre_save_receiver, sender=Blog)


def attachment_slug_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        title = instance.blog.title.lower()[:10]
        slug_binding = title + '-' + time_str_mix_slug()
        instance.slug = slug_binding


pre_save.connect(attachment_slug_pre_save_receiver, sender=Attachment)

    
