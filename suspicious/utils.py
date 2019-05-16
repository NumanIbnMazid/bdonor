from uuid import getnode as get_mac
from .models import Suspicious
import datetime
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def block_suspicious_user(request):
    instance_user = request.user
    suspicious_users_filter = Suspicious.objects.filter(user=instance_user)
    if suspicious_users_filter.exists():
        suspicious_user_instance = suspicious_users_filter.first()
        current_attempt = suspicious_user_instance.attempt
        total_attempt = current_attempt + 1
        update_time = datetime.datetime.now()
        suspicious_users_filter.update(
            attempt=total_attempt, last_attempt=update_time)
    else:
        client_ip = get_client_ip(request)
        client_mac = get_mac()
        Suspicious.objects.create(
            user=instance_user, ip=client_ip, mac=client_mac)
    messages.add_message(request, messages.ERROR,
                         "You are not allowed. Your account is being tracked for suspicious activity !"
                         )
    pass
