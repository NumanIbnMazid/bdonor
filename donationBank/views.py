from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, ListView, DetailView, TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import DonationBankForm, DonationBankSettingForm
from .models import DonationBank, DonationBankSetting, BankMember, MemberRequest
from django.urls import reverse
from django.contrib import messages
from django import forms
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from suspicious.utils import block_suspicious_user
from django.views.decorators.csrf import csrf_exempt
import datetime
from suspicious.models import Suspicious
from utils.handlers import create_notification
from utils.models import Notification
from accounts.utils import time_str_mix_slug
from accounts.models import UserProfile
from django.core.mail import EmailMultiAlternatives


@method_decorator(login_required, name='dispatch')
class DonationBankCreateView(CreateView):
    template_name = 'donationBank/manage.html'
    form_class = DonationBankForm

    def form_valid(self, form):
        institute = form.instance.institute
        qs = DonationBank.objects.filter(
            institute__iexact=institute)
        if qs.exists():
            form.add_error(
                'institute', forms.ValidationError(
                    "This Institute is alreay exists!"
                )
            )
            return super().form_invalid(form)
        else:
            messages.add_message(self.request, messages.SUCCESS,
                                 "Donation Bank has been created successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('donation_bank:bank_dashboard')

    def get_context_data(self, **kwargs):
        context = super(DonationBankCreateView,
                        self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        context['page_title'] = "Create Donation Bank"
        context['object_list'] = DonationBank.objects.all().order_by(
            '-created_at')
        return context

    def user_passes_test(self, request):
        qs = BankMember.objects.filter(user=self.request.user)
        member_request_qs = MemberRequest.objects.filter(
            user=self.request.user)
        if not qs.exists() and not member_request_qs.exists():
            if request.user.profile.account_type == 1 or request.user.is_superuser:
                return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            qs = BankMember.objects.filter(user=self.request.user)
            if not qs.exists():
                messages.add_message(self.request, messages.INFO,
                                     "Please subscribe a plan to Create Donation Bank.")
                return HttpResponseRedirect(reverse('priceplan:plan_list'))
            else:
                messages.add_message(self.request, messages.WARNING,
                                     f"You are already a member of '{qs.first().bank.institute}'!")
                return HttpResponseRedirect(reverse('home'))
        return super(DonationBankCreateView, self).dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class BankDashboardView(TemplateView):
    def get(self, request, *args, **kwargs):
        user = request.user
        qs = DonationBank.objects.filter(bank_member__user=self.request.user)
        if qs.exists():
            bank_object = qs.first()
            creator_qs = BankMember.objects.filter(bank=bank_object, role=0)
            if creator_qs.exists() and creator_qs.first().user.profile.account_type == 1:
                member_requests = MemberRequest.objects.filter(
                    bank__bank_member__user=self.request.user)
                # Starts Base Template Context
                if self.request.user.is_superuser:
                    base_template = 'admin-site/base.html'
                else:
                    base_template = 'base.html'
                # Ends Base Template Context
                context = {
                    'base_template': base_template,
                    'object': bank_object,
                    'member_requests': member_requests,
                }
                return render(self.request, "donationBank/dashboard.html", context=context)
        return HttpResponseRedirect(reverse('home'))


@csrf_exempt
@login_required
def donationBank_delete(request):
    url = reverse('home')
    if request.method == "POST":
        slug = request.POST.get("slug")
        qs = DonationBank.objects.filter(
            slug=slug, bank_member__user=request.user)
        if qs.exists() and request.user.profile.account_type == 1:
            if request.user.user_bank_member.role == 0:
                qs.delete()
                messages.add_message(request, messages.SUCCESS,
                                     "Donation Bank has been deleted successfully!")
            else:
                block_suspicious_user(request)
        else:
            messages.add_message(request, messages.WARNING,
                                 "Not found!")
    return HttpResponseRedirect(url)


@method_decorator(login_required, name='dispatch')
class DonationBankDetailView(DetailView):
    template_name = 'donationBank/details.html'

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        qs = DonationBank.objects.filter(slug=slug)
        if qs.exists():
            return qs.first()
        return None

    def get_context_data(self, **kwargs):
        context = super(DonationBankDetailView,
                        self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        return context

    # def user_passes_test(self, request):
    #     if request.user.is_authenticated:
    #         return True
    #     return False

    # def dispatch(self, request, *args, **kwargs):
    #     if not self.user_passes_test(request):
    #         block_suspicious_user(request)
    #         return HttpResponseRedirect(reverse('home'))
    #     return super(DonationBankDetailView, self).dispatch(request, *args, **kwargs)


class DonationBankUpdateView(UpdateView):
    template_name = 'donationBank/manage.html'
    form_class = DonationBankForm

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        qs = DonationBank.objects.filter(slug=slug)
        if qs.exists():
            return qs.first()
        return None

    def form_valid(self, form):
        self.object = self.get_object()
        institute = form.instance.institute
        if not institute == self.object.institute:
            qs = DonationBank.objects.filter(
                institute__iexact=institute)
            if qs.exists():
                form.add_error(
                    'institute', forms.ValidationError(
                        "This institute is alreay exists!"
                    )
                )
                return super().form_invalid(form)
            # else:
            #     messages.add_message(self.request, messages.SUCCESS,
            #                          "Price Plan has been updated successfully!")
        messages.add_message(self.request, messages.SUCCESS,
                             "Donation Bank has been updated successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        self.object = self.get_object()
        return reverse('donation_bank:bank_details', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super(DonationBankUpdateView,
                        self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        context['page_title'] = "Update Bank Info"
        # Ends Base Template Context
        return context

    def user_passes_test(self, request):
        self.object = self.get_object()
        qs = DonationBank.objects.filter(
            slug=self.object.slug, bank_member__user=request.user
        )
        member_request_qs = MemberRequest.objects.filter(
            user=self.request.user)
        if qs.exists() and self.request.user.profile.account_type == 1:
            if not member_request_qs.exists() and self.request.user.user_bank_member.role == 0:
                return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(DonationBankUpdateView, self).dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class DonationBankListView(ListView):
    template_name = 'donationBank/list.html'

    def get_queryset(self):
        qs = DonationBank.objects.all()
        if qs.exists():
            return qs
        return None

    def get_context_data(self, **kwargs):
        context = super(DonationBankListView, self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        return context


@method_decorator(login_required, name='dispatch')
class DonationBankSettingUpdateView(UpdateView):
    template_name = 'donationBank/manage.html'
    form_class = DonationBankSettingForm

    def get_object(self, *args, **kwargs):
        qs = DonationBankSetting.objects.filter(
            bank__bank_member__user=self.request.user)
        if qs.exists():
            return qs.first()
        return None

    def form_valid(self, form):
        self.object = self.get_object()
        messages.add_message(self.request, messages.SUCCESS,
                             "Donation Bank Settings has been updated successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        self.object = self.get_object()
        return reverse('donation_bank:bank_dashboard')

    def get_context_data(self, **kwargs):
        context = super(DonationBankSettingUpdateView,
                        self).get_context_data(**kwargs)
        self.object = self.get_object()
        qs = DonationBank.objects.filter(slug=self.object.bank.slug)
        if qs.exists():
            context['object'] = qs.first()
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        context['page_title'] = "Update Bank Settings"
        # Ends Base Template Context
        return context

    def user_passes_test(self, request):
        self.object = self.get_object()
        qs = DonationBank.objects.filter(
            slug=self.object.bank.slug
        )
        member_qs = BankMember.objects.filter(user=self.request.user, role=0)
        if qs.exists() and member_qs.exists() and qs.first() == member_qs.first().bank and self.request.user.profile.account_type == 1:
            if self.request.user.user_bank_member.role == 0:
                return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(DonationBankSettingUpdateView, self).dispatch(request, *args, **kwargs)


# @method_decorator(login_required, name='dispatch')
# class InviteMemberTemplateView(TemplateView):
#     def get(self, request, *args, **kwargs):
#         user = request.user
#         qs = DonationBank.objects.filter(bank_member__user=self.request.user)
#         bank_member_qs = BankMember.objects.filter(user=self.request.user, bank=qs.first(), role=0)
#         if qs.exists():
#             if bank_member_qs.exists() and self.request.user.profile.account_type == 1:
#                 bank_object = qs.first()
#                 # STARTS URL Prefix
#                 domain = self.request.META['HTTP_HOST']
#                 if self.request.is_secure():
#                     scheme = "https://"
#                 else:
#                     scheme = "http://"
#                 join_url = reverse('donation_bank:bank_member_request_create',
#                                    kwargs={'slug': bank_object.slug})
#                 redirect_url = f"{scheme}{domain}{join_url}"
#                 # ENDS URL Prefix

#                 # Starts Base Template Context
#                 if self.request.user.is_superuser:
#                     base_template = 'admin-site/base.html'
#                 else:
#                     base_template = 'base.html'
#                 # Ends Base Template Context
#                 context = {
#                     'base_template': base_template,
#                     'object': bank_object,
#                     'link': redirect_url
#                 }
#                 return render(request, "donationBank/invite.html", context=context)
#         return HttpResponseRedirect(reverse('home'))

#     # def user_passes_test(self, request):
#     #     user_bank_qs = BankMember.objects.filter(user=self.request.user, role=0)
#     #     if user_bank_qs.exists() and self.request.user.profile.account_type == 1:
#     #         if self.request.user.user_bank_member.role == 0:
#     #             return True
#     #     return False

#     # def dispatch(self, request, *args, **kwargs):
#     #     if not self.user_passes_test(request):
#     #         block_suspicious_user(request)
#     #         return HttpResponseRedirect(reverse('home'))
#     #     return super(InviteMemberTemplateView, self).dispatch(request, *args, **kwargs)


# @csrf_exempt
# @login_required
# def send_invitation_mail(request):
#     url = reverse('home')
#     user = request.user
#     user_bank_qs = BankMember.objects.filter(user=user, role=0)
#     if user_bank_qs.exists() and request.user.profile.account_type == 1:
#         user_bank = user_bank_qs.first()
#         if request.method == "POST":
#             email = request.POST.get("email")
#             request_url = request.POST.get("request_url")
#             # print(request_url)
#             # Sending Email
#             mail_msg = f"Hello! <br> {user.profile.get_dynamic_name()} has invited you to be a member of '{user_bank.bank.institute}'<br> click <a href='{request_url}' target='_blank'>here</a> to join.<br> Have a good day. <br>Thanks for being with us."
#             mail_subject = f'{user.profile.get_dynamic_name()} has invited you to join in {user_bank.bank.institute}.'
#             mail_from = 'admin@bdonor.com'
#             mail_text = 'Please do not Reply'
#             subject = mail_subject
#             from_email = mail_from
#             to = [email]
#             text_content = mail_text
#             html_content = mail_msg
#             msg = EmailMultiAlternatives(
#                 subject, text_content, from_email, [to])
#             msg.attach_alternative(html_content, "text/html")
#             msg.send()
#             # Save form
#             messages.add_message(request, messages.SUCCESS,
#                                     "Your invitation has been sent successfully!")
#             url = reverse('donation_bank:bank_dashboard')
#     return HttpResponseRedirect(url)


@csrf_exempt
@login_required
def member_request_create(request):
    url = reverse('home')
    user = request.user
    if request.method == "POST":
        slug = request.POST.get("slug")
        bank_qs = DonationBank.objects.filter(slug=slug)
        if bank_qs.exists():
            bank = bank_qs.first()
            url = reverse('donation_bank:bank_details',
                          kwargs={'slug': bank.slug})
            filter_request = MemberRequest.objects.filter(user=user)
            filter_member = BankMember.objects.filter(user=user)
            count_members = BankMember.objects.filter(bank=bank).count()
            if filter_request.exists():
                messages.add_message(request, messages.WARNING,
                                     f"You already have a pending request to join '{filter_request.first().bank.institute}'.")
            elif filter_member.exists():
                messages.add_message(request, messages.WARNING,
                                     f"You are already a member of '{filter_member.first().bank.institute}'.")
            elif count_members >= 3:
                messages.add_message(request, messages.WARNING,
                                     "There are no free slot to join this Donation Bank! Maximum 3 members can join each Donation Bank.")
            else:
                if len(user.username) < 11:
                    slug_binding = user.username.lower()+'-'+time_str_mix_slug()
                else:
                    username = user.username[:10]
                    slug_binding = username.lower()+'-'+time_str_mix_slug()
                instance = MemberRequest.objects.create(
                    user=user, bank=bank, slug=slug_binding
                )
                # url = reverse('donation_bank:bank_list')
                # Create Notification
                receiver_qs = BankMember.objects.filter(bank=bank, role=0)
                if receiver_qs.exists():
                    sender = request.user
                    receiver = receiver_qs.first().user
                    category = 'memberRequest_Create'
                    identifier = slug_binding
                    subject = f"{sender.profile.get_dynamic_name()} wants to be a member of your Donation bank."
                    message = f"{sender.profile.get_dynamic_name()} wants to be a member of your Donation bank. <br> Requested sent at : {instance.created_at}"
                    
                    notification_pre_qs = Notification.objects.filter(
                        category__iexact='memberRequest_Create', sender=sender, receiver=receiver)
                    if notification_pre_qs.exists():
                        # Update Notification
                        notification_pre_qs.update(
                            updated_at=datetime.datetime.now())
                    else:
                        # Create Notification
                        create_notification(
                            request=request, sender=sender, receiver=receiver, category=category, identifier=identifier, subject=subject, message=message
                        )
                # ----------- Notification Ends -----------
                messages.add_message(request, messages.SUCCESS,
                                     "Your request has been created successfully!")
    return HttpResponseRedirect(url)


@csrf_exempt
@login_required
def member_request_delete(request):
    url = reverse('home')
    user = request.user
    if request.method == "POST":
        slug = request.POST.get("slug")
        request_qs = MemberRequest.objects.filter(slug=slug)
        if request_qs.exists():
            member_request = request_qs.first()
            url = reverse('donation_bank:bank_details',
                          kwargs={'slug': member_request.bank.slug})
            instance = request_qs.delete()
            # url = reverse('donation_bank:bank_list')
            # Create Notification
            receiver_qs = BankMember.objects.filter(
                bank=member_request.bank, role=0)
            if receiver_qs.exists():
                sender = request.user
                receiver = receiver_qs.first().user
                category = 'memberRequest_Delete'
                identifier = member_request.bank.slug
                subject = f"{sender.profile.get_dynamic_name()} cancels his request to join your Donation Bank."
                message = f"{sender.profile.get_dynamic_name()} cancels his request to join your Donation Bank."
                notification_pre_qs = Notification.objects.filter(
                    category__iexact='memberRequest_Delete', sender=sender, receiver=receiver)
                if notification_pre_qs.exists():
                    # Update Notification
                    notification_pre_qs.update(
                        updated_at=datetime.datetime.now())
                else:
                    # Create Notification
                    create_notification(
                        request=request, sender=sender, receiver=receiver, category=category, identifier=identifier, subject=subject, message=message
                    )
            # Delete Notification
            notification_qs = Notification.objects.filter(
                category__iexact='memberRequest_Create', sender=sender, receiver=receiver)
            if notification_qs.exists():
                notification_qs.delete()
            # ----------- Notification Ends -----------
            messages.add_message(request, messages.SUCCESS,
                                 "Your request has been created successfully!")
    return HttpResponseRedirect(url)


@csrf_exempt
@login_required
def member_request_accept(request):
    url = reverse('home')
    user = request.user
    if request.method == "POST":
        slug = request.POST.get("slug")
        member_requests_qs = MemberRequest.objects.filter(slug=slug)
        if member_requests_qs.exists():
            member_request = member_requests_qs.first()
            bank_member_qs = BankMember.objects.filter(
                user=user, bank=member_request.bank, role=0)
            if bank_member_qs.exists():
                bank_qs = DonationBank.objects.filter(slug=member_request.bank.slug)
                if bank_qs.exists():
                    bank = bank_qs.first()
                    url = reverse('donation_bank:bank_dashboard')
                    filter_member = BankMember.objects.filter(
                        user=member_request.user)
                    count_members = BankMember.objects.filter(bank=bank).count()
                    if filter_member.exists():
                        messages.add_message(request, messages.WARNING,
                                             f"{member_request.user.profile.get_dynamic_name()} is already a member of '{filter_member.first().bank.institute}'.")
                    elif count_members >= 3:
                        messages.add_message(request, messages.WARNING,
                                     "There are no free slot remaining! Maximum 3 members can join each Donation Bank.")
                    else:
                        instance = BankMember.objects.create(
                            user=member_request.user, bank=member_request.bank, role=1)
                        member_requests_qs.delete()
                        # Create Notification
                        sender = request.user
                        receiver = member_request.user
                        category = 'memberRequest_Accept'
                        identifier = member_request.slug
                        subject = f"{sender.profile.get_dynamic_name()} accepted your member request."
                        message = f"{sender.profile.get_dynamic_name()} accepted your member request. <br> You are now a member of '{member_request.bank.institute}'."
                        notification_pre_qs = Notification.objects.filter(
                            category__iexact='memberRequest_Accept', sender=sender, receiver=receiver)
                        if notification_pre_qs.exists():
                            # Update Notification
                            notification_pre_qs.update(
                                updated_at=datetime.datetime.now())
                        else:
                            # Create Notification
                            create_notification(
                                request=request, sender=sender, receiver=receiver, category=category, identifier=identifier, subject=subject, message=message
                            )
                        # Delete Notification
                        notification_qs = Notification.objects.filter(
                            category__iexact='memberRequest_Create', sender=receiver, receiver=request.user)
                        if notification_qs.exists():
                            notification_qs.delete()
                        # ----------- Notification Ends -----------
                        messages.add_message(request, messages.SUCCESS,
                                             f"Request accepted! {member_request.user.profile.get_dynamic_name()} is now a member of your Donation Bank.")
            else:
                block_suspicious_user(request)
    return HttpResponseRedirect(url)


@csrf_exempt
@login_required
def member_request_reject(request):
    url = reverse('home')
    user = request.user
    if request.method == "POST":
        slug = request.POST.get("slug")
        member_requests_qs = MemberRequest.objects.filter(slug=slug)
        if member_requests_qs.exists():
            member_request = member_requests_qs.first()
            bank_member_qs = BankMember.objects.filter(
                user=user, bank=member_request.bank, role=0)
            if bank_member_qs.exists():
                bank_qs = DonationBank.objects.filter(
                    slug=member_request.bank.slug)
                if bank_qs.exists():
                    bank = bank_qs.first()
                    url = reverse('donation_bank:bank_dashboard')
                    instance = member_requests_qs.delete()
                    # Create Notification
                    sender = request.user
                    receiver = member_request.user
                    category = 'memberRequest_Deny'
                    identifier = member_request.slug
                    subject = f"{sender.profile.get_dynamic_name()} rejected your member request."
                    message = f"{sender.profile.get_dynamic_name()} has rejected your member request to '{member_request.bank.institute}'."
                    notification_pre_qs = Notification.objects.filter(
                        category__iexact='memberRequest_Deny', sender=sender, receiver=receiver)
                    if notification_pre_qs.exists():
                        # Update Notification
                        notification_pre_qs.update(
                            updated_at=datetime.datetime.now())
                    else:
                        # Create Notification
                        create_notification(
                            request=request, sender=sender, receiver=receiver, category=category, identifier=identifier, subject=subject, message=message
                        )
                    # Delete Notification
                    notification_qs = Notification.objects.filter(
                        category__iexact='memberRequest_Create', sender=receiver, receiver=request.user)
                    if notification_qs.exists():
                            notification_qs.delete()
                    # ----------- Notification Ends -----------
                    messages.add_message(request, messages.SUCCESS,
                                            f"Request Rejected Successfully!")
            else:
                block_suspicious_user(request)
    return HttpResponseRedirect(url)


@method_decorator(login_required, name='dispatch')
class BankMembersListView(ListView):
    template_name = 'donationBank/members-list.html'

    def get_queryset(self):
        user = self.request.user
        member_qs = BankMember.objects.filter(user=user)
        if member_qs.exists():
            membership = member_qs.first()
            qs = BankMember.objects.filter(bank=membership.bank)
            if qs.exists():
                return qs
        return None

    def get_context_data(self, **kwargs):
        context = super(BankMembersListView,
                        self).get_context_data(**kwargs)
        qs = DonationBank.objects.filter(bank_member__user=self.request.user)
        if qs.exists():
            bank_object = qs.first()
        else:
            bank_object = None
        context['object'] = bank_object
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        return context

    # def user_passes_test(self, request):
    #     if request.user.is_authenticated:
    #         return True
    #     return False

    # def dispatch(self, request, *args, **kwargs):
    #     if not self.user_passes_test(request):
    #         block_suspicious_user(request)
    #         return HttpResponseRedirect(reverse('home'))
    #     return super(BankMembersListView, self).dispatch(request, *args, **kwargs)


@login_required
def membership_remove(request):
    url = reverse('home')
    user = request.user
    if request.method == "POST":
        slug = request.POST.get("slug")
        profile_qs = UserProfile.objects.filter(slug=slug)
        if profile_qs.exists():
            profile = profile_qs.first()
            bank_member_qs = BankMember.objects.filter(user=profile.user)
            if bank_member_qs.exists():
                membership = bank_member_qs.first()
                instance = bank_member_qs.delete()
                url = reverse('donation_bank:bank_members_list')
                # Create Notification
                sender = request.user
                receiver = membership.user
                category = 'membershipRemove'
                identifier = membership.user.profile.slug
                subject = f"{sender.profile.get_dynamic_name()} removed your membership."
                message = f"{sender.profile.get_dynamic_name()} has removed your membership from '{membership.bank.institute}'."
                notification_pre_qs = Notification.objects.filter(
                    category__iexact='membershipRemove', sender=sender, receiver=receiver)
                if notification_pre_qs.exists():
                    # Update Notification
                    notification_pre_qs.update(
                        updated_at=datetime.datetime.now())
                else:
                    # Create Notification
                    create_notification(
                        request=request, sender=sender, receiver=receiver, category=category, identifier=identifier, subject=subject, message=message
                    )
                # ----------- Notification Ends -----------
                messages.add_message(request, messages.SUCCESS,
                                        f"Membership removed Successfully!")
    return HttpResponseRedirect(url)
