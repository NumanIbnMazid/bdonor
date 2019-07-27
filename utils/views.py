from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse
from accounts.models import UserProfile
from .models import SitePreference, Location
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
import datetime
# Method Decorator imports
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# autocomplete
import json
from django.db.models import Count


@method_decorator(login_required, name='dispatch')
class SitePreferenceView(TemplateView):
    def get(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.filter(user=request.user).first()
        site_preference_filter = SitePreference.objects.filter(
            user=user_profile)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin/base.html'
        else:
            base_template = 'base.html'
        # Ends Base Template Context
        if site_preference_filter.exists():
            context = {
                'site_preference': site_preference_filter.first(),
                'base_template': base_template
            }
        else:
            context = {
                'site_preference': None,
                'base_template': base_template
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
        chat_with_others = request.POST.get('chat-with-others')
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
                chat_with_others=chat_with_others,
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
                scroll_to_top=scroll_to_top,
                chat_with_others=chat_with_others
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
        SitePreference.objects.create(user=user_profile)
    url = reverse('utils:site_preference')
    messages.add_message(request, messages.SUCCESS,
                         "Site preference changed to default!")
    return HttpResponseRedirect(url)


@login_required
def address_autocomplete_view(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        places = Location.objects.filter(location__icontains=q, location_type=0).annotate(
            hit_count=Count('hit')).order_by('-hit_count')
        results = []
        for pl in places:
            place_json = {}
            place_json = pl.location
            results.append(place_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


@login_required
def hospital_autocomplete_view(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        places = Location.objects.filter(
            location__icontains=q, location_type=1).annotate(
            hit_count=Count('hit')).order_by('-hit_count')
        results = []
        for pl in places:
            place_json = {}
            place_json = pl.location
            results.append(place_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
