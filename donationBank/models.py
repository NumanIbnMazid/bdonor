from django.db import models
from django_countries.fields import CountryField
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from accounts.utils import unique_slug_generator, time_str_mix_slug, upload_campaign_image_path
from django.template.defaultfilters import slugify
from middlewares.middlewares import RequestMiddleware
from django.db.models import Q
import datetime
from django.urls import reverse
from django.http import Http404
from django.db.models import F, Sum


class DonationBankQuerySet(models.query.QuerySet):
    def banks_by_user(self):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        qs = self.filter(bank_member__user=self.request.user)
        if qs.exists():
            return qs
        return None

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

    def banks_current_year(self):
        today = datetime.datetime.now()
        return self.filter(created_at__year=today.year)

    def banks_by_year(self, year_search):
        return self.filter(created_at__year=year_search)

    # Foreign

    def is_public(self):
        return self.filter(bank_setting__privacy=0)
    
    def is_private(self):
        return self.filter(bank_setting__privacy=1)

    def search(self, query):
        lookups = (Q(institute__icontains=query) |
                   Q(address__icontains=query) |
                   Q(city__icontains=query) |
                   Q(state__icontains=query) |
                   Q(country__icontains=query) |
                   Q(contact__icontains=query) |
                   Q(email__icontains=query) |
                   Q(description__icontains=query))
        return self.filter(lookups).distinct()


class DonationBankManager(models.Manager):
    def get_queryset(self):
        return DonationBankQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset()

    def get_by_id(self, id):
        try:
            instance = self.get_queryset().get(id=id)
        except DonationBank.DoesNotExist:
            raise Http404("Not Found !!!")
        except DonationBank.MultipleObjectsReturned:
            qs = self.get_queryset().filter(id=id)
            instance = qs.first()
        except:
            raise Http404("Something went wrong !!!")
        return instance

    def get_by_slug(self, slug):
        try:
            instance = self.get_queryset().get(slug=slug)
        except DonationBank.DoesNotExist:
            raise Http404("Not Found !!!")
        except DonationBank.MultipleObjectsReturned:
            qs = self.get_queryset().filter(slug=slug)
            instance = qs.first()
        except:
            raise Http404("Something went wrong !!!")
        return instance

    def search(self, query):
        return self.get_queryset().search(query)


class DonationBank(models.Model):
    institute = models.CharField(max_length=100, verbose_name='institute name')
    slug = models.SlugField(unique=True, verbose_name='slug')
    address = models.CharField(max_length=250, verbose_name='address')
    city = models.CharField(max_length=100, verbose_name='city')
    state = models.CharField(max_length=100, blank=True,
                             null=True, verbose_name='state/province')
    # country = models.CharField(max_length=100, verbose_name='country')
    country = CountryField()
    contact = models.CharField(max_length=100, verbose_name='contact no.')
    email = models.EmailField(blank=True, null=True, verbose_name='email')
    description = models.TextField(
        max_length=1000, blank=True, null=True, verbose_name='description')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    objects = DonationBankManager()

    class Meta:
        verbose_name = ("DonationBank")
        verbose_name_plural = ("DonationBanks")
        ordering = ["-created_at"]

    def __str__(self):
        return self.institute


class DonationBankSetting(models.Model):
    ALLOW = 0
    NOT_ALLOW = 1
    MEMBER_REQUEST_STATUS_CHOICES = (
        (ALLOW, 'Allow'),
        (NOT_ALLOW, 'Not Allow')
    )
    PUBLIC = 0
    PRIVATE = 1
    BANK_PRIVACY_CHOICES = (
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private')
    )
    bank = models.OneToOneField(
        DonationBank, on_delete=models.CASCADE, related_name='bank_setting', unique=True, verbose_name='bank')
    member_request = models.PositiveSmallIntegerField(
        choices=MEMBER_REQUEST_STATUS_CHOICES, default=0, verbose_name='member request')
    privacy = models.PositiveSmallIntegerField(
        choices=BANK_PRIVACY_CHOICES, default=0, verbose_name='privacy')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    class Meta:
        verbose_name = ("DonationBankSetting")
        verbose_name_plural = ("DonationBankSettings")
        ordering = ["-created_at"]

    def __str__(self):
        return self.bank.institute

    def get_privacy_status(self):
        status = "Undefined"
        if self.privacy == 0:
            status = "Public"
        if self.privacy == 1:
            status = "Private"
        return status
    
    def get_member_request_status(self):
        status = "Undefined"
        if self.member_request == 0:
            status = "Allowed"
        if self.member_request == 1:
            status = "Not Allowed"
        return status


