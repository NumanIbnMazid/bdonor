from django.db import models
from accounts.models import UserProfile
from donations.models import Donation
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import datetime
from .utils import time_str_mix_slug


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

    class Meta:
        verbose_name = ("Site Preference")
        verbose_name_plural = ("Site Preferences")
        ordering = ["-updated_at"]

    def __str__(self):
        return self.user.user.username


class Location(models.Model):
    ADDRESS = 0
    HOSPITAL = 1
    LOCATION_CHOICES = (
        (ADDRESS, 'Address'),
        (HOSPITAL, 'Hospital')
    )
    provider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name='location_provider', verbose_name='provider')
    location_type = models.PositiveSmallIntegerField(
        default=0, verbose_name='location type')
    location = models.TextField(blank=True, null=True, verbose_name='location')
    hit = models.PositiveIntegerField(default=1, verbose_name='hit')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    class Meta:
        verbose_name = ("Location")
        verbose_name_plural = ("Locations")
        ordering = ["-updated_at"]

    def __str__(self):
        return self.location


class Notification(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
                               related_name='notification_sender', verbose_name='sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
                                 related_name='notification_receiver', verbose_name='receiver')
    category = models.CharField(
        max_length=255, blank=True, null=True, verbose_name='category')
    identifier = models.CharField(
        max_length=255, blank=True, null=True, verbose_name='identifier')
    slug = models.SlugField(unique=True, verbose_name='slug')
    subject = models.CharField(
        max_length=255, blank=True, null=True, verbose_name='subject')
    message = models.TextField(
        max_length=1000, blank=True, null=True, verbose_name='message')
    is_seen = models.BooleanField(default=False, verbose_name='is seen')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-updated_at']

    def __str__(self):
        return self.subject


# Create site preference object after user signup
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_site_preference(sender, instance, **kwargs):
    qs = SitePreference.objects.filter(user=instance.profile)
    if not qs.exists():
        SitePreference.objects.create(user=instance.profile)


# Create location object From User Profile
@receiver(post_save, sender=UserProfile)
def create_or_update_utils_module_from_user_profile(sender, instance, **kwargs):
    if not instance.address == None:
        qs = Location.objects.filter(
            location_type=0, location__iexact=instance.address)
        if qs.exists():
            if not qs.first().provider == instance.user:
                calculated_hit = qs.first().hit + 1
                qs.update(hit=calculated_hit,
                          updated_at=datetime.datetime.now())
        else:
            Location.objects.create(
                provider=instance.user, location_type=0, location=instance.address)


# Create location object From Donation Management
@receiver(post_save, sender=Donation)
def create_or_update_utils_module_from_donations(sender, instance, **kwargs):
    # Address Component
    if not instance.location == None:
        address_qs = Location.objects.filter(
            location__iexact=instance.location)
        if address_qs.exists():
            if not address_qs.first().provider == instance.user.user:
                address_calculated_hit = address_qs.first().hit + 1
                address_qs.update(hit=address_calculated_hit,
                                  updated_at=datetime.datetime.now())
        else:
            Location.objects.create(
                provider=instance.user.user, location_type=0, location=instance.location)
    # Hospital Component
    if not instance.hospital == None:
        hospital_qs = Location.objects.filter(
            location_type=1, location__iexact=instance.hospital)
        if hospital_qs.exists():
            if not hospital_qs.first().provider == instance.user.user:
                hospital_calculated_hit = hospital_qs.first().hit + 1
                hospital_qs.update(hit=hospital_calculated_hit,
                                   updated_at=datetime.datetime.now())
        else:
            Location.objects.create(
                provider=instance.user.user, location_type=1, location=instance.hospital)


def notification_slug_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug_bind = instance.sender.username[:5] + "-" + instance.receiver.username[:5] + "_" + time_str_mix_slug()
        instance.slug = slug_bind


pre_save.connect(notification_slug_pre_save_receiver, sender=Notification)

