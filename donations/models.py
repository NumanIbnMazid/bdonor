from django.db import models
from accounts.models import UserProfile
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from accounts.utils import unique_slug_generator
from django.core.validators import RegexValidator
import datetime
from django.db.models import Q
from django.urls import reverse
from django.http import Http404

class DonationQuerySet(models.query.QuerySet):
    def offers(self):
        return self.filter(category=0)

    def requests(self):
        return self.filter(category=1)

    def blood_type(self):
        return self.filter(type=0)
    
    def organ_type(self):
        return self.filter(type=1)
    
    def custom_type(self):
        return self.filter(type=2)

    def is_published(self):
        return self.filter(publication_status=0)

    def is_not_published(self):
        return self.filter(publication_status=1)

    # Foreign
    def is_done(self):
        return self.filter(donation_progress__progress_status=1)

    def is_pending(self):
        return self.filter(donation_progress__progress_status=0)

    def is_managed_on_site(self):
        return self.filter(donation_progress__management_status=0)

    def is_managed_on_outside(self):
        return self.filter(donation_progress__management_status=1)
    # /Foreign

    def is_important(self):
        return self.filter(priority=1)

    def is_normal(self):
        return self.filter(priority=0)

    def latest(self):
        return self.filter().order_by('-created_at')

    def Donations_current_year(self):
        today = datetime.datetime.now()
        return self.filter(created_at__year=today.year)

    def donations_by_year(self, year_search):
        return self.filter(created_at__year=year_search)

    def donations_by_user(self, user):
        return self.filter(user=user.profile)

    def search(self, query):
        lookups = (Q(title__icontains=query) |
                   Q(user__icontains=query) |
                   Q(category__icontains=query) |
                   Q(type__icontains=query) |
                   Q(custom_type__icontains=query) |
                   Q(blood_group__icontains=query) |
                   Q(blood_bag__icontains=query) |
                   Q(organ_name__icontains=query) |
                   Q(details__icontains=query) |
                   Q(contact__icontains=query) |
                   Q(contact2__icontains=query) |
                   Q(contact3__icontains=query) |
                   Q(preferred_date__icontains=query) |
                   Q(preferred_date_from__icontains=query) |
                   Q(preferred_date_to__icontains=query) |
                   Q(location__icontains=query) |
                   Q(priority__icontains=query) |
                   Q(user__user__username__icontains=query) |
                   Q(user__user__first_name__icontains=query) |
                   Q(user__user__last_name__icontains=query) |
                   Q(user__user__email__icontains=query)
                   )
        return self.filter(lookups).distinct()



class DonationManager(models.Manager):
    def get_queryset(self):
        return DonationQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset()

    def get_by_id(self, id):
        try:
            instance = self.get_queryset().get(id=id)
        except Donation.DoesNotExist:
            raise Http404("Not Found !!!")
        except Donation.MultipleObjectsReturned:
            qs = self.get_queryset().filter(id=id)
            instance = qs.first()
        except:
            raise Http404("Something went wrong !!!")
        return instance

    def get_by_slug(self, slug):
        try:
            instance = self.get_queryset().get(slug=slug)
        except Donation.DoesNotExist:
            raise Http404("Not Found !!!")
        except Donation.MultipleObjectsReturned:
            qs = self.get_queryset().filter(slug=slug)
            instance = qs.first()
        except:
            raise Http404("Something went wrong !!!")
        return instance

    def search(self, query):
        return self.get_queryset()