class BankMember(models.Model):
    CREATOR = 0
    MAINTAINER = 1
    MEMBERSHIP_ROLE_CHOICES = (
        (CREATOR, 'Creator'),
        (MAINTAINER, 'Maintainer')
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='user_bank_member', verbose_name='user')
    bank = models.ForeignKey(DonationBank, on_delete=models.CASCADE,
                             related_name='bank_member', verbose_name='bank')
    role = models.PositiveSmallIntegerField(
        choices=MEMBERSHIP_ROLE_CHOICES, default=1, verbose_name='member role')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    class Meta:
        verbose_name = ("BankMember")
        verbose_name_plural = ("BankMembers")
        ordering = ["-created_at"]

    def __str__(self):
        return self.user.username

    def get_bank_member_role(self):
        role = 'Undefined'
        if self.role == 0:
            role = 'Creator'
        if self.role == 1:
            role = 'Maintainer'
        return role


class MemberRequest(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                unique=True, related_name='user_member_request', verbose_name='user'
                                )
    bank = models.ForeignKey(
        DonationBank, related_name='bank_member_request', on_delete=models.CASCADE, verbose_name='bank')
    slug = models.SlugField(unique=True, verbose_name='slug')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    class Meta:
        verbose_name = ("MemberRequest")
        verbose_name_plural = ("MemberRequests")
        ordering = ["-created_at"]

    def __str__(self):
        return self.user.username


class CampaignQuerySet(models.query.QuerySet):
    def campaigns_by_user_bank(self):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        qs = self.filter(bank__bank_member__user=self.request.user)
        if qs.exists():
            return qs
        return None

    def is_not_expired(self):
        qs = self.filter(Q(held_date__gte=datetime.datetime.now())
                         | Q(end_date__gte=datetime.datetime.now()))
        return qs

    def is_expired(self):
        qs = self.filter(Q(held_date__lt=datetime.datetime.now())
                         | Q(end_date__lt=datetime.datetime.now()))
        return qs

    def held_date_not_expired(self):
        qs = self.filter(held_date__gte=datetime.datetime.now())
        return qs

    def held_date_expired(self):
        qs = self.filter(held_date__lt=datetime.datetime.now())
        return qs

    def end_date_not_expired(self):
        qs = self.filter(end_date__gte=datetime.datetime.now())
        return qs

    def end_date_expired(self):
        qs = self.filter(end_date__lt=datetime.datetime.now())
        return qs

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

    def campaigns_current_year(self):
        today = datetime.datetime.now()
        return self.filter(created_at__year=today.year)

    def campaigns_by_year(self, year_search):
        return self.filter(created_at__year=year_search)

    # Foreign
    def bank_is_public(self):
        return self.filter(bank__bank_setting__privacy=0)
    
    def bank_is_private(self):
        return self.filter(bank__bank_setting__privacy=1)

    def search(self, query):
        lookups = (Q(bank__institute__icontains=query) |
                   Q(bank__address__icontains=query) |
                   Q(bank__city__icontains=query) |
                   Q(bank__state__icontains=query) |
                   Q(bank__country__icontains=query) |
                   Q(bank__contact__icontains=query) |
                   Q(bank__email__icontains=query) |
                   Q(bank__description__icontains=query) |
                   Q(title__icontains=query) |
                   Q(held_date__icontains=query) |
                   Q(end_date__icontains=query) |
                   Q(contact__icontains=query) |
                   Q(email__icontains=query) |
                   Q(address__icontains=query) |
                   Q(city__icontains=query) |
                   Q(state__icontains=query) |
                   Q(country__icontains=query) |
                   Q(details__icontains=query))
        return self.filter(lookups).distinct()


