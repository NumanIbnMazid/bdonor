from django.db import models
from accounts.utils import unique_slug_generator
from django.db.models.signals import pre_save

PLAN_EXPIRATION_CYCLE_CHOICES = [
    (1, '1 Month'),
    (2, '2 Month'),
    (3, '3 Month'),
    (4, '4 Month'),
    (5, '5 Month'),
    (6, '6 Month'),
    (7, '7 Month'),
    (8, '8 Month'),
    (9, '9 Month'),
    (10, '10 Month'),
    (11, '11 Month'),
    (12, '12 Month')
]

CURRENCY_CHOICES = [
    ('USD', 'usd'),
]


class Plan(models.Model):

    # ONE = 1
    # TWO = 2
    # THREE = 3
    # FOUR = 4
    # FIVE = 5
    # SIX = 6
    # SEVEN = 7
    # EIGHT = 8
    # NINE = 9
    # TEN = 10
    # ELEVEN = 11
    # TWELVE = 12
    # PLAN_EXPIRATION_CYCLE_CHOICES = (
    #     (ONE, '1 Month'),
    #     (TWO, '2 Month'),
    #     (THREE, '3 Month'),
    #     (FOUR, '4 month'),
    #     (FIVE, '5 month'),
    #     (SIX, '6 month'),
    #     (SEVEN, '7 month'),
    #     (EIGHT, '8 month'),
    #     (NINE, '9 month'),
    #     (TEN, '10 month'),
    #     (ELEVEN, '11 month'),
    #     (TWELVE, '12 month'),
    # )

    title = models.CharField(max_length=100, verbose_name='plan title')
    slug = models.SlugField(unique=True, verbose_name='slug')
    amount = models.PositiveIntegerField(default=0, verbose_name='amount')
    currency = models.CharField(
        max_length=50, choices=CURRENCY_CHOICES, default='usd', verbose_name='currency')
    expiration_cycle = models.PositiveSmallIntegerField(
        choices=PLAN_EXPIRATION_CYCLE_CHOICES, default=1, verbose_name='expiration cycle')
    description = models.TextField(max_length=100, blank=True, null=True, verbose_name='short description')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    class Meta:
        verbose_name = ("Plan")
        verbose_name_plural = ("Plans")
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


def plan_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(plan_pre_save_receiver, sender=Plan)
