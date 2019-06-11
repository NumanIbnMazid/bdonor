from django import template
from utils.models import SitePreference
from accounts.models import UserProfile
from chat.models import ChatMessage, Thread
from django.db.models import Q
import datetime


register = template.Library()


@register.simple_tag(takes_context=True)
def get_site_preference(context):
    request = context['request']
    user_profile_filter = UserProfile.objects.filter(user=request.user)
    if user_profile_filter.exists():
        qs = SitePreference.objects.filter(user=user_profile_filter.first())
        if qs.exists():
            return qs.first()
    return None


@register.simple_tag(takes_context=True)
def get_datetime_tag(context):
    return datetime.datetime.now()


@register.simple_tag(takes_context=True)
def get_chat_messages(context):
    request = context['request']
    qs = ChatMessage.objects.filter(Q(thread__first=request.user) | Q(thread__second=request.user))
    if qs.exists():
        return qs.order_by('-timestamp')
    return None

@register.simple_tag(takes_context=True)
def get_threads(context):
    request = context['request']
    qs = Thread.objects.filter(Q(first=request.user) | Q(second=request.user))
    if qs.exists():
        return qs.order_by('-updated_at')
    return None