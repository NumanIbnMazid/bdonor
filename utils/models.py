from django.db import models
from accounts.models import UserProfile
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class SitePreference(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE,
                             related_name='user_site_preference', verbose_name='user')
    logo_header_color = models.CharField(
        max_length=100, null=True, blank=True, verbose_name='logo header color')
    navbar_header_color = models.CharField(
        max_length=100, null=True, blank=True, verbose_name='navbar header color')
    sidebar_color = models.CharField(
        max_length=50, null=True, blank=True, verbose_name='sidebar color')
    background_color = models.CharField(
        max_length=50, null=True, blank=True, verbose_name='background color')
    sidebar_type = models.CharField(
        max_length=50, blank=True, null=True, default='Default', verbose_name='sidebar type')
    scroll_to_top = models.BooleanField(
        default=True, verbose_name='scroll to top')
    chat_with_others = models.BooleanField(
        default=True, verbose_name='chat with others')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    def __str__(self):
        return self.user.user.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        SitePreference.objects.create(user=instance.profile)
