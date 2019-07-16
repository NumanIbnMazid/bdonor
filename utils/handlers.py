from .models import Notification
import datetime


def create_notification(request, sender, receiver, category, identifier, subject, message):
    qs = Notification.objects.filter(
        category__iexact=category, identifier__iexact=category)
    if qs.exists():
        qs.update(sender=sender, receiver=receiver, subject=subject,
                  message=message, updated_at=datetime.datetime.now())
    else:
        Notification.objects.create(
            sender=sender, receiver=receiver, category=category, identifier=identifier, subject=subject, message=message
        )
    pass
