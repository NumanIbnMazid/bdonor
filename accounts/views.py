from django.shortcuts import render
from django.views.generic import UpdateView, DetailView, ListView, CreateView
from .models import UserProfile, UserReport, UserPermission
from suspicious.utils import block_suspicious_user
from .forms import UserProfileUpdateForm, UserReportManageForm, UserPermissionManageForm
from django import forms
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from el_pagination.views import AjaxListView
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .utils import time_str_mix_slug
from utils.handlers import create_notification
from django.core.mail import EmailMultiAlternatives
# Custom Decorators Starts
from accounts.decorators import (
    can_browse_required, can_donate_required, can_ask_for_a_donor_required,
    can_manage_bank_required, can_chat_required
)
# Custom Decorators Ends

decorators = [login_required, can_browse_required]


@method_decorator(decorators, name='dispatch')
@method_decorator(can_donate_required, name='dispatch')
@method_decorator(can_ask_for_a_donor_required, name='dispatch')
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


@method_decorator(decorators, name='dispatch')
# @method_decorator(can_donate_required, name='dispatch')
# @method_decorator(can_ask_for_a_donor_required, name='dispatch')
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
        self.object = self.get_object()
        if not self.object.user == self.request.user:
            if self.request.user.user_permissions_user.can_donate == False or self.request.user.user_permissions_user.can_ask_for_a_donor == False:
                messages.add_message(self.request, messages.INFO,
                                     "You are not allowed to view others profile as your donation permission is blocked!")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return super(ProfileDetailView, self).dispatch(request, *args, **kwargs)


@method_decorator(decorators, name='dispatch')
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



@method_decorator(decorators, name='dispatch')
@method_decorator(can_donate_required, name='dispatch')
@method_decorator(can_ask_for_a_donor_required, name='dispatch')
@method_decorator(can_manage_bank_required, name='dispatch')
@method_decorator(can_chat_required, name='dispatch')
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


@method_decorator(decorators, name='dispatch')
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


@method_decorator(decorators, name='dispatch')
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


@method_decorator(decorators, name='dispatch')
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
@can_browse_required
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
@can_browse_required
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


@method_decorator(decorators, name='dispatch')
class UserPermissionListView(ListView):
    template_name = 'user-permission/list.html'

    def get_queryset(self):
        qs = UserPermission.objects.all()
        if qs.exists():
            return qs
        return None

    def get_context_data(self, **kwargs):
        context = super(UserPermissionListView,
                        self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        context['page_title'] = "User Permissions List"
        return context

    def user_passes_test(self, request):
        if self.request.user.is_superuser:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(UserPermissionListView, self).dispatch(request, *args, **kwargs)


@method_decorator(decorators, name='dispatch')
class UserPermissionUpdateView(UpdateView):
    template_name = 'snippets/common/manage.html'
    form_class = UserPermissionManageForm

    def get_object(self):
        slug = self.kwargs['slug']
        profile_qs = UserProfile.objects.filter(slug=slug)
        if profile_qs.exists():
            qs = UserPermission.objects.filter(user=profile_qs.first().user)
            if qs.exists():
                return qs.first()
        return None

    def get_success_url(self):
        return reverse('user_permission_list')

    def form_valid(self, form):
        self.object = self.get_object()
        details_fake = form.cleaned_data['details_fake']
        message_array = []
        fields_dict = {
            'can_browse': 'Browse Permission', 'can_donate': 'Donate Permission',
            'can_ask_for_a_donor': 'Donor Request Permission',
            'can_manage_bank': 'Bank Manage Permission', 'can_chat': 'Chat Permission'
        }
        for key, value in fields_dict.items():
            if key in form.changed_data:
                if form.cleaned_data[key] == False:
                    status = "<span style='color:red;'>Blocked</span>"
                else:
                    status = "<span style='color:green;'>Allowed</span>"
                msg = f"{value}: {status}"
                message_array.append(msg)
        if not details_fake == None and not details_fake == "":
            message_bind = f"<br>Permission Changed: <span style='color:blue;font-size:15px;margin-left:5px;'>{message_array}</span>. <br><br> <span style='color:black;font-style:italic;font-size:17px;font-weight:700;'>Message:</span><br> {details_fake}<br><br><p>If you have any query, please feel free to contact with us.</p>"
        else:
            message_bind = f"<br>Permission Changed: <span style='color:blue;font-size:15px;margin-left:5px;'>{message_array}<br><br><p>If you have any query, please feel free to contact with us.</p></span>"
        receiver = self.object.user
        sender = self.request.user
        receiver_email = receiver.email
        # Sending Email
        mail_msg = f"Hello {receiver.profile.get_username()} ! <br> Your Permissions in BDonor has been changed!. <br> <br> <span style='color:black;font-style:italic;font-size:17px;font-weight:700;'>Additional Information:</span> {message_bind} <br><br><br> Have a good day. <br>Thanks for being with us."
        mail_subject = 'Your Permissions in BDonor has been changed!'
        mail_from = 'bdonorweb@gmail.com'
        mail_text = 'Please do not Reply'
        subject = mail_subject
        from_email = mail_from
        to = [receiver_email]
        text_content = mail_text
        html_content = mail_msg
        msg = EmailMultiAlternatives(
            subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        # Create Notification
        request = self.request
        sender = self.request.user
        receiver = receiver
        category = 'userPermission_Update'
        identifier = time_str_mix_slug()
        subject = 'Your Permissions in BDonor has been changed!'
        message = f"Your Permissions in BDonor has been changed! <br> <br> <span style='color:black;font-style:italic;font-size:17px;font-weight:700;'>Additional Information:</span> {message_bind}"
        create_notification(
            request=request, sender=sender, receiver=receiver, category=category, identifier=identifier, subject=subject, message=message
        )
        messages.add_message(self.request, messages.SUCCESS,
                             f"{self.object.user.profile.get_smallname()}'s Permissions has been updated successfully !")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UserPermissionUpdateView,
                        self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        self.object = self.get_object()
        context['page_title'] = f"Update {self.object.user.profile.get_smallname()}'s Permissions"
        return context

    def user_passes_test(self, request):
        if self.request.user.is_superuser:
            self.object = self.get_object()
            if not self.object.user.is_superuser:
                return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            messages.add_message(self.request, messages.ERROR,
                "Superuser's permission can't be changed from here! Please use the Django Admin Panel."
            )
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return super(UserPermissionUpdateView, self).dispatch(request, *args, **kwargs)
