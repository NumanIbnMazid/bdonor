from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q
from .utils import time_str_mix_slug, upload_image_path
from django.urls import reverse


class UserProfile(models.Model):
    MALE = 'Male'
    FEMALE = 'Female'
    OTHERS = 'Others'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHERS, 'Others'),
    )
    REGULAR = 0
    PREMIUM = 1
    ACCOUNT_TYPE_CHOICES = (
        (REGULAR, 'Regular'),
        (PREMIUM, 'Premium')
    )
    A_POSITIVE = 'A+'
    A_NEGATIVE = 'A-'
    B_POSITIVE = 'B+'
    B_NEGATIVE = 'B-'
    O_POSITIVE = 'O+'
    O_NEGATIVE = 'O-'
    AB_POSITIVE = 'AB+'
    AB_NEGATIVE = 'AB-'
    BLOOD_GROUP_CHOICES = (
        (A_POSITIVE, 'A+'),
        (A_NEGATIVE, 'A-'),
        (B_POSITIVE, 'B+'),
        (B_NEGATIVE, 'B-'),
        (O_POSITIVE, 'O+'),
        (O_NEGATIVE, 'O-'),
        (AB_POSITIVE, 'AB+'),
        (AB_NEGATIVE, 'AB-')
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True, related_name='profile', verbose_name='user')
    slug = models.SlugField(unique=True, verbose_name='slug')
    gender = models.CharField(choices=GENDER_CHOICES, blank=True,
                              null=True, max_length=10, verbose_name='gender')
    dob = models.DateField(blank=True, null=True, verbose_name='DOB')
    blood_group = models.CharField(
        max_length=10, choices=BLOOD_GROUP_CHOICES, verbose_name='blood group')
    contact = models.CharField(
        max_length=20, blank=True, null=True, verbose_name='contact')
    address = models.TextField(max_length=200, blank=True,
                               null=True, verbose_name='address')
    about = models.TextField(max_length=300, blank=True,
                             null=True, verbose_name='about')
    facebook = models.URLField(
        max_length=300, blank=True, null=True, verbose_name='facebook')
    linkedin = models.URLField(
        max_length=300, blank=True, null=True, verbose_name='linkedin')
    website = models.URLField(
        max_length=300, blank=True, null=True, verbose_name='website')
    image = models.ImageField(
        upload_to=upload_image_path, null=True, blank=True, verbose_name='image')
    account_type = models.PositiveSmallIntegerField(
        choices=ACCOUNT_TYPE_CHOICES, default=0, verbose_name='account type')
    is_volunteer = models.BooleanField(
        default=False, verbose_name='is volunteer')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    class Meta:
        verbose_name = ("User Profile")
        verbose_name_plural = ("User Profiles")
        ordering = ["-user__date_joined"]

    def get_absolute_url(self):
        return reverse("profile_details", kwargs={"slug": self.slug})

    def username(self):
        return self.user.username

    def get_username(self):
        if self.user.first_name or self.user.last_name:
            name = self.user.get_full_name()
        else:
            name = self.user.username
        return name

    def get_smallname(self):
        if self.user.first_name or self.user.last_name:
            name = self.user.get_short_name()
        else:
            name = self.user.username
        return name

    def get_dynamic_name(self):
        if len(self.get_username()) < 13:
            name = self.get_username()
        else:
            name = self.get_smallname()
        return name

    def get_account_type(self):
        account_type = "Undefined"
        if self.account_type == 0:
            account_type = "Regular Account"
        if self.account_type == 1:
            account_type = "Premium Account"
        return account_type

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    username = instance.username.lower()
    slug_binding = username+'-'+time_str_mix_slug()
    if created:
        UserProfile.objects.create(user=instance, slug=slug_binding)
    instance.profile.save()
