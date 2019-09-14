from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q
from .utils import time_str_mix_slug, upload_image_path
from django.urls import reverse
from allauth.account.signals import user_logged_in, user_signed_up
import stripe
from django_countries.fields import CountryField

stripe.api_key = settings.STRIPE_SECRET_KEY


class UserProfile(models.Model):
    MALE = 'Male'
    FEMALE = 'Female'
    OTHERS = 'Others'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHERS, 'Others'),
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
    REGULAR = 0
    PREMIUM = 1
    ACCOUNT_TYPE_CHOICES = (
        (REGULAR, 0),
        (PREMIUM, 1),
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True, related_name='profile', verbose_name='user')
    # name = models.CharField(max_length=250, blank=True, null=True, verbose_name='name')
    slug = models.SlugField(unique=True, verbose_name='slug')
    account_type = models.PositiveSmallIntegerField(
        default=0, choices=ACCOUNT_TYPE_CHOICES, verbose_name='account type')
    gender = models.CharField(choices=GENDER_CHOICES, blank=True,
                              null=True, max_length=10, verbose_name='gender')
    dob = models.DateField(blank=True, null=True, verbose_name='DOB')
    blood_group = models.CharField(
        max_length=10, choices=BLOOD_GROUP_CHOICES, verbose_name='blood group')
    contact = models.CharField(
        max_length=20, blank=True, null=True, verbose_name='contact')
    address = models.TextField(max_length=200, blank=True,
                               null=True, verbose_name='address')
    city = models.CharField(blank=True, null=True,
                            max_length=100, verbose_name='city')
    state = models.CharField(blank=True, null=True,
                             max_length=100, verbose_name='state/province')
    country = CountryField(blank=True, null=True)
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
            account_type = "Regular User"
        if self.account_type == 1:
            account_type = "Premium User"
        return account_type

    def __str__(self):
        return self.user.username


class UserStripe(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='user')
    stripe_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='stripe id')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    class Meta:
        verbose_name = ("User Stripe")
        verbose_name_plural = ("User Stripes")
        ordering = ["-user__date_joined"]

    def __str__(self):
        if self.stripe_id:
            return str(self.stripe_id)
        else:
            return self.user.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    username = instance.username.lower()
    slug_binding = username+'-'+time_str_mix_slug()
    if created:
        UserProfile.objects.create(user=instance, slug=slug_binding)
    instance.profile.save()


def stripeCallback(sender, request, user, **kwargs):
    user_stripe_account, created = UserStripe.objects.get_or_create(user=user)
    # if created:
        # print('Created for %s' % (user.username))
    if user_stripe_account.stripe_id is None or user_stripe_account.stripe_id == '':
        new_stripe_id = stripe.Customer.create(email=user.email)
        user_stripe_account.stripe_id = new_stripe_id['id']
        user_stripe_account.save()

user_logged_in.connect(stripeCallback)
user_signed_up.connect(stripeCallback)
