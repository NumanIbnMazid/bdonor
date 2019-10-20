from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from el_pagination.views import AjaxListView
from django.urls import reverse
from accounts.models import UserProfile
from .models import SitePreference, Location, Notification
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
import datetime
from django_countries.fields import CountryField
from django_countries import countries, Countries
# Method Decorator imports
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# autocomplete
import json
from django.db.models import Count
from suspicious.utils import block_suspicious_user
from suspicious.models import Suspicious
# Custom Decorators Starts
from accounts.decorators import (
    can_browse_required, can_donate_required, can_ask_for_a_donor_required,
    can_manage_bank_required, can_chat_required
)
# Custom Decorators Ends

decorators = [login_required, can_browse_required]


@method_decorator(decorators, name='dispatch')
class SitePreferenceView(TemplateView):
    def get(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.filter(user=request.user).first()
        site_preference_filter = SitePreference.objects.filter(
            user=user_profile)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
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
@can_browse_required
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
@can_browse_required
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
@can_browse_required
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
@can_browse_required
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



@login_required
@can_browse_required
def update_user_country(request):
    # if request.user.is_authenticated:
    if request.is_ajax():
        location = request.GET.get('location', None)
        # print(location)
        all_countries_list = list(countries)
        for code, name in list(countries):
            # print(f"{name} - {code}")
            if location == name:
                profile_qs = UserProfile.objects.filter(user=request.user)
                if profile_qs.exists():
                    instance = profile_qs.update(country=code)
                    # print(instance)
        data = {
            'location': UserProfile.objects.filter(country__iexact=location).exists()
        }
        return JsonResponse(data)
    # return None


@method_decorator(decorators, name='dispatch')
class NotificationListView(AjaxListView):
    template_name = 'notification/list.html'
    # paginate_by = 4
    # model = Notification
    page_template = 'notification/snippets/page-template-list.html'
    # context_object_name = 'objects'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        query = Notification.objects.filter(
            receiver=request.user).order_by('-updated_at')
        if query.exists():
            return query
        return None

    def get_context_data(self, **kwargs):
        context = super(NotificationListView,
                        self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        return context


@method_decorator(login_required, name='dispatch')
class NotificationDetailView(DetailView):
    template_name = 'notification/details.html'

    def get_object(self):
        slug = self.kwargs['slug']
        notification_filter = Notification.objects.filter(slug=slug)
        if notification_filter.exists():
            notification = notification_filter.first()
            if notification.is_seen == False:
                notification_filter.update(is_seen=True)
            return notification
        return None

    def user_passes_test(self, request):
        user = request.user
        self.object = self.get_object()
        if self.object.receiver == user:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        instance_user = self.request.user
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(NotificationDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(NotificationDetailView,
                        self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        return context


@login_required
@can_browse_required
def mark_all_as_read(request):
    user = request.user
    url = reverse('home')
    qs = Notification.objects.filter(receiver=user)
    if qs.exists():
        qs.update(is_seen=True)
        messages.add_message(request, messages.SUCCESS,
                             "All Notifications has been marked as read !"
                             )
        url = reverse('utils:notification_list')
    return HttpResponseRedirect(url)
