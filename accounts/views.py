from django.shortcuts import render
from django.views.generic import UpdateView, DetailView, ListView, CreateView
from .models import UserProfile, UserReport
from suspicious.utils import block_suspicious_user
from .forms import UserProfileUpdateForm, UserReportManageForm
from django import forms
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from el_pagination.views import AjaxListView
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt


class UserListView(AjaxListView):
    template_name = 'profile/profile-list.html'
    page_template = 'profile/entry_list_page.html'
    # paginate_by = 3

    def get_queryset(self):
        qs = UserProfile.objects.all()
        return qs
    
    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        return context


@method_decorator(login_required, name='dispatch')
class ProfileDetailView(DetailView):
    template_name = 'profile/profile-details.html'

    def get_object(self):
        qs = UserProfile.objects.filter(slug=self.kwargs['slug'])
        if qs.exists():
            return qs.first()
        return None
    
    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        return context

    def user_passes_test(self, request):
        if request.user.is_authenticated:
            # self.object = self.get_object()
            # return self.object.user == request.user
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(ProfileDetailView, self).dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(UpdateView):
    template_name = 'profile/profile-update.html'
    form_class = UserProfileUpdateForm

    def get_object(self):
        qs = UserProfile.objects.filter(slug=self.kwargs['slug'])
        if qs.exists():
            return qs.first()
        return None

    def form_valid(self, form):
        self.object = self.get_object()
        contact = form.instance.contact
        # print(f"XXX___{contact}")
        contactFake = self.request.POST.get("contact_fake")
        # print(self.request.POST.get("first_name"))
        # Save the form
        # if not self.request.POST.get("first_name") == "" and not self.request.POST.get("last_name") == "":
        #     form.instance.name = self.request.POST.get("first_name") + " " + self.request.POST.get("last_name")
        # elif not self.request.POST.get("first_name") == "" and self.request.POST.get("last_name") == "":
        #     form.instance.name = self.request.POST.get("first_name")
        # elif self.request.POST.get("first_name") == "" and not self.request.POST.get("last_name") == "":
        #     form.instance.name = self.request.POST.get("last_name")
        # else:
        #     form.instance.name = self.object.user.username
        if contact is not "":
            form.instance.contact = contactFake + contact
        messages.add_message(self.request, messages.SUCCESS,
                             "Your profile has been updated successfully !")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        return context

    def user_passes_test(self, request):
        if request.user.is_authenticated:
            self.object = self.get_object()
            return self.object.user == request.user
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(ProfileUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        slug = self.kwargs['slug']
        return reverse('profile_update', kwargs={'slug': slug})


@method_decorator(login_required, name='dispatch')
class UserReportCreateView(CreateView):
    template_name = 'report/manage.html'
    form_class = UserReportManageForm

    def form_valid(self, form):
        slug = self.kwargs.get('slug')
        profile_qs = UserProfile.objects.filter(slug=slug)
        if profile_qs.exists():
            # user_qs = User.objects.filter(username__iexact=profile_qs.first().user.username)
            # reported_by_qs = User.objects.filter(username__exact=self.request.user.username)
            report_filter_qs = UserReport.objects.filter(
                user=profile_qs.first().user, reported_by=self.request.user
            )
            if not report_filter_qs.exists():
                if not profile_qs.first().user.is_superuser:
                    form.instance.user = profile_qs.first().user
                    form.instance.reported_by = self.request.user
                    messages.add_message(self.request, messages.SUCCESS,
                                        "We apologize for your bad experience! Your report has been submitted successfully & is under review. Necessary steps will be taken after investigation.")
                    return super().form_valid(form)
                else:
                    messages.add_message(self.request, messages.WARNING,
                                         "You cannot report this user!!!")
            else:
                messages.add_message(self.request, messages.INFO,
                                     "You already reported this user. Necessary steps will be taken if the investigation result goes against this user. If you want to know more, please feel free to contact with us.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('home')

    def get_context_data(self, **kwargs):
        context = super(UserReportCreateView,
                        self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        context['page_title'] = "Report User"
        return context

    def user_passes_test(self, request):
        if request.user.is_authenticated:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        slug = self.kwargs.get('slug')
        profile_qs = UserProfile.objects.filter(slug=slug)
        if profile_qs.exists():
            url = request.META.get('HTTP_REFERER', '/')
            report_filter_qs = UserReport.objects.filter(
                user=profile_qs.first().user, reported_by=self.request.user
            )
            if report_filter_qs.exists():
                messages.add_message(self.request, messages.INFO,
                                        "You already reported this user. Necessary steps will be taken if the investigation result goes against this user. If you want to know more, please feel free to contact with us.")
                return HttpResponseRedirect(url)
            if profile_qs.first().user.is_superuser:
                messages.add_message(self.request, messages.WARNING,
                                        "You cannot report this user!!!")
                return HttpResponseRedirect(url)
        return super(UserReportCreateView, self).dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class UserReportListView(ListView):
    template_name = 'report/list.html'

    def get_queryset(self):
        qs = UserReport.objects.all()
        return qs

    def get_context_data(self, **kwargs):
        context = super(UserReportListView,
                        self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        context['page_title'] = "User Report List"
        return context

    def user_passes_test(self, request):
        if request.user.is_superuser:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(UserReportListView, self).dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class UserReportDetailView(DetailView):
    template_name = 'report/detail.html'

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        qs = UserReport.objects.filter(slug=slug)
        if qs.exists():
            return qs.first()
        return None

    def get_context_data(self, **kwargs):
        context = super(UserReportDetailView, self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        context['page_title'] = "Report Details"
        return context

    def user_passes_test(self, request):
        if request.user.is_superuser:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(UserReportDetailView, self).dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class SingleUserReportListView(ListView):
    template_name = 'report/list.html'

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        profile_qs = UserProfile.objects.filter(slug=slug)
        if profile_qs.exists():
            qs = UserReport.objects.filter(user=profile_qs.first().user)
            return qs
        return None

    def get_context_data(self, **kwargs):
        context = super(SingleUserReportListView,
                        self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        slug = self.kwargs.get('slug')
        profile_qs = UserProfile.objects.filter(slug=slug)
        if profile_qs.exists():
            profile = profile_qs.first()
            context['page_title'] = f"{profile.get_smallname()}'s Reports"
            context['page_type'] = "SingleReports"
        return context

    def user_passes_test(self, request):
        if request.user.is_superuser:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(SingleUserReportListView, self).dispatch(request, *args, **kwargs)


@csrf_exempt
@login_required
def report_delete_all(request):
    url = reverse('home')
    user = request.user
    if user.is_superuser:
        if request.method == "POST":
            slug = request.POST.get("slug")
            profile_qs = UserProfile.objects.filter(slug=slug)
            if profile_qs.exists():
                qs = UserReport.objects.filter(user=profile_qs.first().user)
                if qs.exists():
                    qs.delete()
                    messages.add_message(request, messages.SUCCESS,
                                        "Deleted successfully!")
                    url = reverse('user_report_list')
                else:
                    messages.add_message(request, messages.WARNING,
                                        "Not found!")
    else:
        block_suspicious_user(request)
    return HttpResponseRedirect(url)


@csrf_exempt
@login_required
def report_delete(request):
    url = reverse('home')
    user = request.user
    if user.is_superuser:
        if request.method == "POST":
            slug = request.POST.get("slug")
            # print(slug)
            qs = UserReport.objects.filter(slug=slug)
            if qs.exists():
                qs.delete()
                messages.add_message(request, messages.SUCCESS,
                                        "Deleted successfully!")
                url = request.META.get('HTTP_REFERER', '/')
            else:
                messages.add_message(request, messages.WARNING,
                                        "Not found!")
    else:
        block_suspicious_user(request)
    return HttpResponseRedirect(url)