class CampaignManager(models.Manager):
    def get_queryset(self):
        return CampaignQuerySet(self.model, using=self._db)

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
        except Campaign.DoesNotExist:
            raise Http404("Not Found !!!")
        except Campaign.MultipleObjectsReturned:
            qs = self.get_queryset().filter(slug=slug)
            instance = qs.first()
        except:
            raise Http404("Something went wrong !!!")
        return instance

    def filter_by_bank_slug(self, slug):
        try:
            instance = self.get_queryset().filter(bank__slug=slug)
        except:
            raise Http404("Something went wrong !!!")
        return instance

    def search(self, query):
        return self.get_queryset().search(query)


class Campaign(models.Model):
    bank = models.ForeignKey(
        DonationBank, on_delete=models.CASCADE, related_name='bank_campaign', verbose_name='bank'
    )
    title = models.CharField(max_length=150, verbose_name='campaign name')
    slug = models.SlugField(unique=True, verbose_name='slug')
    held_date = models.DateTimeField(verbose_name='held date')
    end_date = models.DateTimeField(verbose_name='end date')
    contact = models.CharField(max_length=20, verbose_name='contact')
    email = models.EmailField(blank=True, null=True, verbose_name='email')
    address = models.CharField(max_length=200, verbose_name='address')
    city = models.CharField(max_length=100, verbose_name='city')
    state = models.CharField(blank=True, null=True,
                             max_length=100, verbose_name='state/province')
    country = CountryField()
    details = models.TextField(blank=True,
                               null=True, verbose_name='details/rules-regulations')
    image = models.ImageField(
        upload_to=upload_campaign_image_path, null=True, blank=True, verbose_name='image/banner')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    objects = CampaignManager()

    class Meta:
        verbose_name = ("Campaign")
        verbose_name_plural = ("Campaigns")
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title

    def get_held_date_remaining(self):
        remaining_days = 0
        if not self.held_date == None:
            remaining_days = int(
                (self.held_date - datetime.datetime.now()).days)
        return remaining_days

    def get_end_date_remaining(self):
        remaining_days = 0
        if not self.end_date == None:
            remaining_days = int(
                (self.end_date - datetime.datetime.now()).days)
        return remaining_days

    def get_volunteer_request(self):
        status = "Undefined"
        if self.volunteer_request == 0:
            status = "Allow"
        if self.volunteer_request == 1:
            status = "Don't Allow"
        return status


