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
