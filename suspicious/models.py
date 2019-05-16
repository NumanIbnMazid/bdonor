from django.db import models
from django.conf import settings


class Suspicious(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='suspicious', verbose_name=('user')
    )
    attempt = models.PositiveSmallIntegerField(
        default=1, verbose_name=('attempt'))
    first_attempt = models.DateTimeField(
        auto_now_add=True, verbose_name=('first attempt'))
    last_attempt = models.DateTimeField(
        auto_now=True, verbose_name=('last attempt'))
    ip = models.CharField(
        max_length=150, verbose_name='ip address', blank=True, null=True)
    mac = models.CharField(
        max_length=150, verbose_name='mac address', blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = ("Suspicious User")
        verbose_name_plural = ("Suspicious Users")
        ordering = ["-last_attempt"]
