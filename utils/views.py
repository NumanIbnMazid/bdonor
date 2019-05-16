from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse
from accounts.models import UserProfile
from utils.models import SitePreference
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
import datetime
# Method Decorator imports
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class SitePreferenceView(TemplateView):
    def get(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.filter(user=request.user).first()
        site_preference_filter = SitePreference.objects.filter(
            user=user_profile)
        if site_preference_filter.exists():
            context = {
                'site_preference': site_preference_filter.first()
            }
        else:
            context = {
                'site_preference': None
            }
        return render(request, "site-preference/preference.html", context=context)


@login_required
def change_site_preference(request):
    url = reverse('home')
    if request.method == "POST":
        now = datetime.datetime.now()
        logo_header = request.POST.get('logo-header')
        navbar_header = request.POST.get('navbar-header')
        sidebar_header = request.POST.get('sidebar-header')
        background_color = request.POST.get('background-color')
        sidebar_type = request.POST.get('sidebar-type')
        scroll_to_top = request.POST.get('scroll-to-top')
        user_profile = UserProfile.objects.filter(user=request.user).first()
        site_preference_filter = SitePreference.objects.filter(
            user=user_profile)
        if site_preference_filter.exists():
            site_preference_filter.update(
                logo_header_color=logo_header,
                navbar_header_color=navbar_header,
                sidebar_color=sidebar_header,
                background_color=background_color,
                sidebar_type=sidebar_type,
                scroll_to_top=scroll_to_top,
                updated_at=now
            )
        else:
            SitePreference.objects.create(
                user=user_profile,
                logo_header_color=logo_header,
                navbar_header_color=navbar_header,
                sidebar_color=sidebar_header,
                background_color=background_color,
                sidebar_type=sidebar_type,
                scroll_to_top=scroll_to_top
            )
        url = reverse('utils:site_preference')
        messages.add_message(request, messages.SUCCESS,
                             "Site preference changed successfully!")
    return HttpResponseRedirect(url)


@login_required
def change_site_preference_default(request):
    url = reverse('home')
    user_profile = UserProfile.objects.filter(user=request.user).first()
    site_preference_filter = SitePreference.objects.filter(
        user=user_profile)
    if site_preference_filter.exists():
        site_preference_filter.delete()
    url = reverse('utils:site_preference')
    messages.add_message(request, messages.SUCCESS,
                         "Site preference changed to default!")
    return HttpResponseRedirect(url)
