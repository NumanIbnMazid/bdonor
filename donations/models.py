from django.db import models
from accounts.models import UserProfile
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from accounts.utils import unique_slug_generator, time_str_mix_slug
from django.core.validators import RegexValidator
import datetime
from django.db.models import Q
from django.urls import reverse
from django.http import Http404
from middlewares.middlewares import RequestMiddleware
from django_countries.fields import CountryField


class DonationQuerySet(models.query.QuerySet):
    def offers(self):
        return self.filter(category=0)

    def requests(self):
        return self.filter(category=1)

    def blood_type(self):
        return self.filter(type=0)

    def organ_type(self):
        return self.filter(type=1)

    def tissue_type(self):
        return self.filter(type=2)
    
    def living_donates(self):
        return self.filter(donate_type=0)
    
    def deceased_donates(self):
        return self.filter(donate_type=1)

    def is_published(self):
        return self.filter(publication_status=0)

    def is_not_published(self):
        return self.filter(publication_status=1)

    def is_verified(self):
        return self.filter(is_verified=True)

    def is_not_verified(self):
        return self.filter(is_verified=False)

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

    def priority_sort(self):
        return self.filter().order_by('priority')

    def is_normal(self):
        return self.filter(priority=0)

    def dynamic_order(self):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        if request.user.is_authenticated and not request.user.profile.country == None:
            from django_countries import countries
            user_country = request.user.profile.country.name
            countries_dict = dict(countries)
            order_field = list(countries_dict.values())
            order_field.remove(user_country)
            order_field.insert(0, user_country)
            # print(order_field)
            # pre_qs = self.filter(country=order_field)
            qs = sorted(self.filter().order_by('-created_at'),
                        key=lambda p: order_field.index(p.country.name))
        else:
            qs = self.filter().order_by('-created_at')
        return qs

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
                   Q(category__icontains=query) |
                   Q(type__icontains=query) |
                   Q(tissue_name__icontains=query) |
                   Q(blood_group__icontains=query) |
                   Q(blood_bag__icontains=query) |
                   Q(quantity__icontains=query) |
                   Q(organ_name__icontains=query) |
                   Q(details__icontains=query) |
                   Q(contact__icontains=query) |
                   Q(contact2__icontains=query) |
                   Q(contact3__icontains=query) |
                   Q(location__icontains=query) |
                   Q(city__icontains=query) |
                   Q(state__icontains=query) |
                   Q(country__icontains=query) |
                   Q(hospital__icontains=query) |
                   Q(preferred_date__icontains=query) |
                   Q(preferred_date_from__icontains=query) |
                   Q(preferred_date_to__icontains=query) |
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

    def get_by_slug(self, slug, request):
        try:
            instance = self.get_queryset().get(slug=slug)
        except Donation.DoesNotExist:
            raise Http404("Not Found !!!")
        except Donation.MultipleObjectsReturned:
            qs = self.get_queryset().filter(slug=slug)
            instance = qs.first()
        except:
            raise Http404("Something went wrong !!!")
        # Manage DonationUtil Object
        if instance.user.user != request.user:
            donation_utils_filter = DonationUtil.objects.filter(
                donation=instance, user=request.user)
            if donation_utils_filter.exists():
                donation_utils_filter.update(
                    updated_at=datetime.datetime.now())
            else:
                DonationUtil.objects.create(
                    donation=instance, user=request.user)
        return instance

    def search(self, query):
        return self.get_queryset().search(query)


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
    ORGAN = 1
    TISSUE = 2
    DONATION_CHOICES = (
        (BLOOD, 'Blood'),
        (ORGAN, 'Organ'),
        (TISSUE, 'Tissue'),
    )
    ANY = 'Any Blood Group'
    A_POSITIVE = 'A+'
    A_NEGATIVE = 'A-'
    B_POSITIVE = 'B+'
    B_NEGATIVE = 'B-'
    O_POSITIVE = 'O+'
    O_NEGATIVE = 'O-'
    AB_POSITIVE = 'AB+'
    AB_NEGATIVE = 'AB-'
    BLOOD_GROUP_CHOICES = (
        (ANY, 'Any Blood Group'),
        (A_POSITIVE, 'A+'),
        (A_NEGATIVE, 'A-'),
        (B_POSITIVE, 'B+'),
        (B_NEGATIVE, 'B-'),
        (O_POSITIVE, 'O+'),
        (O_NEGATIVE, 'O-'),
        (AB_POSITIVE, 'AB+'),
        (AB_NEGATIVE, 'AB-')
    )
    HEART = 'Heart'
    KIDNEY = 'Kidney'
    PANCREAS = 'Pancreas'
    LUNGS = 'Lungs'
    LIVER = 'Liver'
    INTESTINES = 'Intestines'
    ORGAN_CHOICES = (
        (HEART, 'Heart'),
        (KIDNEY, 'Kidney'),
        (PANCREAS, 'Pancreas'),
        (LUNGS, 'Lungs'),
        (LIVER, 'Liver'),
        (INTESTINES, 'Intestines')
    )
    BONES = 'Bones'
    LIGAMENTS = 'Ligaments'
    TENDONS = 'Tendons'
    FASCIA = 'Fascia'
    VEINS = 'Veins'
    NERVES = 'Nerves'
    CORNEAS = 'Corneas'
    SCLERA = 'Sclera'
    HEART_VALVES = 'Heart Valves'
    SKIN = 'Skin'
    TISSUE_CHOICES = (
        (BONES, 'Bones'),
        (LIGAMENTS, 'Ligaments'),
        (TENDONS, 'Tendons'),
        (FASCIA, 'Fascia'),
        (VEINS, 'Veins'),
        (NERVES, 'Nerves'),
        (CORNEAS, 'Corneas'),
        (SCLERA, 'Sclera'),
        (HEART_VALVES, 'Heart Valves'),
        (SKIN, 'Skin')
    )
    LIVING = 0
    DECEASED = 1
    DONATE_TYPE_CHOICES = (
        (LIVING, 'Living'),
        (DECEASED, 'Deceased')
    )
    PUBLIC = 0
    PRIVATE = 1
    CONTACT_PRIVACY_CHOICES = (
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
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
        choices=DONATION_CHOICES, default=0, verbose_name='donation type')
    blood_group = models.CharField(
        max_length=20, choices=BLOOD_GROUP_CHOICES, null=True, blank=True, verbose_name='blood group')
    blood_bag = models.CharField(
        blank=True, null=True, max_length=4, verbose_name='blood bag quantity')
    organ_name = models.CharField(
        choices=ORGAN_CHOICES, blank=True, max_length=100, null=True, verbose_name='organ name')
    tissue_name = models.CharField(
        choices=TISSUE_CHOICES, blank=True, max_length=100, null=True, verbose_name='tissue name')
    quantity = models.CharField(
        blank=True, null=True, max_length=4, verbose_name='quantity')
    donate_type = models.PositiveSmallIntegerField(
        choices=DONATE_TYPE_CHOICES, default=0, verbose_name='donate type')
    is_verified = models.BooleanField(default=True, verbose_name='is verified')
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
    contact_privacy = models.PositiveSmallIntegerField(
        choices=CONTACT_PRIVACY_CHOICES, default=0, verbose_name='contact privacy')
    location = models.CharField(max_length=200, verbose_name='location')
    city = models.CharField(max_length=100, verbose_name='city')
    state = models.CharField(blank=True, null=True,
                             max_length=100, verbose_name='state/province')
    country = CountryField()
    hospital = models.CharField(
        max_length=200, null=True, blank=True, verbose_name='hospital')
    preferred_date = models.DateTimeField(
        verbose_name='preferred date', blank=True, null=True)
    preferred_date_from = models.DateTimeField(
        verbose_name='preferred date from', blank=True, null=True)
    preferred_date_to = models.DateTimeField(
        verbose_name='preferred date to', blank=True, null=True)
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
            type = "Tissue"
        return type

    def get_type_dynamic_short_detail(self):
        detail = "Undefined"
        if self.type == 0:
            detail = f"{self.blood_group} ({self.blood_bag} bag)"
        if self.type == 1:
            detail = f"{self.organ_name} ({self.quantity})"
        if self.type == 2:
            detail = f"{self.tissue_name}"
        return detail

    def get_priority(self):
        priority = "Undefined"
        if self.priority == 0:
            priority = "Normal"
        if self.priority == 1:
            priority = "Important"
        return priority

    def get_viewers(self):
        qs = DonationUtil.objects.filter(donation=self)
        return qs

    def get_respondents(self):
        qs = self.donation_respond.all()
        return qs

    def has_response(self):
        response = False
        qs = self.donation_respond.all()
        if qs.count() > 0:
            response = True
        return response

    def is_virtually_verified(self):
        virtual_verified = True
        if self.donate_type == 0:
            virtual_verified = False
        elif self.donate_type == 1 and self.is_verified == False:
            virtual_verified = False
        else:
            virtual_verified = True
        return virtual_verified


    def get_user_is_responded(self):
        # First we need create an instance of that and later get the current_request assigned
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        qs = self.donation_respond.filter(respondent=request.user)
        if qs.exists():
            return True
        return False

    def is_modifiable(self):
        is_modifiable = True
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        has_response = self.has_response()
        is_virtually_verified = self.is_virtually_verified()
        if self.user.user == request.user and self.donation_progress.progress_status == 0 and has_response == False and is_virtually_verified == False:
            is_modifiable = True
        else:
            is_modifiable = False
        return is_modifiable


