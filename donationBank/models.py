from django.db import models
from django_countries.fields import CountryField
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from accounts.utils import unique_slug_generator, time_str_mix_slug
from django.template.defaultfilters import slugify
from middlewares.middlewares import RequestMiddleware


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
    bank = models.OneToOneField(
        DonationBank, on_delete=models.CASCADE, related_name='bank_setting', unique=True, verbose_name='bank')
    member_request = models.PositiveSmallIntegerField(
        choices=MEMBER_REQUEST_STATUS_CHOICES, default=0, verbose_name='member request')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    class Meta:
        verbose_name = ("DonationBankSetting")
        verbose_name_plural = ("DonationBankSettings")
        ordering = ["-created_at"]

    def __str__(self):
        return self.bank.institute


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
    gender = models.CharField(choices=GENDER_CHOICES, blank=True,
                              null=True, max_length=10, verbose_name='gender')
    dob = models.DateField(blank=True, null=True, verbose_name='DOB')
    blood_group = models.CharField(
        max_length=10, choices=BLOOD_GROUP_CHOICES, verbose_name='blood group')
    deseases = models.CharField(
        max_length=250, blank=True, null=True, verbose_name='deseases (If any)')
    contact = models.CharField(
        max_length=20, blank=True, null=True, verbose_name='contact')
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
        default=1, verbose_name='quantity')
    description = models.TextField(
        max_length=1000, blank=True, null=True, verbose_name='description')
    collection_date = models.DateTimeField(verbose_name='collection date')
    expiration_date = models.DateTimeField(verbose_name='expiration date')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    class Meta:
        verbose_name = ("Donation")
        verbose_name_plural = ("Donations")
        ordering = ["-updated_at"]

    def __str__(self):
        full_name = self.last_name
        if not self.first_name == None and not self.last_name == None:
            full_name = self.first_name + " " + self.last_name
        return full_name


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
    first_name = models.CharField(blank=True, null=True, max_length=50, verbose_name='first name')
    last_name = models.CharField(blank=True, null=True, max_length=50, verbose_name='last name')
    email = models.EmailField(blank=True, null=True, verbose_name='email')
    gender = models.CharField(choices=GENDER_CHOICES, blank=True,
                              null=True, max_length=10, verbose_name='gender')
    blood_group = models.CharField(
        blank=True, null=True, max_length=10, choices=BLOOD_GROUP_CHOICES, verbose_name='blood group')
    address = models.CharField(blank=True, null=True, max_length=250, verbose_name='address')
    city = models.CharField(blank=True, null=True, max_length=100, verbose_name='city')
    state = models.CharField(blank=True, null=True, max_length=100, verbose_name='state/province')
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
        return self.donation.donation_type

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
        slug_binding = slugify(institute) + "-" + instance.id + "_" + time_str_mix_slug()
        # print(slug_binding)
        instance.slug = slug_binding


pre_save.connect(donation_slug_pre_save_receiver, sender=Donation)


@receiver(post_save, sender=Donation)
def create_donation_progress(sender, instance, created, **kwargs):
    if created:
        DonationProgress.objects.create(donation=instance)
