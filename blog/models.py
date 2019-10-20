from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from accounts.utils import time_str_mix_slug, unique_slug_generator
from .utils import upload_blog_files_path
from django.urls import reverse
from django.http import Http404
from django.db.models import Q
from middlewares.middlewares import RequestMiddleware
import os


class BlogQuerySet(models.query.QuerySet):
    def article_type(self):
        return self.filter(category__iexact='article')
    
    def story_type(self):
        return self.filter(category__iexact='story')

    def help_type(self):
        return self.filter(category__iexact='help')

    def question_type(self):
        return self.filter(category__iexact='question')

    def research_type(self):
        return self.filter(category__iexact='research')
    
    def issue_type(self):
        return self.filter(category__iexact='issue')
    
    def other_type(self):
        return self.filter(category__iexact='other')

    def dynamic_order(self):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        qs = self.filter().order_by('-created_at')
        if request.user.is_authenticated and not request.user.profile.country == None:
            user_country = request.user.profile.country.code
            country_blog_qs = Blog.objects.filter().order_by('-created_at')
            if country_blog_qs.exists():
                countries_bind = country_blog_qs.values_list(
                    'user__profile__country', flat=True)
                order_field = list(countries_bind)
                if user_country in order_field:
                    order_field.remove(user_country)
                order_field.insert(0, user_country)
                qs = sorted(self.filter().order_by('-created_at'),
                            key=lambda p: order_field.index(p.user.profile.country))
                # print(order_field)
                # print(qs)
        else:
            qs = self.filter().order_by('-created_at')
        return qs

    def search(self, query):
        lookups = (Q(title__icontains=query) |
                   Q(category__icontains=query) |
                   Q(tags__icontains=query) |
                   Q(details__icontains=query) |
                   Q(user__username__icontains=query) |
                   Q(user__first_name__icontains=query) |
                   Q(user__last_name__icontains=query) |
                   Q(user__email__icontains=query)
                   )
        return self.filter(lookups).distinct()


class BlogManager(models.Manager):
    def get_queryset(self):
        return BlogQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset()

    def get_by_id(self, id):
        try:
            instance = self.get_queryset().get(id=id)
        except Comment.DoesNotExist:
            raise Http404("Not Found !!!")
        except Comment.MultipleObjectsReturned:
            qs = self.get_queryset().filter(id=id)
            instance = qs.first()
        except:
            raise Http404("Something went wrong !!!")
        return instance

    def get_by_slug(self, slug, request):
        try:
            instance = self.get_queryset().get(slug=slug)
        except Blog.DoesNotExist:
            raise Http404("Not Found !!!")
        except Blog.MultipleObjectsReturned:
            qs = self.get_queryset().filter(slug=slug)
            instance = qs.first()
        except:
            raise Http404("Something went wrong !!!")
        return instance

    def search(self, query):
        return self.get_queryset().search(query)


class Blog(models.Model):
    ARTICLE = 'article'
    PERSONAL_STORY = 'story'
    HELP_POST = 'help'
    QUESTIONNAIRE = 'question'
    RESEARCH_ACTIVITY = 'research'
    ISSUE = 'issue'
    OTHER = 'other'
    CATEGORY_CHOICES = (
        (ARTICLE, 'Article'),
        (PERSONAL_STORY, 'Personal Story'),
        (HELP_POST, 'Help Post'),
        (QUESTIONNAIRE, 'Questionnaire'),
        (RESEARCH_ACTIVITY, 'Research Activity'),
        (ISSUE, 'Issue'),
        (OTHER, 'Other'),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_blog', verbose_name='user'
    )
    slug = models.SlugField(max_length=255, unique=True, verbose_name='slug')
    title = models.CharField(max_length=250, verbose_name='title')
    category = models.CharField(max_length=250, choices=CATEGORY_CHOICES, default='article', verbose_name='category')
    details = models.TextField(max_length=20000, verbose_name='details')
    tags = models.CharField(max_length=150, blank=True, null=True, verbose_name='tags')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    objects = BlogManager()

    class Meta:
        verbose_name = ("Blog")
        verbose_name_plural = ("Blogs")
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_category(self):
        category = None
        if self.category == 'article':
            category = 'Article'
        if self.category == 'story':
            category = 'Personal Story'
        if self.category == 'help':
            category = 'Help Post'
        if self.category == 'question':
            category = 'Questionnaire'
        if self.category == 'research':
            category = 'Research Activity'
        if self.category == 'issue':
            category = 'Issue'
        if self.category == 'other':
            category = 'Other'
        return category


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


class CommentQuerySet(models.query.QuerySet):
    def is_selected(self):
        return self.filter(is_selected=True)


class CommentManager(models.Manager):
    def get_queryset(self):
        return CommentQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset()

    def get_by_id(self, id):
        try:
            instance = self.get_queryset().get(id=id)
        except Comment.DoesNotExist:
            raise Http404("Not Found !!!")
        except Comment.MultipleObjectsReturned:
            qs = self.get_queryset().filter(id=id)
            instance = qs.first()
        except:
            raise Http404("Something went wrong !!!")
        return instance


class Comment(models.Model):
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name='blog_comment', verbose_name='blog'
    )
    commented_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_comment', verbose_name='commented by'
    )
    comment = models.TextField(max_length=1000, verbose_name='comment')
    is_selected = models.BooleanField(default=False, verbose_name='is selected')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    objects = CommentManager()

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['-updated_at']

    def __str__(self):
        return self.blog.title



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

    
