from django.db import models
from django.conf import settings
from priceplan.models import Plan

# Create your models here.


class Checkout(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='user_checkout', verbose_name='user')
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, verbose_name='plan')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    # created_at = models.DateTimeField(verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    class Meta:
        verbose_name = ("Checkout")
        verbose_name_plural = ("Checkouts")
        ordering = ["-user__date_joined"]

    def __str__(self):
        return self.user.username