class DonationQuerySet(models.query.QuerySet):
    def blood_type(self):
        return self.filter(type=0)

    def organ_type(self):
        return self.filter(type=1)

    def tissue_type(self):
        return self.filter(type=2)

    def is_not_expired(self):
        qs = self.filter(expiration_date__gte=datetime.date.today())
        return qs

    def is_expired(self):
        qs = self.filter(expiration_date__lt=datetime.date.today())
        return qs

    # Foreign
    def is_done(self):
        return self.filter(donation_progress__progress_status=1)

    def is_pending(self):
        return self.filter(donation_progress__progress_status=0)
    # /Foreign

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
        lookups = (Q(bank__institute__icontains=query) |
                   Q(bank__address__icontains=query) |
                   Q(bank__city__icontains=query) |
                   Q(bank__state__icontains=query) |
                   Q(bank__country__icontains=query) |
                   Q(bank__contact__icontains=query) |
                   Q(bank__email__icontains=query) |
                   Q(bank__description__icontains=query) |
                   Q(first_name__icontains=query) |
                   Q(last_name__icontains=query) |
                   Q(gender__icontains=query) |
                   Q(dob__icontains=query) |
                   Q(diseases__icontains=query) |
                   Q(contact__icontains=query) |
                   Q(email__icontains=query) |
                   Q(address__icontains=query) |
                   Q(city__icontains=query) |
                   Q(state__icontains=query) |
                   Q(country__icontains=query) |
                   Q(donation_type__icontains=query) |
                   Q(tissue_name__icontains=query) |
                   Q(blood_group__icontains=query) |
                   Q(quantity__icontains=query) |
                   Q(organ_name__icontains=query) |
                   Q(description__icontains=query) |
                   Q(collection_date__icontains=query) |
                   Q(expiration_date__icontains=query) |
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

    def filter_by_bank_slug(self, slug):
        try:
            instance = self.get_queryset().filter(bank__slug=slug)
        except:
            raise Http404("Something went wrong !!!")
        return instance

    def search(self, query):
        return self.get_queryset().search(query)


class Donation(models.Model):
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
    BLOOD = 0
    ORGAN = 1
    TISSUE = 2
    DONATION_CHOICES = (
        (BLOOD, 'Blood'),
        (ORGAN, 'Organ'),
        (TISSUE, 'Tissue'),
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
    bank = models.ForeignKey(DonationBank, on_delete=models.CASCADE,
                             related_name='donation_bank_bank', verbose_name='bank')
    slug = models.SlugField(unique=True, verbose_name='slug')
    first_name = models.CharField(max_length=50, verbose_name='first name')
    last_name = models.CharField(max_length=50, verbose_name='last name')
    email = models.EmailField(blank=True, null=True, verbose_name='email')
    gender = models.CharField(choices=GENDER_CHOICES,
                              max_length=10, verbose_name='gender')
    dob = models.DateField(verbose_name='Date of Birth')
    blood_group = models.CharField(
        max_length=10, choices=BLOOD_GROUP_CHOICES, verbose_name='blood group')
    diseases = models.CharField(
        max_length=250, blank=True, null=True, verbose_name='diseases (If any)')
    contact = models.CharField(
        max_length=20, verbose_name='contact')
    address = models.CharField(max_length=250, verbose_name='address')
    city = models.CharField(max_length=100, verbose_name='city')
    state = models.CharField(max_length=100, blank=True,
                             null=True, verbose_name='state/province')
    country = CountryField()
    donation_type = models.PositiveSmallIntegerField(
        choices=DONATION_CHOICES, verbose_name='donation type')
    organ_name = models.CharField(
        choices=ORGAN_CHOICES, blank=True, max_length=100, null=True, verbose_name='organ name')
    tissue_name = models.CharField(
        choices=TISSUE_CHOICES, blank=True, max_length=100, null=True, verbose_name='tissue name')
    quantity = models.PositiveIntegerField(
        default=1, blank=True, null=True, verbose_name='quantity')
    description = models.TextField(
        max_length=1000, blank=True, null=True, verbose_name='description')
    collection_date = models.DateField(verbose_name='collection date')
    expiration_date = models.DateField(verbose_name='expiration date')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    objects = DonationManager()

    class Meta:
        verbose_name = ("Donation")
        verbose_name_plural = ("Donations")
        ordering = ["-updated_at"]

    def __str__(self):
        return self.bank.institute

    def get_donor_name(self):
        name = "Undefined"
        if not self.first_name == None and not self.last_name == None:
            name = self.first_name + " " + self.last_name
        return name

    def get_donor_age(self):
        age = 0
        if not self.dob == None:
            age = int((datetime.datetime.now().date() - self.dob).days / 365.25)
        return age

    def get_donation_type(self):
        donation_type = "Undefined"
        if self.donation_type == 0:
            donation_type = "Blood"
        if self.donation_type == 1:
            donation_type = "Organ"
        if self.donation_type == 2:
            donation_type = "Tissue"
        return donation_type

    def get_type_dynamic_short_detail(self):
        detail = "Undefined"
        if self.donation_type == 0:
            detail = f"{self.blood_group} ({self.quantity} bag)"
        if self.donation_type == 1:
            detail = f"{self.organ_name} ({self.quantity})"
        if self.donation_type == 2:
            detail = f"{self.tissue_name}"
        return detail

    def is_expired(self):
        status = False
        if not self.expiration_date == None and not self.donation_progress.progress_status == 1:
            today = datetime.date.today()
            if self.expiration_date < today:
                status = True
        return status

    def get_expiration_days(self):
        expired_in = 0
        if not self.expiration_date == None and not self.donation_progress.progress_status == 1:
            expired_in = int(
                (self.expiration_date - datetime.datetime.now().date()).days)
        return expired_in

    # def get_total_quantity(self):
    #     total = 0
    #     if self.donation_type == 0:
    #         qs = Donation.objects.filter(bank=self.bank, donation_type=0, blood_group=self.blood_group)
    #     elif self.donation_type == 1:
    #         qs = Donation.objects.filter(bank=self.bank, donation_type=1, organ_name=self.organ_name)
    #     elif self.donation_type == 2:
    #         qs = Donation.objects.filter(bank=self.bank, donation_type=2, tissue_name=self.tissue_name)
    #     else:
    #         qs = Donation.objects.filter(bank=self.bank, donation_type=self.donation_type)
    #     if qs.exists():
    #         total = qs.aggregate(total=Sum(F('quantity'))).get('total', 0)
    #     return total

    # def get_absolute_url(self):
    #     return reverse("donation_bank:bank_donation_details", kwargs={"slug": self.slug})


class DonationProgress(models.Model):
    PENDING = 0
    DONE = 1
    DONATION_PROGRESS_CHOICES = (
        (PENDING, 'Pending'),
        (DONE, 'Completed'),
    )
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
    donation = models.OneToOneField(Donation, on_delete=models.CASCADE,
                                    unique=True, related_name='donation_progress', verbose_name='donation')
    progress_status = models.PositiveSmallIntegerField(
        choices=DONATION_PROGRESS_CHOICES, default=0, verbose_name='progress status')
    completion_date = models.DateField(
        blank=True, null=True, verbose_name='completion date')
    first_name = models.CharField(
        blank=True, null=True, max_length=50, verbose_name='first name')
    last_name = models.CharField(
        blank=True, null=True, max_length=50, verbose_name='last name')
    gender = models.CharField(choices=GENDER_CHOICES, blank=True,
                              null=True, max_length=10, verbose_name='gender')
    blood_group = models.CharField(
        blank=True, null=True, max_length=10, choices=BLOOD_GROUP_CHOICES, verbose_name='blood group')
    dob = models.DateField(blank=True, null=True, verbose_name='Date of Birth')
    contact = models.CharField(
        blank=True, null=True, max_length=20, verbose_name='contact')
    email = models.EmailField(blank=True, null=True, verbose_name='email')
    address = models.CharField(
        blank=True, null=True, max_length=250, verbose_name='address')
    city = models.CharField(blank=True, null=True,
                            max_length=100, verbose_name='city')
    state = models.CharField(blank=True, null=True,
                             max_length=100, verbose_name='state/province')
    country = CountryField(blank=True, null=True)
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
        return self.donation.bank.institute

    def get_progress_status(self):
        progress_status = "Undefined"
        if self.progress_status == 0:
            progress_status = "Pending"
        if self.progress_status == 1:
            progress_status = "Completed"
        return progress_status


def donation_bank_slug_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        if len(instance.institute) > 10:
            institute = instance.institute.lower()[:10]
        else:
            institute = instance.institute.lower()
        slug_binding = slugify(institute) + "_" + time_str_mix_slug()
        # print(slug_binding)
        instance.slug = slug_binding


pre_save.connect(donation_bank_slug_pre_save_receiver, sender=DonationBank)


@receiver(post_save, sender=DonationBank)
def create_bank_post_save_module(sender, instance, created, **kwargs):
    if created:
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        BankMember.objects.create(user=request.user, bank=instance, role=0)
        DonationBankSetting.objects.create(bank=instance)


def donation_slug_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        if len(instance.bank.institute) > 10:
            institute = instance.bank.institute.lower()[:10]
        else:
            institute = instance.bank.institute.lower()
        if len(instance.last_name) > 5:
            last_name = instance.last_name.lower()[:5]
        else:
            last_name = instance.last_name.lower()
        slug_binding = slugify(institute) + "-" + \
            last_name + "_" + time_str_mix_slug()
        # print(slug_binding)
        instance.slug = slug_binding


pre_save.connect(donation_slug_pre_save_receiver, sender=Donation)


@receiver(post_save, sender=Donation)
def create_donation_progress(sender, instance, created, **kwargs):
    if created:
        DonationProgress.objects.create(donation=instance)


def campaign_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(campaign_pre_save_receiver, sender=Campaign)