class Donation(models.Model):
    # contact_regex = RegexValidator(
    #     regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    OFFER_DONATION = 0
    ASK_FOR_DONATION = 1
    DONATION_CATEGORY_CHOICES = (
        (OFFER_DONATION, 'Offer Donation'),
        (ASK_FOR_DONATION, 'Ask for Donation'),
    )
    BLOOD = 0
    BODY_ORGANS = 1
    OTHERS = 2
    DONATION_CHOICES = (
        (BLOOD, 'Blood'),
        (BODY_ORGANS, 'Organ'),
        (OTHERS, 'Other'),
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
    NORMAL = 0
    IMPORTANT = 1
    DONATION_PRIORITY_CHOICES = (
        (NORMAL, 'Normal'),
        (IMPORTANT, 'Important'),
    )
    PUBLISHED = 0
    UNPUBLISHED = 1
    DONATION_PUBLICATION_CHOICES = (
        (PUBLISHED, 'Published'),
        (UNPUBLISHED, 'Unpublished'),
    )
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='donation_profile', verbose_name='user')
    title = models.CharField(max_length=60, verbose_name='post title')
    slug = models.SlugField(unique=True, verbose_name='slug')
    category = models.PositiveSmallIntegerField(
        choices=DONATION_CATEGORY_CHOICES, verbose_name='category')
    type = models.PositiveSmallIntegerField(
        choices=DONATION_CHOICES, verbose_name='donation type')
    custom_type = models.CharField(
        max_length=30, blank=True, null=True, verbose_name='custom type name')
    blood_group = models.CharField(
        max_length=10, choices=BLOOD_GROUP_CHOICES, null=True, blank=True, verbose_name='blood group')
    blood_bag = models.CharField(
        blank=True, null=True, max_length=4, verbose_name='blood bag quantity')
    organ_name = models.CharField(
        max_length=50, blank=True, null=True, verbose_name='organ name')
    details = models.TextField(blank=True,
                               null=True, verbose_name='details')
    # contact = models.CharField(
    #     validators=[contact_regex], max_length=17, verbose_name='contact number')
    contact = models.CharField(
        max_length=17, verbose_name='contact number')
    contact2 = models.CharField(
        max_length=17, blank=True, null=True, verbose_name='contact number 2')
    contact3 = models.CharField(
        max_length=17, blank=True, null=True, verbose_name='contact number 3')
    preferred_date = models.DateTimeField(
        verbose_name='preferred date', blank=True, null=True)
    preferred_date_from = models.DateTimeField(
        verbose_name='preferred date from', blank=True, null=True)
    preferred_date_to = models.DateTimeField(
        verbose_name='preferred date to', blank=True, null=True)
    location = models.CharField(max_length=200, blank=True,
                                null=True, verbose_name='preferred location')
    priority = models.PositiveSmallIntegerField(
        choices=DONATION_PRIORITY_CHOICES, default=0, verbose_name='priority')
    publication_status = models.PositiveSmallIntegerField(
        choices=DONATION_PUBLICATION_CHOICES, default=0, verbose_name='publication status')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    objects = DonationManager()

    class Meta:
        verbose_name = ("Donation")
        verbose_name_plural = ("Donations")
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("donations:donation_details", kwargs={"slug": self.slug})

    def get_donation_type(self):
        type = "Undefined"
        if self.type == 0:
            type = "Blood"
        if self.type == 1:
            type = "Organ"
        if self.type == 2:
            type = "Other"
        return type

    def get_type_dynamic_short_detail(self):
        detail = "Undefined"
        if self.type == 0:
            detail = f"{self.blood_group} ({self.blood_bag} bag)"
        if self.type == 1:
            detail = f"{self.organ_name}"
        if self.type == 2:
            detail = f"{self.custom_type}"
        return detail

    def get_priority(self):
        priority = "Undefined"
        if self.priority == 0:
            priority = "Normal"
        if self.priority == 1:
            priority = "Important"
        return priority


class DonationProgress(models.Model):
    PENDING = 0
    DONE = 1
    DONATION_PROGRESS_CHOICES = (
        (PENDING, 'Pending'),
        (DONE, 'Completed'),
    )
    MANAGED_ON_SITE = 0
    MANAGED_OUTSIDE = 1
    DONATION_MANAGEMENT_CHOICES = (
        (MANAGED_ON_SITE, 'Managed on site'),
        (MANAGED_OUTSIDE, 'Managed on somewhere else'),
    )
    donation = models.OneToOneField(Donation, on_delete=models.CASCADE,
                                    unique=True, related_name='donation_progress', verbose_name='donation')
    progress_status = models.PositiveSmallIntegerField(
        choices=DONATION_PROGRESS_CHOICES, default=0, verbose_name='progress status')
    management_status = models.PositiveSmallIntegerField(
        blank=True, null=True, choices=DONATION_MANAGEMENT_CHOICES, verbose_name='managed on')
    details = models.TextField(max_length=500, blank=True,
                               null=True, verbose_name='details')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    class Meta:
        verbose_name = ("Donation Progress")
        verbose_name_plural = ("Donation Progresses")
        ordering = ["-updated_at"]

    def __str__(self):
        return self.donation.title

    def get_progress_status(self):
        progress_status = "Undefined"
        if self.progress_status == 0:
            progress_status = "Pending"
        if self.progress_status == 1:
            progress_status = "Completed"
        return progress_status


def donation_slug_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(donation_slug_pre_save_receiver, sender=Donation)


@receiver(post_save, sender=Donation)
def create_donation_progress(sender, instance, created, **kwargs):
    if created:
        DonationProgress.objects.create(donation=instance)
