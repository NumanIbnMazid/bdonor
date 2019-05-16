from django import template
from utils.models import SitePreference
from accounts.models import UserProfile
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