class DonationRespond(models.Model):
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE,
                                 related_name='donation_respond', verbose_name='donation')
    respondent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='donation_respondent', verbose_name='respondent')
    contact = models.CharField(blank=True, null=True, max_length=17, verbose_name='contact')
    message = models.TextField(max_length=500, blank=True, null=True, verbose_name='message')
    is_selected = models.BooleanField(default=False, verbose_name='is selected')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    class Meta:
        verbose_name = ("Donation Respond")
        verbose_name_plural = ("Donation Responds")
        ordering = ["-updated_at"]

    def __str__(self):
        return self.donation.title

    def get_contact(self):
        contact = "Not Provided"
        if not self.contact == "":
            contact = self.contact
        return contact

    def get_message(self):
        message = "Not Provided"
        if not self.message == "":
            message = self.message
        return message


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
        (MANAGED_ON_SITE, 'BDonar'),
        (MANAGED_OUTSIDE, 'Somewhere else'),
    )
    donation = models.OneToOneField(Donation, on_delete=models.CASCADE,
                                    unique=True, related_name='donation_progress', verbose_name='donation')
    progress_status = models.PositiveSmallIntegerField(
        choices=DONATION_PROGRESS_CHOICES, default=0, verbose_name='progress status')
    respondent = models.ForeignKey(DonationRespond, on_delete=models.CASCADE, blank=True, null=True,
                                   related_name='donation_progress_respondent', verbose_name='respondent')
    completion_date = models.DateField(
        blank=True, null=True, verbose_name='completion date')
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

    def get_donation_user(self):
        return self.donation.user

    def get_progress_status(self):
        progress_status = "Undefined"
        if self.progress_status == 0:
            progress_status = "Pending"
        if self.progress_status == 1:
            progress_status = "Completed"
        return progress_status

    def get_management_status(self):
        management_status = "Undefined"
        if self.management_status == 0:
            management_status = "Managed on site"
        if self.management_status == 1:
            management_status = "Managed on somewhere else"
        return management_status


class DonationUtil(models.Model):
    donation = models.ForeignKey(
        Donation, on_delete=models.CASCADE, related_name='donation_util', verbose_name='donation')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='donation_util_user', verbose_name='user')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created_at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated_at')

    class Meta:
        verbose_name = ("Donation Util")
        verbose_name_plural = ("Donation Utils")
        ordering = ["-updated_at"]

    def __str__(self):
        return self.donation.title


def donation_slug_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        user = instance.user.user.username.lower()
        donation_type = str(instance.type)
        post_category = str(instance.category)
        slug_binding = user + "_" + post_category + "-" + donation_type + "-" + time_str_mix_slug()
        instance.slug = slug_binding


pre_save.connect(donation_slug_pre_save_receiver, sender=Donation)


@receiver(post_save, sender=Donation)
def create_donation_progress(sender, instance, created, **kwargs):
    if created:
        DonationProgress.objects.create(donation=instance)
