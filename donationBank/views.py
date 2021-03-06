from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, ListView, DetailView, TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import (DonationBankForm, DonationBankSettingForm, DonationManageForm,
                    DonationRequestManageForm, CampaignManageForm, DonationProgressForm,
                    DonationRequestProgressForm
                    )
from .models import (DonationBank, DonationBankSetting, BankMember,
                     MemberRequest, Donation, DonationRequest, DonationProgress, Campaign,
                     DonationRequestProgress
                     )
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
from django.db.models import Count, F, Sum
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
# Custom Decorators Starts
from accounts.decorators import (
    can_browse_required, can_donate_required, can_ask_for_a_donor_required,
    can_manage_bank_required, can_chat_required
)
# Custom Decorators Ends

decorators = [login_required, can_browse_required]


@method_decorator(decorators, name='dispatch')
@method_decorator(can_manage_bank_required, name='dispatch')
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
                    "This Institute is already exists!"
                )
            )
            return super().form_invalid(form)
        else:
            messages.add_message(self.request, messages.SUCCESS,
                                 "Donation Bank has been created successfully!")
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        response = super(DonationBankCreateView, self).post(
            request, *args, **kwargs)
        institute = self.object.institute
        super_user_qs = User.objects.filter(is_superuser=True)
        sender_qs = User.objects.filter(username=self.request.user.username)
        # print(super_user_qs)
        # print(sender_qs)
        if super_user_qs.exists() and sender_qs.exists():
            sender = sender_qs.first()
            # URL Prefix
            domain = self.request.META['HTTP_HOST']
            if self.request.is_secure():
                scheme = "https://"
            else:
                scheme = "http://"
            donation_url = reverse('donation_bank:bank_details',
                                    kwargs={'slug': self.object.slug})
            redirect_url = f"{scheme}{domain}{donation_url}"
            # End URL Prefix
            for receiver in super_user_qs:
                # print(receiver)
                # Create Notification to Superusers
                category = 'donationBank_Create'
                identifier = sender.username[:5] + "-" + receiver.username[:5] + "_BankCreate"
                subject = f"{sender.profile.get_username()} has created a bank."
                message = f"Hello {receiver.profile.get_username()} ! <br> {sender.profile.get_username()} has created a bank named {institute} and is waiting for verification approval. <br> click <a href='{redirect_url}' target='_blank'>here</a> to view bank details."
                create_notification(
                    request=self.request, sender=sender, receiver=receiver, category=category, identifier=identifier, subject=subject, message=message
                )
                # Sending Email
                mail_msg = f"Hello {receiver.profile.get_username()} ! <br> {sender.profile.get_username()} has created a bank named {institute} and is waiting for verification approval. <br> click <a href='{redirect_url}' target='_blank'>here</a> to view bank details. <br> Have a good day. <br>Thanks for being with us."
                mail_subject = f'{sender.profile.get_username()} has created a bank.'
                mail_from = 'admin@bdonor.com'
                mail_text = 'Please do not Reply'
                subject = mail_subject
                from_email = mail_from
                to = [receiver.email]
                text_content = mail_text
                html_content = mail_msg
                msg = EmailMultiAlternatives(
                    subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
        return response
    
    def get_form_kwargs(self):
        kwargs = super(DonationBankCreateView, self).get_form_kwargs()
        if self.form_class:
            kwargs.update({'request': self.request})
        return kwargs

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
        if not qs.exists() and not member_request_qs.exists() and not request.user.is_superuser:
            if request.user.profile.account_type == 1:
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


@method_decorator(decorators, name='dispatch')
@method_decorator(can_manage_bank_required, name='dispatch')
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
@can_browse_required
@can_manage_bank_required
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


@method_decorator(decorators, name='dispatch')
# @method_decorator(can_manage_bank_required, name='dispatch')
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
        # Bank Storage Calculation
        self.object = self.get_object()
        blood_qs = Donation.objects.values('blood_group').annotate(
            total_count=Sum(F('quantity'))).order_by().filter(donation_type=0, bank=self.object).is_not_expired().is_pending()
        organ_qs = Donation.objects.values('organ_name').annotate(
            total_count=Sum(F('quantity'))).order_by().filter(donation_type=1, bank=self.object).is_not_expired().is_pending()
        tissue_qs = Donation.objects.values('tissue_name').annotate(
            total_count=Count('id')).order_by().filter(donation_type=2, bank=self.object).is_not_expired().is_pending()
        context['blood_list'] = blood_qs
        context['blood_count'] = Donation.objects.filter(
            donation_type=0, bank=self.object).is_not_expired().is_pending().aggregate(total=Sum(F('quantity'))).get('total', 0)
        context['organ_list'] = organ_qs
        context['organ_count'] = Donation.objects.filter(
            donation_type=1, bank=self.object).is_not_expired().is_pending().aggregate(total=Sum(F('quantity'))).get('total', 0)
        context['tissue_list'] = tissue_qs
        context['tissue_count'] = Donation.objects.filter(
            donation_type=2, bank=self.object).is_not_expired().is_pending().count()
        return context

    def user_passes_test(self, request):
        if request.user.is_authenticated:
            # self.object = self.get_object()
            # if self.object.bank_setting.privacy == 0:
            #     return True
            self.object = self.get_object()
            qs = DonationBank.objects.filter(
                slug=self.object.slug, bank_member__user=request.user
            )
            if qs.exists() and self.request.user.profile.account_type == 1:
                return True
            elif self.object.bank_setting.privacy == 0:
                return True
            elif request.user.is_superuser:
                return True
            else:
                return False
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(DonationBankDetailView, self).dispatch(request, *args, **kwargs)


@method_decorator(decorators, name='dispatch')
@method_decorator(can_manage_bank_required, name='dispatch')
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
                        "This institute is already exists!"
                    )
                )
                return super().form_invalid(form)
            # else:
            #     messages.add_message(self.request, messages.SUCCESS,
            #                          "Price Plan has been updated successfully!")
        messages.add_message(self.request, messages.SUCCESS,
                             "Donation Bank has been updated successfully!")
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(DonationBankUpdateView, self).get_form_kwargs()
        if self.form_class:
            kwargs.update({'request': self.request})
        return kwargs

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
        elif request.user.is_superuser:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(DonationBankUpdateView, self).dispatch(request, *args, **kwargs)



@method_decorator(decorators, name='dispatch')
class DonationBankListView(ListView):
    template_name = 'donationBank/list.html'

    def get_queryset(self):
        if self.request.user.is_superuser == True:
            qs = DonationBank.objects.all().dynamic_order()
        else:
            qs = DonationBank.objects.all().is_public().is_verified().dynamic_order()
        # if qs.exists():
        #     return qs
        return qs

    def get_context_data(self, **kwargs):
        context = super(DonationBankListView, self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        return context


@method_decorator(decorators, name='dispatch')
@method_decorator(can_manage_bank_required, name='dispatch')
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
@can_browse_required
@can_manage_bank_required
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
                    message = f"{sender.profile.get_dynamic_name()} wants to be a member of your Donation bank. <br> Requested at : {instance.created_at}"

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
@can_browse_required
@can_manage_bank_required
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
                subject = f"{sender.profile.get_dynamic_name()} cancels his/her request to join your Donation Bank."
                message = f"{sender.profile.get_dynamic_name()} cancels his/her request to join your Donation Bank."
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
@can_browse_required
@can_manage_bank_required
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
                bank_qs = DonationBank.objects.filter(
                    slug=member_request.bank.slug)
                if bank_qs.exists():
                    bank = bank_qs.first()
                    url = reverse('donation_bank:bank_dashboard')
                    filter_member = BankMember.objects.filter(
                        user=member_request.user)
                    count_members = BankMember.objects.filter(
                        bank=bank).count()
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
@can_browse_required
@can_manage_bank_required
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


@method_decorator(decorators, name='dispatch')
@method_decorator(can_manage_bank_required, name='dispatch')
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

    def user_passes_test(self, request):
        qs = DonationBank.objects.filter(bank_member__user=request.user)
        if qs.exists() and self.request.user.profile.account_type == 1:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(BankMembersListView, self).dispatch(request, *args, **kwargs)


@csrf_exempt
@login_required
@can_browse_required
@can_manage_bank_required
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


@method_decorator(decorators, name='dispatch')
@method_decorator(can_manage_bank_required, name='dispatch')
class DonationCreateView(CreateView):
    template_name = 'donationBank/donation-manage.html'
    form_class = DonationManageForm

    def form_valid(self, form):
        user = self.request.user
        qs = DonationBank.objects.filter(bank_member__user=user)
        if qs.exists():
            donation_type = form.instance.donation_type
            bank_object = qs.first()
            if donation_type == 1 and form.instance.organ_name == None:
                form.add_error(
                    'organ_name', forms.ValidationError(
                        "You must select organ name."
                    )
                )
            elif donation_type == 2 and form.instance.tissue_name == None:
                form.add_error(
                    'tissue_name', forms.ValidationError(
                        "You must select tissue name."
                    )
                )
            elif donation_type == 1 and form.instance.quantity == None:
                form.add_error(
                    'quantity', forms.ValidationError(
                        "You must enter the quantity."
                    )
                )
            elif donation_type == 0 and form.instance.quantity == None:
                form.add_error(
                    'quantity', forms.ValidationError(
                        "You must enter blood bag quantity."
                    )
                )
            else:
                if form.instance.organ_name == "Heart" or form.instance.organ_name == "Liver" or form.instance.organ_name == "Pancreas" or form.instance.organ_name == "Intestines":
                    form.instance.quantity = 1
                if form.instance.donation_type == 0:
                    form.instance.quantity = 1
                form.instance.bank = bank_object
                messages.add_message(self.request, messages.SUCCESS,
                                     "Donation item has been created successfully!")
                return super().form_valid(form)
        return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(DonationCreateView, self).get_form_kwargs()
        if self.form_class:
            kwargs.update({'request': self.request})
            kwargs.update({'object': None})
        return kwargs

    def get_success_url(self):
        return reverse('donation_bank:bank_add_donation')

    def get_context_data(self, **kwargs):
        context = super(DonationCreateView,
                        self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        context['page_title'] = "Add Donation"
        qs = DonationBank.objects.filter(bank_member__user=self.request.user)
        bank_object = None
        if qs.exists():
            bank_object = qs.first()
        context['object'] = bank_object
        return context

    def user_passes_test(self, request):
        qs = DonationBank.objects.filter(bank_member__user=request.user, is_verified=True)
        if qs.exists() and self.request.user.profile.account_type == 1:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(DonationCreateView, self).dispatch(request, *args, **kwargs)


@method_decorator(decorators, name='dispatch')
@method_decorator(can_manage_bank_required, name='dispatch')
class DonationListView(ListView):
    template_name = 'donationBank/donation-list.html'
    context_object_name = 'donation_list'

    def get_queryset(self):
        user = self.request.user
        bank_qs = DonationBank.objects.filter(bank_member__user=user)
        if bank_qs.exists():
            bank = bank_qs.first()
            qs = Donation.objects.filter_by_bank_slug(bank.slug)
            return qs
        return None

    def get_context_data(self, **kwargs):
        context = super(DonationListView,
                        self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        qs = DonationBank.objects.filter(bank_member__user=self.request.user)
        bank_object = None
        if qs.exists():
            bank_object = qs.first()
        context['object'] = bank_object
        return context

    def user_passes_test(self, request):
        qs = DonationBank.objects.filter(bank_member__user=request.user, is_verified=True)
        if qs.exists() and self.request.user.profile.account_type == 1:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(DonationListView, self).dispatch(request, *args, **kwargs)


@method_decorator(decorators, name='dispatch')
@method_decorator(can_manage_bank_required, name='dispatch')
class DonationRequestListView(ListView):
    template_name = 'donationBank/donation-request-list.html'
    context_object_name = 'donation_list'

    def get_queryset(self):
        user = self.request.user
        bank_qs = DonationBank.objects.filter(bank_member__user=user)
        if bank_qs.exists():
            bank = bank_qs.first()
            qs = DonationRequest.objects.filter_by_bank_slug(bank.slug)
            return qs
        return None

    def get_context_data(self, **kwargs):
        context = super(DonationRequestListView,
                        self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        qs = DonationBank.objects.filter(bank_member__user=self.request.user)
        bank_object = None
        if qs.exists():
            bank_object = qs.first()
        context['object'] = bank_object
        return context

    def user_passes_test(self, request):
        qs = DonationBank.objects.filter(
            bank_member__user=request.user, is_verified=True)
        if qs.exists() and self.request.user.profile.account_type == 1:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(DonationRequestListView, self).dispatch(request, *args, **kwargs)


@method_decorator(decorators, name='dispatch')
# @method_decorator(can_manage_bank_required, name='dispatch')
class DonationRequestPublicListView(ListView):
    template_name = 'donationBank/donation-request-public.html'
    context_object_name = 'donation_list'

    def get_queryset(self):
        qs = DonationRequest.objects.all().dynamic_order()
        return qs

    def get_context_data(self, **kwargs):
        context = super(DonationRequestPublicListView,
                        self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        qs = DonationBank.objects.filter(bank_member__user=self.request.user)
        bank_object = None
        if qs.exists():
            bank_object = qs.first()
        context['object'] = bank_object
        return context

    def user_passes_test(self, request):
        if self.request.user.is_authenticated:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(DonationRequestPublicListView, self).dispatch(request, *args, **kwargs)


@method_decorator(decorators, name='dispatch')
@method_decorator(can_manage_bank_required, name='dispatch')
class DonationDetailView(DetailView):
    template_name = 'donationBank/donation-details.html'
    context_object_name = 'donation'

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        return Donation.objects.get_by_slug(slug)

    def get_context_data(self, **kwargs):
        context = super(DonationDetailView, self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        qs = DonationBank.objects.filter(bank_member__user=self.request.user)
        bank_object = None
        if qs.exists():
            bank_object = qs.first()
        context['object'] = bank_object
        return context

    def user_passes_test(self, request):
        self.object = self.get_object()
        qs = DonationBank.objects.filter(
            slug=self.object.bank.slug, bank_member__user=request.user, is_verified=True
        )
        if qs.exists() and self.request.user.profile.account_type == 1:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(DonationDetailView, self).dispatch(request, *args, **kwargs)



@method_decorator(decorators, name='dispatch')
@method_decorator(can_manage_bank_required, name='dispatch')
class DonationRequestDetailView(DetailView):
    template_name = 'donationBank/donation-request-details.html'
    context_object_name = 'donation'

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        return DonationRequest.objects.get_by_slug(slug)

    def get_context_data(self, **kwargs):
        context = super(DonationRequestDetailView, self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        qs = DonationBank.objects.filter(bank_member__user=self.request.user)
        bank_object = None
        if qs.exists():
            bank_object = qs.first()
        context['object'] = bank_object
        return context

    def user_passes_test(self, request):
        self.object = self.get_object()
        qs = DonationBank.objects.filter(
            slug=self.object.bank.slug, bank_member__user=request.user, is_verified=True
        )
        if qs.exists() and self.request.user.profile.account_type == 1:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(DonationRequestDetailView, self).dispatch(request, *args, **kwargs)



@method_decorator(decorators, name='dispatch')
# @method_decorator(can_manage_bank_required, name='dispatch')
class DonationRequestPublicDetailView(DetailView):
    template_name = 'donationBank/donation-request-details.html'
    context_object_name = 'donation'

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        return DonationRequest.objects.get_by_slug(slug)

    def get_context_data(self, **kwargs):
        context = super(DonationRequestPublicDetailView,
                        self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        qs = DonationBank.objects.filter(bank_member__user=self.request.user)
        bank_object = None
        if qs.exists():
            bank_object = qs.first()
        context['object'] = bank_object
        return context

    def user_passes_test(self, request):
        if self.request.user.is_authenticated:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(DonationRequestPublicDetailView, self).dispatch(request, *args, **kwargs)



@method_decorator(decorators, name='dispatch')
@method_decorator(can_manage_bank_required, name='dispatch')
class DonationUpdateView(UpdateView):
    template_name = 'donationBank/donation-manage.html'
    form_class = DonationManageForm

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        return Donation.objects.get_by_slug(slug)

    def form_valid(self, form):
        self.object = self.get_object()
        user = self.request.user
        qs = DonationBank.objects.filter(bank_member__user=user)
        if qs.exists():
            donation_type = form.instance.donation_type
            bank_object = qs.first()
            if donation_type == 1 and form.instance.organ_name == None:
                form.add_error(
                    'organ_name', forms.ValidationError(
                        "You must select organ name."
                    )
                )
            elif donation_type == 2 and form.instance.tissue_name == None:
                form.add_error(
                    'tissue_name', forms.ValidationError(
                        "You must select tissue name."
                    )
                )
            elif donation_type == 1 and form.instance.quantity == None:
                form.add_error(
                    'quantity', forms.ValidationError(
                        "You must enter the quantity."
                    )
                )
            elif donation_type == 0 and form.instance.quantity == None:
                form.add_error(
                    'quantity', forms.ValidationError(
                        "You must enter blood bag quantity."
                    )
                )
            else:
                if form.instance.organ_name == "Heart" or form.instance.organ_name == "Liver" or form.instance.organ_name == "Pancreas" or form.instance.organ_name == "Intestines":
                    form.instance.quantity = 1
                if form.instance.donation_type == 0:
                    form.instance.quantity = 1
                form.instance.bank = bank_object
                messages.add_message(self.request, messages.SUCCESS,
                                     "Donation item has been updated successfully!")
                return super().form_valid(form)
        return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(DonationUpdateView, self).get_form_kwargs()
        if self.form_class:
            kwargs.update({'request': self.request})
            kwargs.update({'object': self.get_object()})
        return kwargs

    def get_success_url(self):
        return reverse('donation_bank:bank_donation_list')

    def get_context_data(self, **kwargs):
        context = super(DonationUpdateView,
                        self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        context['page_title'] = "Update Donation"
        qs = DonationBank.objects.filter(bank_member__user=self.request.user)
        bank_object = None
        if qs.exists():
            bank_object = qs.first()
        context['object'] = bank_object
        return context

    def user_passes_test(self, request):
        self.object = self.get_object()
        qs = DonationBank.objects.filter(
            slug=self.object.bank.slug, bank_member__user=request.user, is_verified=True
        )
        if qs.exists() and self.request.user.profile.account_type == 1:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(DonationUpdateView, self).dispatch(request, *args, **kwargs)


@method_decorator(decorators, name='dispatch')
@method_decorator(can_manage_bank_required, name='dispatch')
class DonationRequestUpdateView(UpdateView):
    template_name = 'donationBank/donation-request-manage.html'
    form_class = DonationRequestManageForm

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        return DonationRequest.objects.get_by_slug(slug)

    def form_valid(self, form):
        self.object = self.get_object()
        user = self.request.user
        qs = DonationBank.objects.filter(bank_member__user=user)
        if qs.exists():
            donation_type = form.instance.donation_type
            bank_object = qs.first()
            if donation_type == 1 and form.instance.organ_name == None:
                form.add_error(
                    'organ_name', forms.ValidationError(
                        "You must select organ name."
                    )
                )
            elif donation_type == 2 and form.instance.tissue_name == None:
                form.add_error(
                    'tissue_name', forms.ValidationError(
                        "You must select tissue name."
                    )
                )
            elif donation_type == 1 and form.instance.quantity == None:
                form.add_error(
                    'quantity', forms.ValidationError(
                        "You must enter the quantity."
                    )
                )
            elif donation_type == 0 and form.instance.quantity == None:
                form.add_error(
                    'quantity', forms.ValidationError(
                        "You must enter blood bag quantity."
                    )
                )
            else:
                if form.instance.organ_name == "Heart" or form.instance.organ_name == "Liver" or form.instance.organ_name == "Pancreas" or form.instance.organ_name == "Intestines":
                    form.instance.quantity = 1
                if form.instance.donation_type == 0:
                    form.instance.quantity = 1
                form.instance.bank = bank_object
                messages.add_message(self.request, messages.SUCCESS,
                                     "Donation Request has been updated successfully!")
                return super().form_valid(form)
        return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(DonationRequestUpdateView, self).get_form_kwargs()
        if self.form_class:
            kwargs.update({'request': self.request})
            kwargs.update({'object': self.get_object()})
        return kwargs

    def get_success_url(self):
        return reverse('donation_bank:bank_donation_request_list')

    def get_context_data(self, **kwargs):
        context = super(DonationRequestUpdateView,
                        self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        context['page_title'] = "Update Donation Request"
        qs = DonationBank.objects.filter(bank_member__user=self.request.user)
        bank_object = None
        if qs.exists():
            bank_object = qs.first()
        context['object'] = bank_object
        return context

    def user_passes_test(self, request):
        self.object = self.get_object()
        qs = DonationBank.objects.filter(
            slug=self.object.bank.slug, bank_member__user=request.user, is_verified=True
        )
        if qs.exists() and self.request.user.profile.account_type == 1:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(DonationRequestUpdateView, self).dispatch(request, *args, **kwargs)


@csrf_exempt
@login_required
@can_browse_required
@can_manage_bank_required
def donation_delete(request):
    url = reverse('home')
    user = request.user
    if request.method == "POST":
        slug = request.POST.get("slug")
        qs = Donation.objects.filter(slug=slug)
        if qs.exists():
            qs.delete()
            messages.add_message(request, messages.SUCCESS,
                                 "Deleted successfully!")
            url = reverse('donation_bank:bank_donation_list')
        else:
            messages.add_message(request, messages.WARNING,
                                 "Not found!")
    return HttpResponseRedirect(url)


@csrf_exempt
@login_required
@can_browse_required
@can_manage_bank_required
def donation_request_delete(request):
    url = reverse('home')
    user = request.user
    if request.method == "POST":
        slug = request.POST.get("slug")
        qs = DonationRequest.objects.filter(slug=slug)
        if qs.exists():
            qs.delete()
            messages.add_message(request, messages.SUCCESS,
                                 "Deleted successfully!")
            url = reverse('donation_bank:bank_donation_request_list')
        else:
            messages.add_message(request, messages.WARNING,
                                 "Not found!")
    return HttpResponseRedirect(url)


@method_decorator(decorators, name='dispatch')
@method_decorator(can_manage_bank_required, name='dispatch')
class DonationRequestCreateView(CreateView):
    template_name = 'donationBank/donation-request-manage.html'
    form_class = DonationRequestManageForm

    def form_valid(self, form):
        user = self.request.user
        qs = DonationBank.objects.filter(bank_member__user=user)
        if qs.exists():
            donation_type = form.instance.donation_type
            bank_object = qs.first()
            if donation_type == 1 and form.instance.organ_name == None:
                form.add_error(
                    'organ_name', forms.ValidationError(
                        "You must select organ name."
                    )
                )
            elif donation_type == 2 and form.instance.tissue_name == None:
                form.add_error(
                    'tissue_name', forms.ValidationError(
                        "You must select tissue name."
                    )
                )
            elif donation_type == 1 and form.instance.quantity == None:
                form.add_error(
                    'quantity', forms.ValidationError(
                        "You must enter the quantity."
                    )
                )
            elif donation_type == 0 and form.instance.quantity == None:
                form.add_error(
                    'quantity', forms.ValidationError(
                        "You must enter blood bag quantity."
                    )
                )
            else:
                if form.instance.organ_name == "Heart" or form.instance.organ_name == "Liver" or form.instance.organ_name == "Pancreas" or form.instance.organ_name == "Intestines":
                    form.instance.quantity = 1
                if form.instance.donation_type == 0:
                    form.instance.quantity = 1
                form.instance.bank = bank_object
                messages.add_message(self.request, messages.SUCCESS,
                                     "Donation request has been created successfully!")
                return super().form_valid(form)
        return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(DonationRequestCreateView, self).get_form_kwargs()
        if self.form_class:
            kwargs.update({'request': self.request})
            kwargs.update({'object': None})
        return kwargs

    def get_success_url(self):
        return reverse('donation_bank:bank_add_donation_request')

    def get_context_data(self, **kwargs):
        context = super(DonationRequestCreateView,
                        self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        context['page_title'] = "Add Donation Request"
        qs = DonationBank.objects.filter(bank_member__user=self.request.user)
        bank_object = None
        if qs.exists():
            bank_object = qs.first()
        context['object'] = bank_object
        return context

    def user_passes_test(self, request):
        qs = DonationBank.objects.filter(
            bank_member__user=request.user, is_verified=True)
        if qs.exists() and self.request.user.profile.account_type == 1:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(DonationRequestCreateView, self).dispatch(request, *args, **kwargs)


@method_decorator(decorators, name='dispatch')
@method_decorator(can_manage_bank_required, name='dispatch')
class ManageProgressStatus(UpdateView):
    template_name = 'donationBank/manage-progress-status.html'
    form_class = DonationProgressForm

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        qs = DonationProgress.objects.filter(donation__slug=slug)
        if qs.exists():
            return qs.first()
        return None

    def form_valid(self, form):
        # category = 0
        self.object = self.get_object()
        # print(form.instance.completion_date)
        messages.add_message(self.request, messages.SUCCESS,
                             "Donation Progress Status has been updated successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('donation_bank:bank_donation_list')

    def get_form_kwargs(self):
        kwargs = super(ManageProgressStatus, self).get_form_kwargs()
        if self.form_class:
            kwargs.update({'request': self.request})
            kwargs.update({'object': self.get_object()})
        return kwargs

    def user_passes_test(self, request):
        self.object = self.get_object()
        qs = DonationBank.objects.filter(
            slug=self.object.donation.bank.slug, bank_member__user=request.user, is_verified=True
        )
        if qs.exists() and self.request.user.profile.account_type == 1:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(ManageProgressStatus, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ManageProgressStatus,
                        self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        qs = DonationBank.objects.filter(bank_member__user=self.request.user)
        bank_object = None
        if qs.exists():
            bank_object = qs.first()
        context['object'] = bank_object
        return context




@method_decorator(decorators, name='dispatch')
@method_decorator(can_manage_bank_required, name='dispatch')
class ManageRequestProgressStatus(UpdateView):
    template_name = 'donationBank/manage-progress-status.html'
    form_class = DonationRequestProgressForm

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        qs = DonationRequestProgress.objects.filter(donation__slug=slug)
        if qs.exists():
            return qs.first()
        return None

    def form_valid(self, form):
        # category = 0
        self.object = self.get_object()
        # print(form.instance.completion_date)
        messages.add_message(self.request, messages.SUCCESS,
                             "Donation Request Progress Status has been updated successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('donation_bank:bank_donation_request_list')

    def get_form_kwargs(self):
        kwargs = super(ManageRequestProgressStatus, self).get_form_kwargs()
        if self.form_class:
            kwargs.update({'request': self.request})
            kwargs.update({'object': self.get_object()})
        return kwargs

    def user_passes_test(self, request):
        self.object = self.get_object()
        qs = DonationBank.objects.filter(
            slug=self.object.donation.bank.slug, bank_member__user=request.user, is_verified=True
        )
        if qs.exists() and self.request.user.profile.account_type == 1:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(ManageRequestProgressStatus, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ManageRequestProgressStatus,
                        self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        qs = DonationBank.objects.filter(bank_member__user=self.request.user)
        bank_object = None
        if qs.exists():
            bank_object = qs.first()
        context['object'] = bank_object
        return context




@method_decorator(decorators, name='dispatch')
@method_decorator(can_manage_bank_required, name='dispatch')
class CampaignCreateView(CreateView):
    template_name = 'donationBank/campaign-manage.html'
    form_class = CampaignManageForm

    def form_valid(self, form):
        user = self.request.user
        bank_qs = DonationBank.objects.filter(bank_member__user=user)
        if bank_qs.exists():
            campaign_qs = Campaign.objects.filter(
                bank=bank_qs.first(), title__iexact=form.instance.title)
            if campaign_qs.exists():
                form.add_error(
                    'title', forms.ValidationError(
                        "Campaign name already exists. Please choose another name."
                    )
                )
            else:
                form.instance.bank = bank_qs.first()
                messages.add_message(self.request, messages.SUCCESS,
                                     "Campaign has been created successfully!")
                return super().form_valid(form)
        return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(CampaignCreateView, self).get_form_kwargs()
        if self.form_class:
            kwargs.update({'request': self.request})
            kwargs.update({'object': None})
        return kwargs

    def get_success_url(self):
        return reverse('donation_bank:bank_add_campaign')

    def get_context_data(self, **kwargs):
        context = super(CampaignCreateView,
                        self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        context['page_title'] = "Add Campaign"
        qs = DonationBank.objects.filter(bank_member__user=self.request.user)
        bank_object = None
        if qs.exists():
            bank_object = qs.first()
        context['object'] = bank_object
        return context

    def user_passes_test(self, request):
        qs = DonationBank.objects.filter(
            bank_member__user=request.user, is_verified=True)
        if qs.exists() and self.request.user.profile.account_type == 1:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(CampaignCreateView, self).dispatch(request, *args, **kwargs)


@method_decorator(decorators, name='dispatch')
@method_decorator(can_manage_bank_required, name='dispatch')
class CampaignListView(ListView):
    template_name = 'donationBank/campaign-list.html'
    context_object_name = 'campaign_list'

    def get_queryset(self):
        user = self.request.user
        bank_qs = DonationBank.objects.filter(
            bank_member__user=user, is_verified=True)
        if bank_qs.exists():
            bank = bank_qs.first()
            qs = Campaign.objects.filter(bank__slug=bank.slug)
            if qs.exists():
                return qs
        return None

    def get_context_data(self, **kwargs):
        context = super(CampaignListView,
                        self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        qs = DonationBank.objects.filter(bank_member__user=self.request.user)
        bank_object = None
        if qs.exists():
            bank_object = qs.first()
        context['object'] = bank_object
        return context

    def user_passes_test(self, request):
        qs = DonationBank.objects.filter(
            bank_member__user=request.user, is_verified=True)
        if qs.exists() and self.request.user.profile.account_type == 1:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(CampaignListView, self).dispatch(request, *args, **kwargs)


@method_decorator(decorators, name='dispatch')
class CampaignPublicListView(ListView):
    template_name = 'donationBank/campaign-list-public.html'
    context_object_name = 'campaign_list'

    def get_queryset(self):
        qs = Campaign.objects.all().bank_is_public().bank_is_verified().dynamic_order()
        return qs

    def get_context_data(self, **kwargs):
        context = super(CampaignPublicListView,
                        self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        campaigns = Campaign.objects.all().bank_is_public(
        ).bank_is_verified().dynamic_order()
        context['campaigns_count'] = len(campaigns)
        # Ends Base Template Context
        return context

    def user_passes_test(self, request):
        if self.request.user.is_authenticated:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(CampaignPublicListView, self).dispatch(request, *args, **kwargs)


@method_decorator(decorators, name='dispatch')
class CampaignDetailView(DetailView):
    template_name = 'donationBank/campaign-details.html'
    context_object_name = 'campaign'

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        qs = Campaign.objects.filter(slug=slug)
        if qs.exists():
            return qs.first()
        return None

    def get_context_data(self, **kwargs):
        context = super(CampaignDetailView, self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        qs = DonationBank.objects.filter(bank_member__user=self.request.user)
        bank_object = None
        if qs.exists():
            bank_object = qs.first()
        context['object'] = bank_object
        return context

    def user_passes_test(self, request):
        self.object = self.get_object()
        # qs = DonationBank.objects.filter(
        #     slug=self.object.bank.slug, bank_member__user=request.user
        # )
        # if qs.exists() and self.request.user.profile.account_type == 1:
        if self.request.user.is_authenticated:
            # if self.object.bank.institute == request.user.user_bank_member.bank.institute:
            #     return True
            # elif not self.object.bank.institute == request.user.user_bank_member.bank.institute and self.object.bank.bank_setting.privacy == 0:
            #     return True
            # else:
            #     return False
            if self.object.bank.bank_setting.privacy == 0:
                return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(CampaignDetailView, self).dispatch(request, *args, **kwargs)


@method_decorator(decorators, name='dispatch')
@method_decorator(can_manage_bank_required, name='dispatch')
class CampaignUpdateView(UpdateView):
    template_name = 'donationBank/campaign-manage.html'
    form_class = CampaignManageForm

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        qs = Campaign.objects.filter(slug=slug)
        if qs.exists():
            return qs.first()
        return None

    def form_valid(self, form):
        user = self.request.user
        self.object = self.get_object()
        bank_qs = DonationBank.objects.filter(bank_member__user=user)
        if bank_qs.exists():
            campaign_qs = Campaign.objects.filter(
                bank=bank_qs.first(), title__iexact=form.instance.title).exclude(title__iexact=self.object.title)
            if campaign_qs.exists():
                form.add_error(
                    'title', forms.ValidationError(
                        "Campaign name already exists. Please choose another name."
                    )
                )
            else:
                form.instance.bank = bank_qs.first()
                messages.add_message(self.request, messages.SUCCESS,
                                     "Campaign has been updated successfully!")
                return super().form_valid(form)
        return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(CampaignUpdateView, self).get_form_kwargs()
        if self.form_class:
            kwargs.update({'request': self.request})
            kwargs.update({'object': self.get_object()})
        return kwargs

    def get_success_url(self):
        return reverse('donation_bank:bank_campaign_list')

    def get_context_data(self, **kwargs):
        context = super(CampaignUpdateView,
                        self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        context['page_title'] = "Update Campaign"
        qs = DonationBank.objects.filter(bank_member__user=self.request.user)
        bank_object = None
        if qs.exists():
            bank_object = qs.first()
        context['object'] = bank_object
        return context

    def user_passes_test(self, request):
        self.object = self.get_object()
        qs = DonationBank.objects.filter(bank_member__user=request.user, slug=self.object.bank.slug)
        if qs.exists() and self.request.user.profile.account_type == 1:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(CampaignUpdateView, self).dispatch(request, *args, **kwargs)


@csrf_exempt
@login_required
@can_browse_required
@can_manage_bank_required
def campaign_delete(request):
    url = reverse('home')
    user = request.user
    if request.method == "POST":
        slug = request.POST.get("slug")
        qs = Campaign.objects.filter(slug=slug)
        if qs.exists():
            qs.delete()
            messages.add_message(request, messages.SUCCESS,
                                 "Deleted successfully!")
            url = reverse('donation_bank:bank_campaign_list')
        else:
            messages.add_message(request, messages.WARNING,
                                 "Not found!")
    return HttpResponseRedirect(url)


# @method_decorator(decorators, name='dispatch')
# @method_decorator(can_manage_bank_required, name='dispatch')
# class BankReportTemplateView(TemplateView):
#     def get(self, request, *args, **kwargs):
#         user = request.user
#         qs = DonationBank.objects.filter(bank_member__user=self.request.user)
#         bank_object = None
#         if qs.exists():
#             bank_object = qs.first()
#         context['object'] = bank_object
#         # Starts Base Template Context
#         if self.request.user.is_superuser:
#             base_template = 'admin-site/base.html'
#         else:
#             base_template = 'base.html'
#         # Ends Base Template Context
#         context = {
#             'base_template': base_template,
#         }
#         return render(request, "donationBank/reports/index.html", context=context)


@method_decorator(decorators, name='dispatch')
@method_decorator(can_manage_bank_required, name='dispatch')
class BankReportTemplateView(TemplateView):
    template_name = "donationBank/reports/index.html"

    def get_context_data(self, **kwargs):
        context = super(BankReportTemplateView,
                        self).get_context_data(**kwargs)
        context['page_title'] = "Bank Reports"
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        # Starts Bank Object
        bank_object = None
        slug = self.kwargs.get('slug')
        if self.request.user.is_superuser:
            qs = DonationBank.objects.filter(slug=slug)
            if qs.exists():
                bank_object = qs.first()
        else:
            qs = DonationBank.objects.filter(bank_member__user=self.request.user)
            if qs.exists():
                bank_object = qs.first()
        context['object'] = bank_object
        # Ends Bank Object
        # Report Data Starts
        context['total_donation'] = Donation.objects.filter(
            bank=bank_object)
        context['total_donation_request'] = DonationRequest.objects.filter(
            bank=bank_object)
        context['total_donation_pending'] = Donation.objects.filter(
            bank=bank_object).is_pending()
        context['total_donation_request_pending'] = DonationRequest.objects.filter(
            bank=bank_object).is_pending()
        context['total_donation_successful'] = Donation.objects.filter(
            bank=bank_object).is_done()
        context['total_donation_request_successful'] = DonationRequest.objects.filter(
            bank=bank_object).is_done()
        context['total_donation_expired'] = Donation.objects.filter(
            bank=bank_object).is_expired_pending()
        context['total_campaign'] = Campaign.objects.filter(
            bank=bank_object)
        context['total_member'] = BankMember.objects.filter(
            bank=bank_object)
        context['donation_a_pos'] = Donation.objects.filter(
            bank=bank_object, blood_group__iexact="A+")
        context['donation_a_neg'] = Donation.objects.filter(
            bank=bank_object, blood_group__iexact="A-")
        context['donation_b_pos'] = Donation.objects.filter(
            bank=bank_object, blood_group__iexact="B+")
        context['donation_b_neg'] = Donation.objects.filter(
            bank=bank_object, blood_group__iexact="B-")
        context['donation_ab_pos'] = Donation.objects.filter(
            bank=bank_object, blood_group__iexact="AB+")
        context['donation_ab_neg'] = Donation.objects.filter(
            bank=bank_object, blood_group__iexact="AB-")
        context['donation_o_pos'] = Donation.objects.filter(
            bank=bank_object, blood_group__iexact="O+")
        context['donation_o_neg'] = Donation.objects.filter(
            bank=bank_object, blood_group__iexact="O-")
        context['donation_request_a_pos'] = DonationRequest.objects.filter(
            bank=bank_object, blood_group__iexact="A+")
        context['donation_request_a_neg'] = DonationRequest.objects.filter(
            bank=bank_object, blood_group__iexact="A-")
        context['donation_request_b_pos'] = DonationRequest.objects.filter(
            bank=bank_object, blood_group__iexact="B+")
        context['donation_request_b_neg'] = DonationRequest.objects.filter(
            bank=bank_object, blood_group__iexact="B-")
        context['donation_request_ab_pos'] = DonationRequest.objects.filter(
            bank=bank_object, blood_group__iexact="AB+")
        context['donation_request_ab_neg'] = DonationRequest.objects.filter(
            bank=bank_object, blood_group__iexact="AB-")
        context['donation_request_o_pos'] = DonationRequest.objects.filter(
            bank=bank_object, blood_group__iexact="O+")
        context['donation_request_o_neg'] = DonationRequest.objects.filter(
            bank=bank_object, blood_group__iexact="O-")
        context['donation_blood'] = Donation.objects.filter(
            bank=bank_object).blood_type()
        context['donation_organ'] = Donation.objects.filter(
            bank=bank_object).organ_type()
        context['donation_tissue'] = Donation.objects.filter(
            bank=bank_object).tissue_type()
        context['donation_request_blood'] = DonationRequest.objects.filter(
            bank=bank_object).blood_type()
        context['donation_request_organ'] = DonationRequest.objects.filter(
            bank=bank_object).organ_type()
        context['donation_request_tissue'] = DonationRequest.objects.filter(
            bank=bank_object).tissue_type()
        context['blood_donation_a_pos'] = Donation.objects.filter(
            bank=bank_object, blood_group__iexact="A+").blood_type()
        context['blood_donation_a_neg'] = Donation.objects.filter(
            bank=bank_object, blood_group__iexact="A-").blood_type()
        context['blood_donation_b_pos'] = Donation.objects.filter(
            bank=bank_object, blood_group__iexact="B+").blood_type()
        context['blood_donation_b_neg'] = Donation.objects.filter(
            bank=bank_object, blood_group__iexact="B-").blood_type()
        context['blood_donation_ab_pos'] = Donation.objects.filter(
            bank=bank_object, blood_group__iexact="AB+").blood_type()
        context['blood_donation_ab_neg'] = Donation.objects.filter(
            bank=bank_object, blood_group__iexact="AB-").blood_type()
        context['blood_donation_o_pos'] = Donation.objects.filter(
            bank=bank_object, blood_group__iexact="O+").blood_type()
        context['blood_donation_o_neg'] = Donation.objects.filter(
            bank=bank_object, blood_group__iexact="O-").blood_type()
        context['blood_donation_request_a_pos'] = DonationRequest.objects.filter(
            bank=bank_object, blood_group__iexact="A+").blood_type()
        context['blood_donation_request_a_neg'] = DonationRequest.objects.filter(
            bank=bank_object, blood_group__iexact="A-").blood_type()
        context['blood_donation_request_b_pos'] = DonationRequest.objects.filter(
            bank=bank_object, blood_group__iexact="B+").blood_type()
        context['blood_donation_request_b_neg'] = DonationRequest.objects.filter(
            bank=bank_object, blood_group__iexact="B-").blood_type()
        context['blood_donation_request_ab_pos'] = DonationRequest.objects.filter(
            bank=bank_object, blood_group__iexact="AB+").blood_type()
        context['blood_donation_request_ab_neg'] = DonationRequest.objects.filter(
            bank=bank_object, blood_group__iexact="AB-").blood_type()
        context['blood_donation_request_o_pos'] = DonationRequest.objects.filter(
            bank=bank_object, blood_group__iexact="O+").blood_type()
        context['blood_donation_request_o_neg'] = DonationRequest.objects.filter(
            bank=bank_object, blood_group__iexact="O-").blood_type()
        # Organ Donation Categorywise
        context['organ_donation_heart'] = Donation.objects.filter(
            bank=bank_object, organ_name__iexact="Heart").organ_type()
        context['organ_donation_kidney'] = Donation.objects.filter(
            bank=bank_object, organ_name__iexact="Kidney").organ_type()
        context['organ_donation_pancreas'] = Donation.objects.filter(
            bank=bank_object, organ_name__iexact="Pancreas").organ_type()
        context['organ_donation_lungs'] = Donation.objects.filter(
            bank=bank_object, organ_name__iexact="Lungs").organ_type()
        context['organ_donation_liver'] = Donation.objects.filter(
            bank=bank_object, organ_name__iexact="Liver").organ_type()
        context['organ_donation_intestines'] = Donation.objects.filter(
            bank=bank_object, organ_name__iexact="Intestines").organ_type()
        # Organ Donation Request Categorywise
        context['organ_donation_request_heart'] = DonationRequest.objects.filter(
            bank=bank_object, organ_name__iexact="Heart").organ_type()
        context['organ_donation_request_kidney'] = DonationRequest.objects.filter(
            bank=bank_object, organ_name__iexact="Kidney").organ_type()
        context['organ_donation_request_pancreas'] = DonationRequest.objects.filter(
            bank=bank_object, organ_name__iexact="Pancreas").organ_type()
        context['organ_donation_request_lungs'] = DonationRequest.objects.filter(
            bank=bank_object, organ_name__iexact="Lungs").organ_type()
        context['organ_donation_request_liver'] = DonationRequest.objects.filter(
            bank=bank_object, organ_name__iexact="Liver").organ_type()
        context['organ_donation_request_intestines'] = DonationRequest.objects.filter(
            bank=bank_object, organ_name__iexact="Intestines").organ_type()
        # Tissue Donation Categorywise
        context['tissue_donation_bones'] = Donation.objects.filter(
            bank=bank_object, tissue_name__iexact="Bones'").tissue_type()
        context['tissue_donation_ligaments'] = Donation.objects.filter(
            bank=bank_object, tissue_name__iexact="Ligaments").tissue_type()
        context['tissue_donation_tendons'] = Donation.objects.filter(
            bank=bank_object, tissue_name__iexact="Tendons").tissue_type()
        context['tissue_donation_fascia'] = Donation.objects.filter(
            bank=bank_object, tissue_name__iexact="Fascia").tissue_type()
        context['tissue_donation_veins'] = Donation.objects.filter(
            bank=bank_object, tissue_name__iexact="Veins").tissue_type()
        context['tissue_donation_nerves'] = Donation.objects.filter(
            bank=bank_object, tissue_name__iexact="Nerves").tissue_type()
        context['tissue_donation_corneas'] = Donation.objects.filter(
            bank=bank_object, tissue_name__iexact="Corneas").tissue_type()
        context['tissue_donation_sclera'] = Donation.objects.filter(
            bank=bank_object, tissue_name__iexact="Sclera").tissue_type()
        context['tissue_donation_heart_valves'] = Donation.objects.filter(
            bank=bank_object, tissue_name__iexact="Heart Valves").tissue_type()
        context['tissue_donation_skin'] = Donation.objects.filter(
            bank=bank_object, tissue_name__iexact="Skin").tissue_type()
        # Tissue Donation Request Categorywise
        context['tissue_donation_request_bones'] = DonationRequest.objects.filter(
            bank=bank_object, tissue_name__iexact="Bones'").tissue_type()
        context['tissue_donation_request_ligaments'] = DonationRequest.objects.filter(
            bank=bank_object, tissue_name__iexact="Ligaments").tissue_type()
        context['tissue_donation_request_tendons'] = DonationRequest.objects.filter(
            bank=bank_object, tissue_name__iexact="Tendons").tissue_type()
        context['tissue_donation_request_fascia'] = DonationRequest.objects.filter(
            bank=bank_object, tissue_name__iexact="Fascia").tissue_type()
        context['tissue_donation_request_veins'] = DonationRequest.objects.filter(
            bank=bank_object, tissue_name__iexact="Veins").tissue_type()
        context['tissue_donation_request_nerves'] = DonationRequest.objects.filter(
            bank=bank_object, tissue_name__iexact="Nerves").tissue_type()
        context['tissue_donation_request_corneas'] = DonationRequest.objects.filter(
            bank=bank_object, tissue_name__iexact="Corneas").tissue_type()
        context['tissue_donation_request_sclera'] = DonationRequest.objects.filter(
            bank=bank_object, tissue_name__iexact="Sclera").tissue_type()
        context['tissue_donation_request_heart_valves'] = DonationRequest.objects.filter(
            bank=bank_object, tissue_name__iexact="Heart Valves").tissue_type()
        context['tissue_donation_request_skin'] = DonationRequest.objects.filter(
            bank=bank_object, tissue_name__iexact="Skin").tissue_type()
        # Report Data Ends
        return context

    def user_passes_test(self, request):
        if self.request.user.is_superuser:
            return True
        else:
            qs = DonationBank.objects.filter(
                bank_member__user=request.user, slug=self.request.user.user_bank_member.bank.slug)
            if qs.exists() and self.request.user.profile.account_type == 1:
                return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(BankReportTemplateView, self).dispatch(request, *args, **kwargs)


@method_decorator(decorators, name='dispatch')
@method_decorator(can_manage_bank_required, name='dispatch')
class BankChartFilterTemplateView(TemplateView):
    template_name = "donationBank/reports/index.html"

    def get_context_data(self, **kwargs):
        context = super(BankChartFilterTemplateView,
                        self).get_context_data(**kwargs)
        context['page_title'] = "Bank Reports"
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        # Starts Bank Object
        bank_object = None
        slug = self.kwargs.get('slug')
        if self.request.user.is_superuser:
            qs = DonationBank.objects.filter(slug=slug)
            if qs.exists():
                bank_object = qs.first()
        else:
            qs = DonationBank.objects.filter(
                bank_member__user=self.request.user)
            if qs.exists():
                bank_object = qs.first()
        context['object'] = bank_object
        # Ends Bank Object
        # Report Data Starts
        query_context = self.request.GET.get('q')
        query_context_date_from = self.request.GET.get('date-from')
        query_context_date_to = self.request.GET.get('date-to')
        context['query'] = query_context
        context['query_date_from'] = query_context_date_from
        context['query_date_to'] = query_context_date_to
        # Query Start
        request = self.request
        method_dict = request.GET
        query = method_dict.get('q', None)
        date_from_filtered = method_dict.get('date-from', None)
        date_to_filtered = method_dict.get('date-to', None)
        if not date_from_filtered == "" and date_to_filtered == "":
            date_to_filtered = datetime.datetime.now()
        if date_from_filtered == "" and not date_to_filtered == "":
            date_from_filtered = datetime.datetime.now()
        # else:
        #     filter_modules_dict = {}
        # #  ------------------------- Magic Starts -------------------------
        # from collections import OrderedDict
        # ordered_dict = OrderedDict(filter_modules_dict)

        # list_pre = []
        # for key, value in ordered_dict.items():
        #     if value:
        #         list_pre.append(f"{key}+ {value}")
        # list_to_dict_like_string = ", ".join(list_pre)
        # string_to_dict = dict((x.strip(), y.strip()) for x, y in (
        #     element.split('+') for element in list_to_dict_like_string.split(', ')))

        # filter_dict = string_to_dict
        # #  ------------------------- Magic Ends -------------------------
        if query is not None and not date_from_filtered == "" and not date_to_filtered == "":
            # print("QUERY With DATE!!!")
            context['total_donation'] = Donation.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object)
            context['total_donation_request'] = DonationRequest.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object)
            context['total_donation_pending'] = Donation.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object).is_pending()
            context['total_donation_request_pending'] = DonationRequest.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object).is_pending()
            context['total_donation_successful'] = Donation.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object).is_done()
            context['total_donation_request_successful'] = DonationRequest.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object).is_done()
            context['total_donation_expired'] = Donation.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object).is_expired_pending()
            context['total_campaign'] = Campaign.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object)
            context['total_member'] = BankMember.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object)
            context['donation_a_pos'] = Donation.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="A+")
            context['donation_a_neg'] = Donation.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="A-")
            context['donation_b_pos'] = Donation.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="B+")
            context['donation_b_neg'] = Donation.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="B-")
            context['donation_ab_pos'] = Donation.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="AB+")
            context['donation_ab_neg'] = Donation.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="AB-")
            context['donation_o_pos'] = Donation.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="O+")
            context['donation_o_neg'] = Donation.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="O-")
            context['donation_request_a_pos'] = DonationRequest.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="A+")
            context['donation_request_a_neg'] = DonationRequest.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="A-")
            context['donation_request_b_pos'] = DonationRequest.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="B+")
            context['donation_request_b_neg'] = DonationRequest.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="B-")
            context['donation_request_ab_pos'] = DonationRequest.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="AB+")
            context['donation_request_ab_neg'] = DonationRequest.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="AB-")
            context['donation_request_o_pos'] = DonationRequest.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="O+")
            context['donation_request_o_neg'] = DonationRequest.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="O-")
            context['donation_blood'] = Donation.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object).blood_type()
            context['donation_organ'] = Donation.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object).organ_type()
            context['donation_tissue'] = Donation.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object).tissue_type()
            context['donation_request_blood'] = DonationRequest.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object).blood_type()
            context['donation_request_organ'] = DonationRequest.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object).organ_type()
            context['donation_request_tissue'] = DonationRequest.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object).tissue_type()
            context['blood_donation_a_pos'] = Donation.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="A+").blood_type()
            context['blood_donation_a_neg'] = Donation.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="A-").blood_type()
            context['blood_donation_b_pos'] = Donation.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="B+").blood_type()
            context['blood_donation_b_neg'] = Donation.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="B-").blood_type()
            context['blood_donation_ab_pos'] = Donation.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="AB+").blood_type()
            context['blood_donation_ab_neg'] = Donation.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="AB-").blood_type()
            context['blood_donation_o_pos'] = Donation.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="O+").blood_type()
            context['blood_donation_o_neg'] = Donation.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="O-").blood_type()
            context['blood_donation_request_a_pos'] = DonationRequest.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="A+").blood_type()
            context['blood_donation_request_a_neg'] = DonationRequest.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="A-").blood_type()
            context['blood_donation_request_b_pos'] = DonationRequest.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="B+").blood_type()
            context['blood_donation_request_b_neg'] = DonationRequest.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="B-").blood_type()
            context['blood_donation_request_ab_pos'] = DonationRequest.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="AB+").blood_type()
            context['blood_donation_request_ab_neg'] = DonationRequest.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="AB-").blood_type()
            context['blood_donation_request_o_pos'] = DonationRequest.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="O+").blood_type()
            context['blood_donation_request_o_neg'] = DonationRequest.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="O-").blood_type()
            # Organ Donation Categorywise
            context['organ_donation_heart'] = Donation.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, organ_name__iexact="Heart").organ_type()
            context['organ_donation_kidney'] = Donation.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, organ_name__iexact="Kidney").organ_type()
            context['organ_donation_pancreas'] = Donation.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, organ_name__iexact="Pancreas").organ_type()
            context['organ_donation_lungs'] = Donation.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, organ_name__iexact="Lungs").organ_type()
            context['organ_donation_liver'] = Donation.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, organ_name__iexact="Liver").organ_type()
            context['organ_donation_intestines'] = Donation.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, organ_name__iexact="Intestines").organ_type()
            # Organ Donation Request Categorywise
            context['organ_donation_request_heart'] = DonationRequest.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, organ_name__iexact="Heart").organ_type()
            context['organ_donation_request_kidney'] = DonationRequest.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, organ_name__iexact="Kidney").organ_type()
            context['organ_donation_request_pancreas'] = DonationRequest.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, organ_name__iexact="Pancreas").organ_type()
            context['organ_donation_request_lungs'] = DonationRequest.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, organ_name__iexact="Lungs").organ_type()
            context['organ_donation_request_liver'] = DonationRequest.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, organ_name__iexact="Liver").organ_type()
            context['organ_donation_request_intestines'] = DonationRequest.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, organ_name__iexact="Intestines").organ_type()
            # Tissue Donation Categorywise
            context['tissue_donation_bones'] = Donation.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, tissue_name__iexact="Bones'").tissue_type()
            context['tissue_donation_ligaments'] = Donation.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, tissue_name__iexact="Ligaments").tissue_type()
            context['tissue_donation_tendons'] = Donation.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, tissue_name__iexact="Tendons").tissue_type()
            context['tissue_donation_fascia'] = Donation.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, tissue_name__iexact="Fascia").tissue_type()
            context['tissue_donation_veins'] = Donation.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, tissue_name__iexact="Veins").tissue_type()
            context['tissue_donation_nerves'] = Donation.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, tissue_name__iexact="Nerves").tissue_type()
            context['tissue_donation_corneas'] = Donation.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, tissue_name__iexact="Corneas").tissue_type()
            context['tissue_donation_sclera'] = Donation.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, tissue_name__iexact="Sclera").tissue_type()
            context['tissue_donation_heart_valves'] = Donation.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, tissue_name__iexact="Heart Valves").tissue_type()
            context['tissue_donation_skin'] = Donation.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, tissue_name__iexact="Skin").tissue_type()
            # Tissue Donation Request Categorywise
            context['tissue_donation_request_bones'] = DonationRequest.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, tissue_name__iexact="Bones'").tissue_type()
            context['tissue_donation_request_ligaments'] = DonationRequest.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, tissue_name__iexact="Ligaments").tissue_type()
            context['tissue_donation_request_tendons'] = DonationRequest.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, tissue_name__iexact="Tendons").tissue_type()
            context['tissue_donation_request_fascia'] = DonationRequest.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, tissue_name__iexact="Fascia").tissue_type()
            context['tissue_donation_request_veins'] = DonationRequest.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, tissue_name__iexact="Veins").tissue_type()
            context['tissue_donation_request_nerves'] = DonationRequest.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, tissue_name__iexact="Nerves").tissue_type()
            context['tissue_donation_request_corneas'] = DonationRequest.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, tissue_name__iexact="Corneas").tissue_type()
            context['tissue_donation_request_sclera'] = DonationRequest.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, tissue_name__iexact="Sclera").tissue_type()
            context['tissue_donation_request_heart_valves'] = DonationRequest.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, tissue_name__iexact="Heart Valves").tissue_type()
            context['tissue_donation_request_skin'] = DonationRequest.objects.search(
                    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, tissue_name__iexact="Skin").tissue_type()
        elif query is None and not date_from_filtered == "" and not date_to_filtered == "":
            # print("DATE!!!")
            context['total_donation'] = Donation.objects.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object)
            context['total_donation_request'] = DonationRequest.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object)
            context['total_donation_pending'] = Donation.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object).is_pending()
            context['total_donation_request_pending'] = DonationRequest.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object).is_pending()
            context['total_donation_successful'] = Donation.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object).is_done()
            context['total_donation_request_successful'] = DonationRequest.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object).is_done()
            context['total_donation_expired'] = Donation.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object).is_expired_pending()
            context['total_campaign'] = Campaign.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object)
            context['total_member'] = BankMember.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object)
            context['donation_a_pos'] = Donation.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="A+")
            context['donation_a_neg'] = Donation.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="A-")
            context['donation_b_pos'] = Donation.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="B+")
            context['donation_b_neg'] = Donation.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="B-")
            context['donation_ab_pos'] = Donation.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="AB+")
            context['donation_ab_neg'] = Donation.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="AB-")
            context['donation_o_pos'] = Donation.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="O+")
            context['donation_o_neg'] = Donation.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="O-")
            context['donation_request_a_pos'] = DonationRequest.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="A+")
            context['donation_request_a_neg'] = DonationRequest.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="A-")
            context['donation_request_b_pos'] = DonationRequest.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="B+")
            context['donation_request_b_neg'] = DonationRequest.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="B-")
            context['donation_request_ab_pos'] = DonationRequest.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="AB+")
            context['donation_request_ab_neg'] = DonationRequest.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="AB-")
            context['donation_request_o_pos'] = DonationRequest.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="O+")
            context['donation_request_o_neg'] = DonationRequest.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="O-")
            context['donation_blood'] = Donation.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object).blood_type()
            context['donation_organ'] = Donation.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object).organ_type()
            context['donation_tissue'] = Donation.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object).tissue_type()
            context['donation_request_blood'] = DonationRequest.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object).blood_type()
            context['donation_request_organ'] = DonationRequest.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object).organ_type()
            context['donation_request_tissue'] = DonationRequest.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object).tissue_type()
            context['blood_donation_a_pos'] = Donation.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="A+").blood_type()
            context['blood_donation_a_neg'] = Donation.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="A-").blood_type()
            context['blood_donation_b_pos'] = Donation.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="B+").blood_type()
            context['blood_donation_b_neg'] = Donation.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="B-").blood_type()
            context['blood_donation_ab_pos'] = Donation.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="AB+").blood_type()
            context['blood_donation_ab_neg'] = Donation.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="AB-").blood_type()
            context['blood_donation_o_pos'] = Donation.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="O+").blood_type()
            context['blood_donation_o_neg'] = Donation.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="O-").blood_type()
            context['blood_donation_request_a_pos'] = DonationRequest.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="A+").blood_type()
            context['blood_donation_request_a_neg'] = DonationRequest.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="A-").blood_type()
            context['blood_donation_request_b_pos'] = DonationRequest.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="B+").blood_type()
            context['blood_donation_request_b_neg'] = DonationRequest.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="B-").blood_type()
            context['blood_donation_request_ab_pos'] = DonationRequest.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="AB+").blood_type()
            context['blood_donation_request_ab_neg'] = DonationRequest.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="AB-").blood_type()
            context['blood_donation_request_o_pos'] = DonationRequest.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="O+").blood_type()
            context['blood_donation_request_o_neg'] = DonationRequest.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, blood_group__iexact="O-").blood_type()
            # Organ Donation Categorywise
            context['organ_donation_heart'] = Donation.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, organ_name__iexact="Heart").organ_type()
            context['organ_donation_kidney'] = Donation.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, organ_name__iexact="Kidney").organ_type()
            context['organ_donation_pancreas'] = Donation.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, organ_name__iexact="Pancreas").organ_type()
            context['organ_donation_lungs'] = Donation.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, organ_name__iexact="Lungs").organ_type()
            context['organ_donation_liver'] = Donation.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, organ_name__iexact="Liver").organ_type()
            context['organ_donation_intestines'] = Donation.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, organ_name__iexact="Intestines").organ_type()
            # Organ Donation Request Categorywise
            context['organ_donation_request_heart'] = DonationRequest.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, organ_name__iexact="Heart").organ_type()
            context['organ_donation_request_kidney'] = DonationRequest.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, organ_name__iexact="Kidney").organ_type()
            context['organ_donation_request_pancreas'] = DonationRequest.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, organ_name__iexact="Pancreas").organ_type()
            context['organ_donation_request_lungs'] = DonationRequest.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, organ_name__iexact="Lungs").organ_type()
            context['organ_donation_request_liver'] = DonationRequest.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, organ_name__iexact="Liver").organ_type()
            context['organ_donation_request_intestines'] = DonationRequest.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, organ_name__iexact="Intestines").organ_type()
            # Tissue Donation Categorywise
            context['tissue_donation_bones'] = Donation.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, tissue_name__iexact="Bones'").tissue_type()
            context['tissue_donation_ligaments'] = Donation.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, tissue_name__iexact="Ligaments").tissue_type()
            context['tissue_donation_tendons'] = Donation.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, tissue_name__iexact="Tendons").tissue_type()
            context['tissue_donation_fascia'] = Donation.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, tissue_name__iexact="Fascia").tissue_type()
            context['tissue_donation_veins'] = Donation.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, tissue_name__iexact="Veins").tissue_type()
            context['tissue_donation_nerves'] = Donation.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, tissue_name__iexact="Nerves").tissue_type()
            context['tissue_donation_corneas'] = Donation.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, tissue_name__iexact="Corneas").tissue_type()
            context['tissue_donation_sclera'] = Donation.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, tissue_name__iexact="Sclera").tissue_type()
            context['tissue_donation_heart_valves'] = Donation.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, tissue_name__iexact="Heart Valves").tissue_type()
            context['tissue_donation_skin'] = Donation.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, tissue_name__iexact="Skin").tissue_type()
            # Tissue Donation Request Categorywise
            context['tissue_donation_request_bones'] = DonationRequest.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, tissue_name__iexact="Bones'").tissue_type()
            context['tissue_donation_request_ligaments'] = DonationRequest.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, tissue_name__iexact="Ligaments").tissue_type()
            context['tissue_donation_request_tendons'] = DonationRequest.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, tissue_name__iexact="Tendons").tissue_type()
            context['tissue_donation_request_fascia'] = DonationRequest.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, tissue_name__iexact="Fascia").tissue_type()
            context['tissue_donation_request_veins'] = DonationRequest.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, tissue_name__iexact="Veins").tissue_type()
            context['tissue_donation_request_nerves'] = DonationRequest.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, tissue_name__iexact="Nerves").tissue_type()
            context['tissue_donation_request_corneas'] = DonationRequest.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, tissue_name__iexact="Corneas").tissue_type()
            context['tissue_donation_request_sclera'] = DonationRequest.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, tissue_name__iexact="Sclera").tissue_type()
            context['tissue_donation_request_heart_valves'] = DonationRequest.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, tissue_name__iexact="Heart Valves").tissue_type()
            context['tissue_donation_request_skin'] = DonationRequest.filter(
                    created_at__range=(date_from_filtered, date_to_filtered)).filter(
                bank=bank_object, tissue_name__iexact="Skin").tissue_type()
        elif not query == None and date_from_filtered == "" or date_to_filtered == "":
            # print("QUERY!!!")
            context['total_donation'] = Donation.objects.search(
                query).filter(
                bank=bank_object)
            context['total_donation_request'] = DonationRequest.objects.search(
                query).filter(
                bank=bank_object)
            context['total_donation_pending'] = Donation.objects.search(
                query).filter(
                bank=bank_object).is_pending()
            context['total_donation_request_pending'] = DonationRequest.objects.search(
                query).filter(
                bank=bank_object).is_pending()
            context['total_donation_successful'] = Donation.objects.search(
                query).filter(
                bank=bank_object).is_done()
            context['total_donation_request_successful'] = DonationRequest.objects.search(
                query).filter(
                bank=bank_object).is_done()
            context['total_donation_expired'] = Donation.objects.search(
                query).filter(
                bank=bank_object).is_expired_pending()
            context['total_campaign'] = Campaign.objects.search(
                query).filter(
                bank=bank_object)
            context['total_member'] = BankMember.objects.search(
                query).filter(
                bank=bank_object)
            context['donation_a_pos'] = Donation.objects.search(
                query).filter(
                bank=bank_object, blood_group__iexact="A+")
            context['donation_a_neg'] = Donation.objects.search(
                query).filter(
                bank=bank_object, blood_group__iexact="A-")
            context['donation_b_pos'] = Donation.objects.search(
                query).filter(
                bank=bank_object, blood_group__iexact="B+")
            context['donation_b_neg'] = Donation.objects.search(
                query).filter(
                bank=bank_object, blood_group__iexact="B-")
            context['donation_ab_pos'] = Donation.objects.search(
                query).filter(
                bank=bank_object, blood_group__iexact="AB+")
            context['donation_ab_neg'] = Donation.objects.search(
                query).filter(
                bank=bank_object, blood_group__iexact="AB-")
            context['donation_o_pos'] = Donation.objects.search(
                query).filter(
                bank=bank_object, blood_group__iexact="O+")
            context['donation_o_neg'] = Donation.objects.search(
                query).filter(
                bank=bank_object, blood_group__iexact="O-")
            context['donation_request_a_pos'] = DonationRequest.objects.search(
                query).filter(
                bank=bank_object, blood_group__iexact="A+")
            context['donation_request_a_neg'] = DonationRequest.objects.search(
                query).filter(
                bank=bank_object, blood_group__iexact="A-")
            context['donation_request_b_pos'] = DonationRequest.objects.search(
                query).filter(
                bank=bank_object, blood_group__iexact="B+")
            context['donation_request_b_neg'] = DonationRequest.objects.search(
                query).filter(
                bank=bank_object, blood_group__iexact="B-")
            context['donation_request_ab_pos'] = DonationRequest.objects.search(
                query).filter(
                bank=bank_object, blood_group__iexact="AB+")
            context['donation_request_ab_neg'] = DonationRequest.objects.search(
                query).filter(
                bank=bank_object, blood_group__iexact="AB-")
            context['donation_request_o_pos'] = DonationRequest.objects.search(
                query).filter(
                bank=bank_object, blood_group__iexact="O+")
            context['donation_request_o_neg'] = DonationRequest.objects.search(
                query).filter(
                bank=bank_object, blood_group__iexact="O-")
            context['donation_blood'] = Donation.objects.search(
                query).filter(
                bank=bank_object).blood_type()
            context['donation_organ'] = Donation.objects.search(
                query).filter(
                bank=bank_object).organ_type()
            context['donation_tissue'] = Donation.objects.search(
                query).filter(
                bank=bank_object).tissue_type()
            context['donation_request_blood'] = DonationRequest.objects.search(
                query).filter(
                bank=bank_object).blood_type()
            context['donation_request_organ'] = DonationRequest.objects.search(
                query).filter(
                bank=bank_object).organ_type()
            context['donation_request_tissue'] = DonationRequest.objects.search(
                query).filter(
                bank=bank_object).tissue_type()
            context['blood_donation_a_pos'] = Donation.objects.search(
                query).filter(
                bank=bank_object, blood_group__iexact="A+").blood_type()
            context['blood_donation_a_neg'] = Donation.objects.search(
                query).filter(
                bank=bank_object, blood_group__iexact="A-").blood_type()
            context['blood_donation_b_pos'] = Donation.objects.search(
                query).filter(
                bank=bank_object, blood_group__iexact="B+").blood_type()
            context['blood_donation_b_neg'] = Donation.objects.search(
                query).filter(
                bank=bank_object, blood_group__iexact="B-").blood_type()
            context['blood_donation_ab_pos'] = Donation.objects.search(
                query).filter(
                bank=bank_object, blood_group__iexact="AB+").blood_type()
            context['blood_donation_ab_neg'] = Donation.objects.search(
                query).filter(
                bank=bank_object, blood_group__iexact="AB-").blood_type()
            context['blood_donation_o_pos'] = Donation.objects.search(
                query).filter(
                bank=bank_object, blood_group__iexact="O+").blood_type()
            context['blood_donation_o_neg'] = Donation.objects.search(
                query).filter(
                bank=bank_object, blood_group__iexact="O-").blood_type()
            context['blood_donation_request_a_pos'] = DonationRequest.objects.search(
                query).filter(
                bank=bank_object, blood_group__iexact="A+").blood_type()
            context['blood_donation_request_a_neg'] = DonationRequest.objects.search(
                query).filter(
                bank=bank_object, blood_group__iexact="A-").blood_type()
            context['blood_donation_request_b_pos'] = DonationRequest.objects.search(
                query).filter(
                bank=bank_object, blood_group__iexact="B+").blood_type()
            context['blood_donation_request_b_neg'] = DonationRequest.objects.search(
                query).filter(
                bank=bank_object, blood_group__iexact="B-").blood_type()
            context['blood_donation_request_ab_pos'] = DonationRequest.objects.search(
                query).filter(
                bank=bank_object, blood_group__iexact="AB+").blood_type()
            context['blood_donation_request_ab_neg'] = DonationRequest.objects.search(
                query).filter(
                bank=bank_object, blood_group__iexact="AB-").blood_type()
            context['blood_donation_request_o_pos'] = DonationRequest.objects.search(
                query).filter(
                bank=bank_object, blood_group__iexact="O+").blood_type()
            context['blood_donation_request_o_neg'] = DonationRequest.objects.search(
                query).filter(
                bank=bank_object, blood_group__iexact="O-").blood_type()
            # Organ Donation Categorywise
            context['organ_donation_heart'] = Donation.objects.search(
                query).filter(
                bank=bank_object, organ_name__iexact="Heart").organ_type()
            context['organ_donation_kidney'] = Donation.objects.search(
                query).filter(
                bank=bank_object, organ_name__iexact="Kidney").organ_type()
            context['organ_donation_pancreas'] = Donation.objects.search(
                query).filter(
                bank=bank_object, organ_name__iexact="Pancreas").organ_type()
            context['organ_donation_lungs'] = Donation.objects.search(
                query).filter(
                bank=bank_object, organ_name__iexact="Lungs").organ_type()
            context['organ_donation_liver'] = Donation.objects.search(
                query).filter(
                bank=bank_object, organ_name__iexact="Liver").organ_type()
            context['organ_donation_intestines'] = Donation.objects.search(
                query).filter(
                bank=bank_object, organ_name__iexact="Intestines").organ_type()
            # Organ Donation Request Categorywise
            context['organ_donation_request_heart'] = DonationRequest.objects.search(
                query).filter(
                bank=bank_object, organ_name__iexact="Heart").organ_type()
            context['organ_donation_request_kidney'] = DonationRequest.objects.search(
                query).filter(
                bank=bank_object, organ_name__iexact="Kidney").organ_type()
            context['organ_donation_request_pancreas'] = DonationRequest.objects.search(
                query).filter(
                bank=bank_object, organ_name__iexact="Pancreas").organ_type()
            context['organ_donation_request_lungs'] = DonationRequest.objects.search(
                query).filter(
                bank=bank_object, organ_name__iexact="Lungs").organ_type()
            context['organ_donation_request_liver'] = DonationRequest.objects.search(
                query).filter(
                bank=bank_object, organ_name__iexact="Liver").organ_type()
            context['organ_donation_request_intestines'] = DonationRequest.objects.search(
                query).filter(
                bank=bank_object, organ_name__iexact="Intestines").organ_type()
            # Tissue Donation Categorywise
            context['tissue_donation_bones'] = Donation.objects.search(
                query).filter(
                bank=bank_object, tissue_name__iexact="Bones'").tissue_type()
            context['tissue_donation_ligaments'] = Donation.objects.search(
                query).filter(
                bank=bank_object, tissue_name__iexact="Ligaments").tissue_type()
            context['tissue_donation_tendons'] = Donation.objects.search(
                query).filter(
                bank=bank_object, tissue_name__iexact="Tendons").tissue_type()
            context['tissue_donation_fascia'] = Donation.objects.search(
                query).filter(
                bank=bank_object, tissue_name__iexact="Fascia").tissue_type()
            context['tissue_donation_veins'] = Donation.objects.search(
                query).filter(
                bank=bank_object, tissue_name__iexact="Veins").tissue_type()
            context['tissue_donation_nerves'] = Donation.objects.search(
                query).filter(
                bank=bank_object, tissue_name__iexact="Nerves").tissue_type()
            context['tissue_donation_corneas'] = Donation.objects.search(
                query).filter(
                bank=bank_object, tissue_name__iexact="Corneas").tissue_type()
            context['tissue_donation_sclera'] = Donation.objects.search(
                query).filter(
                bank=bank_object, tissue_name__iexact="Sclera").tissue_type()
            context['tissue_donation_heart_valves'] = Donation.objects.search(
                query).filter(
                bank=bank_object, tissue_name__iexact="Heart Valves").tissue_type()
            context['tissue_donation_skin'] = Donation.objects.search(
                query).filter(
                bank=bank_object, tissue_name__iexact="Skin").tissue_type()
            # Tissue Donation Request Categorywise
            context['tissue_donation_request_bones'] = DonationRequest.objects.search(
                query).filter(
                bank=bank_object, tissue_name__iexact="Bones'").tissue_type()
            context['tissue_donation_request_ligaments'] = DonationRequest.objects.search(
                query).filter(
                bank=bank_object, tissue_name__iexact="Ligaments").tissue_type()
            context['tissue_donation_request_tendons'] = DonationRequest.objects.search(
                query).filter(
                bank=bank_object, tissue_name__iexact="Tendons").tissue_type()
            context['tissue_donation_request_fascia'] = DonationRequest.objects.search(
                query).filter(
                bank=bank_object, tissue_name__iexact="Fascia").tissue_type()
            context['tissue_donation_request_veins'] = DonationRequest.objects.search(
                query).filter(
                bank=bank_object, tissue_name__iexact="Veins").tissue_type()
            context['tissue_donation_request_nerves'] = DonationRequest.objects.search(
                query).filter(
                bank=bank_object, tissue_name__iexact="Nerves").tissue_type()
            context['tissue_donation_request_corneas'] = DonationRequest.objects.search(
                query).filter(
                bank=bank_object, tissue_name__iexact="Corneas").tissue_type()
            context['tissue_donation_request_sclera'] = DonationRequest.objects.search(
                query).filter(
                bank=bank_object, tissue_name__iexact="Sclera").tissue_type()
            context['tissue_donation_request_heart_valves'] = DonationRequest.objects.search(
                query).filter(
                bank=bank_object, tissue_name__iexact="Heart Valves").tissue_type()
            context['tissue_donation_request_skin'] = DonationRequest.objects.search(
                query).filter(
                bank=bank_object, tissue_name__iexact="Skin").tissue_type()
        else:
            # print("NONE!!!")
            context['total_donation'] = Donation.objects.filter(
            bank=bank_object)
            context['total_donation_request'] = DonationRequest.objects.filter(
                bank=bank_object)
            context['total_donation_pending'] = Donation.objects.filter(
                bank=bank_object).is_pending()
            context['total_donation_request_pending'] = DonationRequest.objects.filter(
                bank=bank_object).is_pending()
            context['total_donation_successful'] = Donation.objects.filter(
                bank=bank_object).is_done()
            context['total_donation_request_successful'] = DonationRequest.objects.filter(
                bank=bank_object).is_done()
            context['total_donation_expired'] = Donation.objects.filter(
                bank=bank_object).is_expired_pending()
            context['total_campaign'] = Campaign.objects.filter(
                bank=bank_object)
            context['total_member'] = BankMember.objects.filter(
                bank=bank_object)
            context['donation_a_pos'] = Donation.objects.filter(
                bank=bank_object, blood_group__iexact="A+")
            context['donation_a_neg'] = Donation.objects.filter(
                bank=bank_object, blood_group__iexact="A-")
            context['donation_b_pos'] = Donation.objects.filter(
                bank=bank_object, blood_group__iexact="B+")
            context['donation_b_neg'] = Donation.objects.filter(
                bank=bank_object, blood_group__iexact="B-")
            context['donation_ab_pos'] = Donation.objects.filter(
                bank=bank_object, blood_group__iexact="AB+")
            context['donation_ab_neg'] = Donation.objects.filter(
                bank=bank_object, blood_group__iexact="AB-")
            context['donation_o_pos'] = Donation.objects.filter(
                bank=bank_object, blood_group__iexact="O+")
            context['donation_o_neg'] = Donation.objects.filter(
                bank=bank_object, blood_group__iexact="O-")
            context['donation_request_a_pos'] = DonationRequest.objects.filter(
                bank=bank_object, blood_group__iexact="A+")
            context['donation_request_a_neg'] = DonationRequest.objects.filter(
                bank=bank_object, blood_group__iexact="A-")
            context['donation_request_b_pos'] = DonationRequest.objects.filter(
                bank=bank_object, blood_group__iexact="B+")
            context['donation_request_b_neg'] = DonationRequest.objects.filter(
                bank=bank_object, blood_group__iexact="B-")
            context['donation_request_ab_pos'] = DonationRequest.objects.filter(
                bank=bank_object, blood_group__iexact="AB+")
            context['donation_request_ab_neg'] = DonationRequest.objects.filter(
                bank=bank_object, blood_group__iexact="AB-")
            context['donation_request_o_pos'] = DonationRequest.objects.filter(
                bank=bank_object, blood_group__iexact="O+")
            context['donation_request_o_neg'] = DonationRequest.objects.filter(
                bank=bank_object, blood_group__iexact="O-")
            context['donation_blood'] = Donation.objects.filter(
                bank=bank_object).blood_type()
            context['donation_organ'] = Donation.objects.filter(
                bank=bank_object).organ_type()
            context['donation_tissue'] = Donation.objects.filter(
                bank=bank_object).tissue_type()
            context['donation_request_blood'] = DonationRequest.objects.filter(
                bank=bank_object).blood_type()
            context['donation_request_organ'] = DonationRequest.objects.filter(
                bank=bank_object).organ_type()
            context['donation_request_tissue'] = DonationRequest.objects.filter(
                bank=bank_object).tissue_type()
            context['blood_donation_a_pos'] = Donation.objects.filter(
                bank=bank_object, blood_group__iexact="A+").blood_type()
            context['blood_donation_a_neg'] = Donation.objects.filter(
                bank=bank_object, blood_group__iexact="A-").blood_type()
            context['blood_donation_b_pos'] = Donation.objects.filter(
                bank=bank_object, blood_group__iexact="B+").blood_type()
            context['blood_donation_b_neg'] = Donation.objects.filter(
                bank=bank_object, blood_group__iexact="B-").blood_type()
            context['blood_donation_ab_pos'] = Donation.objects.filter(
                bank=bank_object, blood_group__iexact="AB+").blood_type()
            context['blood_donation_ab_neg'] = Donation.objects.filter(
                bank=bank_object, blood_group__iexact="AB-").blood_type()
            context['blood_donation_o_pos'] = Donation.objects.filter(
                bank=bank_object, blood_group__iexact="O+").blood_type()
            context['blood_donation_o_neg'] = Donation.objects.filter(
                bank=bank_object, blood_group__iexact="O-").blood_type()
            context['blood_donation_request_a_pos'] = DonationRequest.objects.filter(
                bank=bank_object, blood_group__iexact="A+").blood_type()
            context['blood_donation_request_a_neg'] = DonationRequest.objects.filter(
                bank=bank_object, blood_group__iexact="A-").blood_type()
            context['blood_donation_request_b_pos'] = DonationRequest.objects.filter(
                bank=bank_object, blood_group__iexact="B+").blood_type()
            context['blood_donation_request_b_neg'] = DonationRequest.objects.filter(
                bank=bank_object, blood_group__iexact="B-").blood_type()
            context['blood_donation_request_ab_pos'] = DonationRequest.objects.filter(
                bank=bank_object, blood_group__iexact="AB+").blood_type()
            context['blood_donation_request_ab_neg'] = DonationRequest.objects.filter(
                bank=bank_object, blood_group__iexact="AB-").blood_type()
            context['blood_donation_request_o_pos'] = DonationRequest.objects.filter(
                bank=bank_object, blood_group__iexact="O+").blood_type()
            context['blood_donation_request_o_neg'] = DonationRequest.objects.filter(
                bank=bank_object, blood_group__iexact="O-").blood_type()
            # Organ Donation Categorywise
            context['organ_donation_heart'] = Donation.objects.filter(
                bank=bank_object, organ_name__iexact="Heart").organ_type()
            context['organ_donation_kidney'] = Donation.objects.filter(
                bank=bank_object, organ_name__iexact="Kidney").organ_type()
            context['organ_donation_pancreas'] = Donation.objects.filter(
                bank=bank_object, organ_name__iexact="Pancreas").organ_type()
            context['organ_donation_lungs'] = Donation.objects.filter(
                bank=bank_object, organ_name__iexact="Lungs").organ_type()
            context['organ_donation_liver'] = Donation.objects.filter(
                bank=bank_object, organ_name__iexact="Liver").organ_type()
            context['organ_donation_intestines'] = Donation.objects.filter(
                bank=bank_object, organ_name__iexact="Intestines").organ_type()
            # Organ Donation Request Categorywise
            context['organ_donation_request_heart'] = DonationRequest.objects.filter(
                bank=bank_object, organ_name__iexact="Heart").organ_type()
            context['organ_donation_request_kidney'] = DonationRequest.objects.filter(
                bank=bank_object, organ_name__iexact="Kidney").organ_type()
            context['organ_donation_request_pancreas'] = DonationRequest.objects.filter(
                bank=bank_object, organ_name__iexact="Pancreas").organ_type()
            context['organ_donation_request_lungs'] = DonationRequest.objects.filter(
                bank=bank_object, organ_name__iexact="Lungs").organ_type()
            context['organ_donation_request_liver'] = DonationRequest.objects.filter(
                bank=bank_object, organ_name__iexact="Liver").organ_type()
            context['organ_donation_request_intestines'] = DonationRequest.objects.filter(
                bank=bank_object, organ_name__iexact="Intestines").organ_type()
            # Tissue Donation Categorywise
            context['tissue_donation_bones'] = Donation.objects.filter(
                bank=bank_object, tissue_name__iexact="Bones'").tissue_type()
            context['tissue_donation_ligaments'] = Donation.objects.filter(
                bank=bank_object, tissue_name__iexact="Ligaments").tissue_type()
            context['tissue_donation_tendons'] = Donation.objects.filter(
                bank=bank_object, tissue_name__iexact="Tendons").tissue_type()
            context['tissue_donation_fascia'] = Donation.objects.filter(
                bank=bank_object, tissue_name__iexact="Fascia").tissue_type()
            context['tissue_donation_veins'] = Donation.objects.filter(
                bank=bank_object, tissue_name__iexact="Veins").tissue_type()
            context['tissue_donation_nerves'] = Donation.objects.filter(
                bank=bank_object, tissue_name__iexact="Nerves").tissue_type()
            context['tissue_donation_corneas'] = Donation.objects.filter(
                bank=bank_object, tissue_name__iexact="Corneas").tissue_type()
            context['tissue_donation_sclera'] = Donation.objects.filter(
                bank=bank_object, tissue_name__iexact="Sclera").tissue_type()
            context['tissue_donation_heart_valves'] = Donation.objects.filter(
                bank=bank_object, tissue_name__iexact="Heart Valves").tissue_type()
            context['tissue_donation_skin'] = Donation.objects.filter(
                bank=bank_object, tissue_name__iexact="Skin").tissue_type()
            # Tissue Donation Request Categorywise
            context['tissue_donation_request_bones'] = DonationRequest.objects.filter(
                bank=bank_object, tissue_name__iexact="Bones'").tissue_type()
            context['tissue_donation_request_ligaments'] = DonationRequest.objects.filter(
                bank=bank_object, tissue_name__iexact="Ligaments").tissue_type()
            context['tissue_donation_request_tendons'] = DonationRequest.objects.filter(
                bank=bank_object, tissue_name__iexact="Tendons").tissue_type()
            context['tissue_donation_request_fascia'] = DonationRequest.objects.filter(
                bank=bank_object, tissue_name__iexact="Fascia").tissue_type()
            context['tissue_donation_request_veins'] = DonationRequest.objects.filter(
                bank=bank_object, tissue_name__iexact="Veins").tissue_type()
            context['tissue_donation_request_nerves'] = DonationRequest.objects.filter(
                bank=bank_object, tissue_name__iexact="Nerves").tissue_type()
            context['tissue_donation_request_corneas'] = DonationRequest.objects.filter(
                bank=bank_object, tissue_name__iexact="Corneas").tissue_type()
            context['tissue_donation_request_sclera'] = DonationRequest.objects.filter(
                bank=bank_object, tissue_name__iexact="Sclera").tissue_type()
            context['tissue_donation_request_heart_valves'] = DonationRequest.objects.filter(
                bank=bank_object, tissue_name__iexact="Heart Valves").tissue_type()
            context['tissue_donation_request_skin'] = DonationRequest.objects.filter(
                bank=bank_object, tissue_name__iexact="Skin").tissue_type()
        # Report Data Ends
        return context

    def user_passes_test(self, request):
        if self.request.user.is_superuser:
            return True
        else:
            qs = DonationBank.objects.filter(
                bank_member__user=request.user, slug=self.request.user.user_bank_member.bank.slug)
            if qs.exists() and self.request.user.profile.account_type == 1:
                return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(BankChartFilterTemplateView, self).dispatch(request, *args, **kwargs)


@method_decorator(decorators, name='dispatch')
@method_decorator(can_manage_bank_required, name='dispatch')
class AdminBankReportTemplateView(TemplateView):
    template_name = "pages/reports/admin/bank/index.html"

    def get_context_data(self, **kwargs):
        context = super(AdminBankReportTemplateView,
                        self).get_context_data(**kwargs)
        context['page_title'] = "Bank Reports"
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        # Starts Bank Object
        # bank_object = None
        # slug = self.kwargs.get('slug')
        # if self.request.user.is_superuser:
        #     qs = DonationBank.objects.filter(slug=slug)
        #     if qs.exists():
        #         bank_object = qs.first()
        # else:
        #     qs = DonationBank.objects.filter(
        #         bank_member__user=self.request.user)
        #     if qs.exists():
        #         bank_object = qs.first()
        # context['object'] = bank_object
        # Ends Bank Object
        # Report Data Starts
        context['total_donation'] = Donation.objects.filter()
        context['total_donation_request'] = DonationRequest.objects.filter()
        context['total_donation_pending'] = Donation.objects.filter().is_pending()
        context['total_donation_request_pending'] = DonationRequest.objects.filter().is_pending()
        context['total_donation_successful'] = Donation.objects.filter().is_done()
        context['total_donation_request_successful'] = DonationRequest.objects.filter().is_done()
        context['total_donation_expired'] = Donation.objects.filter().is_expired_pending()
        context['total_campaign'] = Campaign.objects.filter()
        context['total_member'] = BankMember.objects.filter()
        context['donation_a_pos'] = Donation.objects.filter(blood_group__iexact="A+")
        context['donation_a_neg'] = Donation.objects.filter(blood_group__iexact="A-")
        context['donation_b_pos'] = Donation.objects.filter(blood_group__iexact="B+")
        context['donation_b_neg'] = Donation.objects.filter(blood_group__iexact="B-")
        context['donation_ab_pos'] = Donation.objects.filter(blood_group__iexact="AB+")
        context['donation_ab_neg'] = Donation.objects.filter(blood_group__iexact="AB-")
        context['donation_o_pos'] = Donation.objects.filter(blood_group__iexact="O+")
        context['donation_o_neg'] = Donation.objects.filter(blood_group__iexact="O-")
        context['donation_request_a_pos'] = DonationRequest.objects.filter(blood_group__iexact="A+")
        context['donation_request_a_neg'] = DonationRequest.objects.filter(blood_group__iexact="A-")
        context['donation_request_b_pos'] = DonationRequest.objects.filter(blood_group__iexact="B+")
        context['donation_request_b_neg'] = DonationRequest.objects.filter(blood_group__iexact="B-")
        context['donation_request_ab_pos'] = DonationRequest.objects.filter(blood_group__iexact="AB+")
        context['donation_request_ab_neg'] = DonationRequest.objects.filter(blood_group__iexact="AB-")
        context['donation_request_o_pos'] = DonationRequest.objects.filter(blood_group__iexact="O+")
        context['donation_request_o_neg'] = DonationRequest.objects.filter(blood_group__iexact="O-")
        context['donation_blood'] = Donation.objects.filter().blood_type()
        context['donation_organ'] = Donation.objects.filter().organ_type()
        context['donation_tissue'] = Donation.objects.filter().tissue_type()
        context['donation_request_blood'] = DonationRequest.objects.filter().blood_type()
        context['donation_request_organ'] = DonationRequest.objects.filter().organ_type()
        context['donation_request_tissue'] = DonationRequest.objects.filter().tissue_type()
        context['blood_donation_a_pos'] = Donation.objects.filter(blood_group__iexact="A+").blood_type()
        context['blood_donation_a_neg'] = Donation.objects.filter(blood_group__iexact="A-").blood_type()
        context['blood_donation_b_pos'] = Donation.objects.filter(blood_group__iexact="B+").blood_type()
        context['blood_donation_b_neg'] = Donation.objects.filter(blood_group__iexact="B-").blood_type()
        context['blood_donation_ab_pos'] = Donation.objects.filter(blood_group__iexact="AB+").blood_type()
        context['blood_donation_ab_neg'] = Donation.objects.filter(blood_group__iexact="AB-").blood_type()
        context['blood_donation_o_pos'] = Donation.objects.filter(blood_group__iexact="O+").blood_type()
        context['blood_donation_o_neg'] = Donation.objects.filter(blood_group__iexact="O-").blood_type()
        context['blood_donation_request_a_pos'] = DonationRequest.objects.filter(blood_group__iexact="A+").blood_type()
        context['blood_donation_request_a_neg'] = DonationRequest.objects.filter(blood_group__iexact="A-").blood_type()
        context['blood_donation_request_b_pos'] = DonationRequest.objects.filter(blood_group__iexact="B+").blood_type()
        context['blood_donation_request_b_neg'] = DonationRequest.objects.filter(blood_group__iexact="B-").blood_type()
        context['blood_donation_request_ab_pos'] = DonationRequest.objects.filter(blood_group__iexact="AB+").blood_type()
        context['blood_donation_request_ab_neg'] = DonationRequest.objects.filter(blood_group__iexact="AB-").blood_type()
        context['blood_donation_request_o_pos'] = DonationRequest.objects.filter(blood_group__iexact="O+").blood_type()
        context['blood_donation_request_o_neg'] = DonationRequest.objects.filter(blood_group__iexact="O-").blood_type()
        # Organ Donation Categorywise
        context['organ_donation_heart'] = Donation.objects.filter(organ_name__iexact="Heart").organ_type()
        context['organ_donation_kidney'] = Donation.objects.filter(organ_name__iexact="Kidney").organ_type()
        context['organ_donation_pancreas'] = Donation.objects.filter(organ_name__iexact="Pancreas").organ_type()
        context['organ_donation_lungs'] = Donation.objects.filter(organ_name__iexact="Lungs").organ_type()
        context['organ_donation_liver'] = Donation.objects.filter(organ_name__iexact="Liver").organ_type()
        context['organ_donation_intestines'] = Donation.objects.filter(organ_name__iexact="Intestines").organ_type()
        # Organ Donation Request Categorywise
        context['organ_donation_request_heart'] = DonationRequest.objects.filter(organ_name__iexact="Heart").organ_type()
        context['organ_donation_request_kidney'] = DonationRequest.objects.filter(organ_name__iexact="Kidney").organ_type()
        context['organ_donation_request_pancreas'] = DonationRequest.objects.filter(organ_name__iexact="Pancreas").organ_type()
        context['organ_donation_request_lungs'] = DonationRequest.objects.filter(organ_name__iexact="Lungs").organ_type()
        context['organ_donation_request_liver'] = DonationRequest.objects.filter(organ_name__iexact="Liver").organ_type()
        context['organ_donation_request_intestines'] = DonationRequest.objects.filter(organ_name__iexact="Intestines").organ_type()
        # Tissue Donation Categorywise
        context['tissue_donation_bones'] = Donation.objects.filter(tissue_name__iexact="Bones'").tissue_type()
        context['tissue_donation_ligaments'] = Donation.objects.filter(tissue_name__iexact="Ligaments").tissue_type()
        context['tissue_donation_tendons'] = Donation.objects.filter(tissue_name__iexact="Tendons").tissue_type()
        context['tissue_donation_fascia'] = Donation.objects.filter(tissue_name__iexact="Fascia").tissue_type()
        context['tissue_donation_veins'] = Donation.objects.filter(tissue_name__iexact="Veins").tissue_type()
        context['tissue_donation_nerves'] = Donation.objects.filter(tissue_name__iexact="Nerves").tissue_type()
        context['tissue_donation_corneas'] = Donation.objects.filter(tissue_name__iexact="Corneas").tissue_type()
        context['tissue_donation_sclera'] = Donation.objects.filter(tissue_name__iexact="Sclera").tissue_type()
        context['tissue_donation_heart_valves'] = Donation.objects.filter(tissue_name__iexact="Heart Valves").tissue_type()
        context['tissue_donation_skin'] = Donation.objects.filter(tissue_name__iexact="Skin").tissue_type()
        # Tissue Donation Request Categorywise
        context['tissue_donation_request_bones'] = DonationRequest.objects.filter(tissue_name__iexact="Bones'").tissue_type()
        context['tissue_donation_request_ligaments'] = DonationRequest.objects.filter(tissue_name__iexact="Ligaments").tissue_type()
        context['tissue_donation_request_tendons'] = DonationRequest.objects.filter(tissue_name__iexact="Tendons").tissue_type()
        context['tissue_donation_request_fascia'] = DonationRequest.objects.filter(tissue_name__iexact="Fascia").tissue_type()
        context['tissue_donation_request_veins'] = DonationRequest.objects.filter(tissue_name__iexact="Veins").tissue_type()
        context['tissue_donation_request_nerves'] = DonationRequest.objects.filter(tissue_name__iexact="Nerves").tissue_type()
        context['tissue_donation_request_corneas'] = DonationRequest.objects.filter(tissue_name__iexact="Corneas").tissue_type()
        context['tissue_donation_request_sclera'] = DonationRequest.objects.filter(tissue_name__iexact="Sclera").tissue_type()
        context['tissue_donation_request_heart_valves'] = DonationRequest.objects.filter(tissue_name__iexact="Heart Valves").tissue_type()
        context['tissue_donation_request_skin'] = DonationRequest.objects.filter(tissue_name__iexact="Skin").tissue_type()
        # Report Data Ends
        return context

    def user_passes_test(self, request):
        if self.request.user.is_superuser:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(AdminBankReportTemplateView, self).dispatch(request, *args, **kwargs)


@method_decorator(decorators, name='dispatch')
@method_decorator(can_manage_bank_required, name='dispatch')
class AdminBankChartFilterTemplateView(TemplateView):
    template_name = "pages/reports/admin/bank/index.html"

    def get_context_data(self, **kwargs):
        context = super(AdminBankChartFilterTemplateView,
                        self).get_context_data(**kwargs)
        context['page_title'] = "Bank Reports"
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        # Report Data Starts
        query_context = self.request.GET.get('q')
        query_context_date_from = self.request.GET.get('date-from')
        query_context_date_to = self.request.GET.get('date-to')
        context['query'] = query_context
        context['query_date_from'] = query_context_date_from
        context['query_date_to'] = query_context_date_to
        # Query Start
        request = self.request
        method_dict = request.GET
        query = method_dict.get('q', None)
        date_from_filtered = method_dict.get('date-from', None)
        date_to_filtered = method_dict.get('date-to', None)
        if not date_from_filtered == "" and date_to_filtered == "":
            date_to_filtered = datetime.datetime.now()
        if date_from_filtered == "" and not date_to_filtered == "":
            date_from_filtered = datetime.datetime.now()
        if query is not None and not date_from_filtered == "" and not date_to_filtered == "":
            # print("QUERY With DATE!!!")
            context['total_donation'] = Donation.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter()
            context['total_donation_request'] = DonationRequest.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter()
            context['total_donation_pending'] = Donation.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter().is_pending()
            context['total_donation_request_pending'] = DonationRequest.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter().is_pending()
            context['total_donation_successful'] = Donation.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter().is_done()
            context['total_donation_request_successful'] = DonationRequest.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter().is_done()
            context['total_donation_expired'] = Donation.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter().is_expired_pending()
            context['total_campaign'] = Campaign.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter()
            context['total_member'] = BankMember.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter()
            context['donation_a_pos'] = Donation.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="A+")
            context['donation_a_neg'] = Donation.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="A-")
            context['donation_b_pos'] = Donation.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="B+")
            context['donation_b_neg'] = Donation.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="B-")
            context['donation_ab_pos'] = Donation.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="AB+")
            context['donation_ab_neg'] = Donation.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="AB-")
            context['donation_o_pos'] = Donation.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="O+")
            context['donation_o_neg'] = Donation.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="O-")
            context['donation_request_a_pos'] = DonationRequest.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="A+")
            context['donation_request_a_neg'] = DonationRequest.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="A-")
            context['donation_request_b_pos'] = DonationRequest.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="B+")
            context['donation_request_b_neg'] = DonationRequest.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="B-")
            context['donation_request_ab_pos'] = DonationRequest.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="AB+")
            context['donation_request_ab_neg'] = DonationRequest.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="AB-")
            context['donation_request_o_pos'] = DonationRequest.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="O+")
            context['donation_request_o_neg'] = DonationRequest.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="O-")
            context['donation_blood'] = Donation.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter().blood_type()
            context['donation_organ'] = Donation.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter().organ_type()
            context['donation_tissue'] = Donation.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter().tissue_type()
            context['donation_request_blood'] = DonationRequest.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter().blood_type()
            context['donation_request_organ'] = DonationRequest.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter().organ_type()
            context['donation_request_tissue'] = DonationRequest.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter().tissue_type()
            context['blood_donation_a_pos'] = Donation.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="A+").blood_type()
            context['blood_donation_a_neg'] = Donation.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="A-").blood_type()
            context['blood_donation_b_pos'] = Donation.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="B+").blood_type()
            context['blood_donation_b_neg'] = Donation.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="B-").blood_type()
            context['blood_donation_ab_pos'] = Donation.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="AB+").blood_type()
            context['blood_donation_ab_neg'] = Donation.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="AB-").blood_type()
            context['blood_donation_o_pos'] = Donation.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="O+").blood_type()
            context['blood_donation_o_neg'] = Donation.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="O-").blood_type()
            context['blood_donation_request_a_pos'] = DonationRequest.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="A+").blood_type()
            context['blood_donation_request_a_neg'] = DonationRequest.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="A-").blood_type()
            context['blood_donation_request_b_pos'] = DonationRequest.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="B+").blood_type()
            context['blood_donation_request_b_neg'] = DonationRequest.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="B-").blood_type()
            context['blood_donation_request_ab_pos'] = DonationRequest.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="AB+").blood_type()
            context['blood_donation_request_ab_neg'] = DonationRequest.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="AB-").blood_type()
            context['blood_donation_request_o_pos'] = DonationRequest.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="O+").blood_type()
            context['blood_donation_request_o_neg'] = DonationRequest.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="O-").blood_type()
            # Organ Donation Categorywise
            context['organ_donation_heart'] = Donation.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(organ_name__iexact="Heart").organ_type()
            context['organ_donation_kidney'] = Donation.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(organ_name__iexact="Kidney").organ_type()
            context['organ_donation_pancreas'] = Donation.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(organ_name__iexact="Pancreas").organ_type()
            context['organ_donation_lungs'] = Donation.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(organ_name__iexact="Lungs").organ_type()
            context['organ_donation_liver'] = Donation.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(organ_name__iexact="Liver").organ_type()
            context['organ_donation_intestines'] = Donation.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(organ_name__iexact="Intestines").organ_type()
            # Organ Donation Request Categorywise
            context['organ_donation_request_heart'] = DonationRequest.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(organ_name__iexact="Heart").organ_type()
            context['organ_donation_request_kidney'] = DonationRequest.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(organ_name__iexact="Kidney").organ_type()
            context['organ_donation_request_pancreas'] = DonationRequest.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(organ_name__iexact="Pancreas").organ_type()
            context['organ_donation_request_lungs'] = DonationRequest.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(organ_name__iexact="Lungs").organ_type()
            context['organ_donation_request_liver'] = DonationRequest.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(organ_name__iexact="Liver").organ_type()
            context['organ_donation_request_intestines'] = DonationRequest.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(organ_name__iexact="Intestines").organ_type()
            # Tissue Donation Categorywise
            context['tissue_donation_bones'] = Donation.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(tissue_name__iexact="Bones'").tissue_type()
            context['tissue_donation_ligaments'] = Donation.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(tissue_name__iexact="Ligaments").tissue_type()
            context['tissue_donation_tendons'] = Donation.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(tissue_name__iexact="Tendons").tissue_type()
            context['tissue_donation_fascia'] = Donation.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(tissue_name__iexact="Fascia").tissue_type()
            context['tissue_donation_veins'] = Donation.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(tissue_name__iexact="Veins").tissue_type()
            context['tissue_donation_nerves'] = Donation.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(tissue_name__iexact="Nerves").tissue_type()
            context['tissue_donation_corneas'] = Donation.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(tissue_name__iexact="Corneas").tissue_type()
            context['tissue_donation_sclera'] = Donation.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(tissue_name__iexact="Sclera").tissue_type()
            context['tissue_donation_heart_valves'] = Donation.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(tissue_name__iexact="Heart Valves").tissue_type()
            context['tissue_donation_skin'] = Donation.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(tissue_name__iexact="Skin").tissue_type()
            # Tissue Donation Request Categorywise
            context['tissue_donation_request_bones'] = DonationRequest.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(tissue_name__iexact="Bones'").tissue_type()
            context['tissue_donation_request_ligaments'] = DonationRequest.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(tissue_name__iexact="Ligaments").tissue_type()
            context['tissue_donation_request_tendons'] = DonationRequest.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(tissue_name__iexact="Tendons").tissue_type()
            context['tissue_donation_request_fascia'] = DonationRequest.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(tissue_name__iexact="Fascia").tissue_type()
            context['tissue_donation_request_veins'] = DonationRequest.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(tissue_name__iexact="Veins").tissue_type()
            context['tissue_donation_request_nerves'] = DonationRequest.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(tissue_name__iexact="Nerves").tissue_type()
            context['tissue_donation_request_corneas'] = DonationRequest.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(tissue_name__iexact="Corneas").tissue_type()
            context['tissue_donation_request_sclera'] = DonationRequest.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(tissue_name__iexact="Sclera").tissue_type()
            context['tissue_donation_request_heart_valves'] = DonationRequest.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(tissue_name__iexact="Heart Valves").tissue_type()
            context['tissue_donation_request_skin'] = DonationRequest.objects.search(
                query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(tissue_name__iexact="Skin").tissue_type()
        elif query is None and not date_from_filtered == "" and not date_to_filtered == "":
            # print("DATE!!!")
            context['total_donation'] = Donation.objects.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter()
            context['total_donation_request'] = DonationRequest.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter()
            context['total_donation_pending'] = Donation.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter().is_pending()
            context['total_donation_request_pending'] = DonationRequest.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter().is_pending()
            context['total_donation_successful'] = Donation.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter().is_done()
            context['total_donation_request_successful'] = DonationRequest.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter().is_done()
            context['total_donation_expired'] = Donation.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter().is_expired_pending()
            context['total_campaign'] = Campaign.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter()
            context['total_member'] = BankMember.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter()
            context['donation_a_pos'] = Donation.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="A+")
            context['donation_a_neg'] = Donation.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="A-")
            context['donation_b_pos'] = Donation.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="B+")
            context['donation_b_neg'] = Donation.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="B-")
            context['donation_ab_pos'] = Donation.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="AB+")
            context['donation_ab_neg'] = Donation.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="AB-")
            context['donation_o_pos'] = Donation.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="O+")
            context['donation_o_neg'] = Donation.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="O-")
            context['donation_request_a_pos'] = DonationRequest.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="A+")
            context['donation_request_a_neg'] = DonationRequest.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="A-")
            context['donation_request_b_pos'] = DonationRequest.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="B+")
            context['donation_request_b_neg'] = DonationRequest.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="B-")
            context['donation_request_ab_pos'] = DonationRequest.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="AB+")
            context['donation_request_ab_neg'] = DonationRequest.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="AB-")
            context['donation_request_o_pos'] = DonationRequest.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="O+")
            context['donation_request_o_neg'] = DonationRequest.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="O-")
            context['donation_blood'] = Donation.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter().blood_type()
            context['donation_organ'] = Donation.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter().organ_type()
            context['donation_tissue'] = Donation.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter().tissue_type()
            context['donation_request_blood'] = DonationRequest.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter().blood_type()
            context['donation_request_organ'] = DonationRequest.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter().organ_type()
            context['donation_request_tissue'] = DonationRequest.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter().tissue_type()
            context['blood_donation_a_pos'] = Donation.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="A+").blood_type()
            context['blood_donation_a_neg'] = Donation.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="A-").blood_type()
            context['blood_donation_b_pos'] = Donation.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="B+").blood_type()
            context['blood_donation_b_neg'] = Donation.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="B-").blood_type()
            context['blood_donation_ab_pos'] = Donation.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="AB+").blood_type()
            context['blood_donation_ab_neg'] = Donation.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="AB-").blood_type()
            context['blood_donation_o_pos'] = Donation.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="O+").blood_type()
            context['blood_donation_o_neg'] = Donation.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="O-").blood_type()
            context['blood_donation_request_a_pos'] = DonationRequest.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="A+").blood_type()
            context['blood_donation_request_a_neg'] = DonationRequest.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="A-").blood_type()
            context['blood_donation_request_b_pos'] = DonationRequest.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="B+").blood_type()
            context['blood_donation_request_b_neg'] = DonationRequest.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="B-").blood_type()
            context['blood_donation_request_ab_pos'] = DonationRequest.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="AB+").blood_type()
            context['blood_donation_request_ab_neg'] = DonationRequest.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="AB-").blood_type()
            context['blood_donation_request_o_pos'] = DonationRequest.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="O+").blood_type()
            context['blood_donation_request_o_neg'] = DonationRequest.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(blood_group__iexact="O-").blood_type()
            # Organ Donation Categorywise
            context['organ_donation_heart'] = Donation.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(organ_name__iexact="Heart").organ_type()
            context['organ_donation_kidney'] = Donation.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(organ_name__iexact="Kidney").organ_type()
            context['organ_donation_pancreas'] = Donation.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(organ_name__iexact="Pancreas").organ_type()
            context['organ_donation_lungs'] = Donation.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(organ_name__iexact="Lungs").organ_type()
            context['organ_donation_liver'] = Donation.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(organ_name__iexact="Liver").organ_type()
            context['organ_donation_intestines'] = Donation.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(organ_name__iexact="Intestines").organ_type()
            # Organ Donation Request Categorywise
            context['organ_donation_request_heart'] = DonationRequest.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(organ_name__iexact="Heart").organ_type()
            context['organ_donation_request_kidney'] = DonationRequest.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(organ_name__iexact="Kidney").organ_type()
            context['organ_donation_request_pancreas'] = DonationRequest.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(organ_name__iexact="Pancreas").organ_type()
            context['organ_donation_request_lungs'] = DonationRequest.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(organ_name__iexact="Lungs").organ_type()
            context['organ_donation_request_liver'] = DonationRequest.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(organ_name__iexact="Liver").organ_type()
            context['organ_donation_request_intestines'] = DonationRequest.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(organ_name__iexact="Intestines").organ_type()
            # Tissue Donation Categorywise
            context['tissue_donation_bones'] = Donation.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(tissue_name__iexact="Bones'").tissue_type()
            context['tissue_donation_ligaments'] = Donation.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(tissue_name__iexact="Ligaments").tissue_type()
            context['tissue_donation_tendons'] = Donation.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(tissue_name__iexact="Tendons").tissue_type()
            context['tissue_donation_fascia'] = Donation.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(tissue_name__iexact="Fascia").tissue_type()
            context['tissue_donation_veins'] = Donation.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(tissue_name__iexact="Veins").tissue_type()
            context['tissue_donation_nerves'] = Donation.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(tissue_name__iexact="Nerves").tissue_type()
            context['tissue_donation_corneas'] = Donation.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(tissue_name__iexact="Corneas").tissue_type()
            context['tissue_donation_sclera'] = Donation.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(tissue_name__iexact="Sclera").tissue_type()
            context['tissue_donation_heart_valves'] = Donation.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(tissue_name__iexact="Heart Valves").tissue_type()
            context['tissue_donation_skin'] = Donation.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(tissue_name__iexact="Skin").tissue_type()
            # Tissue Donation Request Categorywise
            context['tissue_donation_request_bones'] = DonationRequest.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(tissue_name__iexact="Bones'").tissue_type()
            context['tissue_donation_request_ligaments'] = DonationRequest.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(tissue_name__iexact="Ligaments").tissue_type()
            context['tissue_donation_request_tendons'] = DonationRequest.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(tissue_name__iexact="Tendons").tissue_type()
            context['tissue_donation_request_fascia'] = DonationRequest.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(tissue_name__iexact="Fascia").tissue_type()
            context['tissue_donation_request_veins'] = DonationRequest.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(tissue_name__iexact="Veins").tissue_type()
            context['tissue_donation_request_nerves'] = DonationRequest.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(tissue_name__iexact="Nerves").tissue_type()
            context['tissue_donation_request_corneas'] = DonationRequest.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(tissue_name__iexact="Corneas").tissue_type()
            context['tissue_donation_request_sclera'] = DonationRequest.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(tissue_name__iexact="Sclera").tissue_type()
            context['tissue_donation_request_heart_valves'] = DonationRequest.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(tissue_name__iexact="Heart Valves").tissue_type()
            context['tissue_donation_request_skin'] = DonationRequest.filter(
                created_at__range=(date_from_filtered, date_to_filtered)).filter(tissue_name__iexact="Skin").tissue_type()
        elif not query == None and date_from_filtered == "" or date_to_filtered == "":
            # print("QUERY!!!")
            context['total_donation'] = Donation.objects.search(
                query).filter()
            context['total_donation_request'] = DonationRequest.objects.search(
                query).filter()
            context['total_donation_pending'] = Donation.objects.search(
                query).filter().is_pending()
            context['total_donation_request_pending'] = DonationRequest.objects.search(
                query).filter().is_pending()
            context['total_donation_successful'] = Donation.objects.search(
                query).filter().is_done()
            context['total_donation_request_successful'] = DonationRequest.objects.search(
                query).filter().is_done()
            context['total_donation_expired'] = Donation.objects.search(
                query).filter().is_expired_pending()
            context['total_campaign'] = Campaign.objects.search(
                query).filter()
            context['total_member'] = BankMember.objects.search(
                query).filter()
            context['donation_a_pos'] = Donation.objects.search(
                query).filter(blood_group__iexact="A+")
            context['donation_a_neg'] = Donation.objects.search(
                query).filter(blood_group__iexact="A-")
            context['donation_b_pos'] = Donation.objects.search(
                query).filter(blood_group__iexact="B+")
            context['donation_b_neg'] = Donation.objects.search(
                query).filter(blood_group__iexact="B-")
            context['donation_ab_pos'] = Donation.objects.search(
                query).filter(blood_group__iexact="AB+")
            context['donation_ab_neg'] = Donation.objects.search(
                query).filter(blood_group__iexact="AB-")
            context['donation_o_pos'] = Donation.objects.search(
                query).filter(blood_group__iexact="O+")
            context['donation_o_neg'] = Donation.objects.search(
                query).filter(blood_group__iexact="O-")
            context['donation_request_a_pos'] = DonationRequest.objects.search(
                query).filter(blood_group__iexact="A+")
            context['donation_request_a_neg'] = DonationRequest.objects.search(
                query).filter(blood_group__iexact="A-")
            context['donation_request_b_pos'] = DonationRequest.objects.search(
                query).filter(blood_group__iexact="B+")
            context['donation_request_b_neg'] = DonationRequest.objects.search(
                query).filter(blood_group__iexact="B-")
            context['donation_request_ab_pos'] = DonationRequest.objects.search(
                query).filter(blood_group__iexact="AB+")
            context['donation_request_ab_neg'] = DonationRequest.objects.search(
                query).filter(blood_group__iexact="AB-")
            context['donation_request_o_pos'] = DonationRequest.objects.search(
                query).filter(blood_group__iexact="O+")
            context['donation_request_o_neg'] = DonationRequest.objects.search(
                query).filter(blood_group__iexact="O-")
            context['donation_blood'] = Donation.objects.search(
                query).filter().blood_type()
            context['donation_organ'] = Donation.objects.search(
                query).filter().organ_type()
            context['donation_tissue'] = Donation.objects.search(
                query).filter().tissue_type()
            context['donation_request_blood'] = DonationRequest.objects.search(
                query).filter().blood_type()
            context['donation_request_organ'] = DonationRequest.objects.search(
                query).filter().organ_type()
            context['donation_request_tissue'] = DonationRequest.objects.search(
                query).filter().tissue_type()
            context['blood_donation_a_pos'] = Donation.objects.search(
                query).filter(blood_group__iexact="A+").blood_type()
            context['blood_donation_a_neg'] = Donation.objects.search(
                query).filter(blood_group__iexact="A-").blood_type()
            context['blood_donation_b_pos'] = Donation.objects.search(
                query).filter(blood_group__iexact="B+").blood_type()
            context['blood_donation_b_neg'] = Donation.objects.search(
                query).filter(blood_group__iexact="B-").blood_type()
            context['blood_donation_ab_pos'] = Donation.objects.search(
                query).filter(blood_group__iexact="AB+").blood_type()
            context['blood_donation_ab_neg'] = Donation.objects.search(
                query).filter(blood_group__iexact="AB-").blood_type()
            context['blood_donation_o_pos'] = Donation.objects.search(
                query).filter(blood_group__iexact="O+").blood_type()
            context['blood_donation_o_neg'] = Donation.objects.search(
                query).filter(blood_group__iexact="O-").blood_type()
            context['blood_donation_request_a_pos'] = DonationRequest.objects.search(
                query).filter(blood_group__iexact="A+").blood_type()
            context['blood_donation_request_a_neg'] = DonationRequest.objects.search(
                query).filter(blood_group__iexact="A-").blood_type()
            context['blood_donation_request_b_pos'] = DonationRequest.objects.search(
                query).filter(blood_group__iexact="B+").blood_type()
            context['blood_donation_request_b_neg'] = DonationRequest.objects.search(
                query).filter(blood_group__iexact="B-").blood_type()
            context['blood_donation_request_ab_pos'] = DonationRequest.objects.search(
                query).filter(blood_group__iexact="AB+").blood_type()
            context['blood_donation_request_ab_neg'] = DonationRequest.objects.search(
                query).filter(blood_group__iexact="AB-").blood_type()
            context['blood_donation_request_o_pos'] = DonationRequest.objects.search(
                query).filter(blood_group__iexact="O+").blood_type()
            context['blood_donation_request_o_neg'] = DonationRequest.objects.search(
                query).filter(blood_group__iexact="O-").blood_type()
            # Organ Donation Categorywise
            context['organ_donation_heart'] = Donation.objects.search(
                query).filter(organ_name__iexact="Heart").organ_type()
            context['organ_donation_kidney'] = Donation.objects.search(
                query).filter(organ_name__iexact="Kidney").organ_type()
            context['organ_donation_pancreas'] = Donation.objects.search(
                query).filter(organ_name__iexact="Pancreas").organ_type()
            context['organ_donation_lungs'] = Donation.objects.search(
                query).filter(organ_name__iexact="Lungs").organ_type()
            context['organ_donation_liver'] = Donation.objects.search(
                query).filter(organ_name__iexact="Liver").organ_type()
            context['organ_donation_intestines'] = Donation.objects.search(
                query).filter(organ_name__iexact="Intestines").organ_type()
            # Organ Donation Request Categorywise
            context['organ_donation_request_heart'] = DonationRequest.objects.search(
                query).filter(organ_name__iexact="Heart").organ_type()
            context['organ_donation_request_kidney'] = DonationRequest.objects.search(
                query).filter(organ_name__iexact="Kidney").organ_type()
            context['organ_donation_request_pancreas'] = DonationRequest.objects.search(
                query).filter(organ_name__iexact="Pancreas").organ_type()
            context['organ_donation_request_lungs'] = DonationRequest.objects.search(
                query).filter(organ_name__iexact="Lungs").organ_type()
            context['organ_donation_request_liver'] = DonationRequest.objects.search(
                query).filter(organ_name__iexact="Liver").organ_type()
            context['organ_donation_request_intestines'] = DonationRequest.objects.search(
                query).filter(organ_name__iexact="Intestines").organ_type()
            # Tissue Donation Categorywise
            context['tissue_donation_bones'] = Donation.objects.search(
                query).filter(tissue_name__iexact="Bones'").tissue_type()
            context['tissue_donation_ligaments'] = Donation.objects.search(
                query).filter(tissue_name__iexact="Ligaments").tissue_type()
            context['tissue_donation_tendons'] = Donation.objects.search(
                query).filter(tissue_name__iexact="Tendons").tissue_type()
            context['tissue_donation_fascia'] = Donation.objects.search(
                query).filter(tissue_name__iexact="Fascia").tissue_type()
            context['tissue_donation_veins'] = Donation.objects.search(
                query).filter(tissue_name__iexact="Veins").tissue_type()
            context['tissue_donation_nerves'] = Donation.objects.search(
                query).filter(tissue_name__iexact="Nerves").tissue_type()
            context['tissue_donation_corneas'] = Donation.objects.search(
                query).filter(tissue_name__iexact="Corneas").tissue_type()
            context['tissue_donation_sclera'] = Donation.objects.search(
                query).filter(tissue_name__iexact="Sclera").tissue_type()
            context['tissue_donation_heart_valves'] = Donation.objects.search(
                query).filter(tissue_name__iexact="Heart Valves").tissue_type()
            context['tissue_donation_skin'] = Donation.objects.search(
                query).filter(tissue_name__iexact="Skin").tissue_type()
            # Tissue Donation Request Categorywise
            context['tissue_donation_request_bones'] = DonationRequest.objects.search(
                query).filter(tissue_name__iexact="Bones'").tissue_type()
            context['tissue_donation_request_ligaments'] = DonationRequest.objects.search(
                query).filter(tissue_name__iexact="Ligaments").tissue_type()
            context['tissue_donation_request_tendons'] = DonationRequest.objects.search(
                query).filter(tissue_name__iexact="Tendons").tissue_type()
            context['tissue_donation_request_fascia'] = DonationRequest.objects.search(
                query).filter(tissue_name__iexact="Fascia").tissue_type()
            context['tissue_donation_request_veins'] = DonationRequest.objects.search(
                query).filter(tissue_name__iexact="Veins").tissue_type()
            context['tissue_donation_request_nerves'] = DonationRequest.objects.search(
                query).filter(tissue_name__iexact="Nerves").tissue_type()
            context['tissue_donation_request_corneas'] = DonationRequest.objects.search(
                query).filter(tissue_name__iexact="Corneas").tissue_type()
            context['tissue_donation_request_sclera'] = DonationRequest.objects.search(
                query).filter(tissue_name__iexact="Sclera").tissue_type()
            context['tissue_donation_request_heart_valves'] = DonationRequest.objects.search(
                query).filter(tissue_name__iexact="Heart Valves").tissue_type()
            context['tissue_donation_request_skin'] = DonationRequest.objects.search(
                query).filter(tissue_name__iexact="Skin").tissue_type()
        else:
            # print("NONE!!!")
            context['total_donation'] = Donation.objects.filter()
            context['total_donation_request'] = DonationRequest.objects.filter()
            context['total_donation_pending'] = Donation.objects.filter().is_pending()
            context['total_donation_request_pending'] = DonationRequest.objects.filter().is_pending()
            context['total_donation_successful'] = Donation.objects.filter().is_done()
            context['total_donation_request_successful'] = DonationRequest.objects.filter().is_done()
            context['total_donation_expired'] = Donation.objects.filter().is_expired_pending()
            context['total_campaign'] = Campaign.objects.filter()
            context['total_member'] = BankMember.objects.filter()
            context['donation_a_pos'] = Donation.objects.filter(blood_group__iexact="A+")
            context['donation_a_neg'] = Donation.objects.filter(blood_group__iexact="A-")
            context['donation_b_pos'] = Donation.objects.filter(blood_group__iexact="B+")
            context['donation_b_neg'] = Donation.objects.filter(blood_group__iexact="B-")
            context['donation_ab_pos'] = Donation.objects.filter(blood_group__iexact="AB+")
            context['donation_ab_neg'] = Donation.objects.filter(blood_group__iexact="AB-")
            context['donation_o_pos'] = Donation.objects.filter(blood_group__iexact="O+")
            context['donation_o_neg'] = Donation.objects.filter(blood_group__iexact="O-")
            context['donation_request_a_pos'] = DonationRequest.objects.filter(blood_group__iexact="A+")
            context['donation_request_a_neg'] = DonationRequest.objects.filter(blood_group__iexact="A-")
            context['donation_request_b_pos'] = DonationRequest.objects.filter(blood_group__iexact="B+")
            context['donation_request_b_neg'] = DonationRequest.objects.filter(blood_group__iexact="B-")
            context['donation_request_ab_pos'] = DonationRequest.objects.filter(blood_group__iexact="AB+")
            context['donation_request_ab_neg'] = DonationRequest.objects.filter(blood_group__iexact="AB-")
            context['donation_request_o_pos'] = DonationRequest.objects.filter(blood_group__iexact="O+")
            context['donation_request_o_neg'] = DonationRequest.objects.filter(blood_group__iexact="O-")
            context['donation_blood'] = Donation.objects.filter().blood_type()
            context['donation_organ'] = Donation.objects.filter().organ_type()
            context['donation_tissue'] = Donation.objects.filter().tissue_type()
            context['donation_request_blood'] = DonationRequest.objects.filter().blood_type()
            context['donation_request_organ'] = DonationRequest.objects.filter().organ_type()
            context['donation_request_tissue'] = DonationRequest.objects.filter().tissue_type()
            context['blood_donation_a_pos'] = Donation.objects.filter(blood_group__iexact="A+").blood_type()
            context['blood_donation_a_neg'] = Donation.objects.filter(blood_group__iexact="A-").blood_type()
            context['blood_donation_b_pos'] = Donation.objects.filter(blood_group__iexact="B+").blood_type()
            context['blood_donation_b_neg'] = Donation.objects.filter(blood_group__iexact="B-").blood_type()
            context['blood_donation_ab_pos'] = Donation.objects.filter(blood_group__iexact="AB+").blood_type()
            context['blood_donation_ab_neg'] = Donation.objects.filter(blood_group__iexact="AB-").blood_type()
            context['blood_donation_o_pos'] = Donation.objects.filter(blood_group__iexact="O+").blood_type()
            context['blood_donation_o_neg'] = Donation.objects.filter(blood_group__iexact="O-").blood_type()
            context['blood_donation_request_a_pos'] = DonationRequest.objects.filter(blood_group__iexact="A+").blood_type()
            context['blood_donation_request_a_neg'] = DonationRequest.objects.filter(blood_group__iexact="A-").blood_type()
            context['blood_donation_request_b_pos'] = DonationRequest.objects.filter(blood_group__iexact="B+").blood_type()
            context['blood_donation_request_b_neg'] = DonationRequest.objects.filter(blood_group__iexact="B-").blood_type()
            context['blood_donation_request_ab_pos'] = DonationRequest.objects.filter(blood_group__iexact="AB+").blood_type()
            context['blood_donation_request_ab_neg'] = DonationRequest.objects.filter(blood_group__iexact="AB-").blood_type()
            context['blood_donation_request_o_pos'] = DonationRequest.objects.filter(blood_group__iexact="O+").blood_type()
            context['blood_donation_request_o_neg'] = DonationRequest.objects.filter(blood_group__iexact="O-").blood_type()
            # Organ Donation Categorywise
            context['organ_donation_heart'] = Donation.objects.filter(organ_name__iexact="Heart").organ_type()
            context['organ_donation_kidney'] = Donation.objects.filter(organ_name__iexact="Kidney").organ_type()
            context['organ_donation_pancreas'] = Donation.objects.filter(organ_name__iexact="Pancreas").organ_type()
            context['organ_donation_lungs'] = Donation.objects.filter(organ_name__iexact="Lungs").organ_type()
            context['organ_donation_liver'] = Donation.objects.filter(organ_name__iexact="Liver").organ_type()
            context['organ_donation_intestines'] = Donation.objects.filter(organ_name__iexact="Intestines").organ_type()
            # Organ Donation Request Categorywise
            context['organ_donation_request_heart'] = DonationRequest.objects.filter(organ_name__iexact="Heart").organ_type()
            context['organ_donation_request_kidney'] = DonationRequest.objects.filter(organ_name__iexact="Kidney").organ_type()
            context['organ_donation_request_pancreas'] = DonationRequest.objects.filter(organ_name__iexact="Pancreas").organ_type()
            context['organ_donation_request_lungs'] = DonationRequest.objects.filter(organ_name__iexact="Lungs").organ_type()
            context['organ_donation_request_liver'] = DonationRequest.objects.filter(organ_name__iexact="Liver").organ_type()
            context['organ_donation_request_intestines'] = DonationRequest.objects.filter(organ_name__iexact="Intestines").organ_type()
            # Tissue Donation Categorywise
            context['tissue_donation_bones'] = Donation.objects.filter(tissue_name__iexact="Bones'").tissue_type()
            context['tissue_donation_ligaments'] = Donation.objects.filter(tissue_name__iexact="Ligaments").tissue_type()
            context['tissue_donation_tendons'] = Donation.objects.filter(tissue_name__iexact="Tendons").tissue_type()
            context['tissue_donation_fascia'] = Donation.objects.filter(tissue_name__iexact="Fascia").tissue_type()
            context['tissue_donation_veins'] = Donation.objects.filter(tissue_name__iexact="Veins").tissue_type()
            context['tissue_donation_nerves'] = Donation.objects.filter(tissue_name__iexact="Nerves").tissue_type()
            context['tissue_donation_corneas'] = Donation.objects.filter(tissue_name__iexact="Corneas").tissue_type()
            context['tissue_donation_sclera'] = Donation.objects.filter(tissue_name__iexact="Sclera").tissue_type()
            context['tissue_donation_heart_valves'] = Donation.objects.filter(tissue_name__iexact="Heart Valves").tissue_type()
            context['tissue_donation_skin'] = Donation.objects.filter(tissue_name__iexact="Skin").tissue_type()
            # Tissue Donation Request Categorywise
            context['tissue_donation_request_bones'] = DonationRequest.objects.filter(tissue_name__iexact="Bones'").tissue_type()
            context['tissue_donation_request_ligaments'] = DonationRequest.objects.filter(tissue_name__iexact="Ligaments").tissue_type()
            context['tissue_donation_request_tendons'] = DonationRequest.objects.filter(tissue_name__iexact="Tendons").tissue_type()
            context['tissue_donation_request_fascia'] = DonationRequest.objects.filter(tissue_name__iexact="Fascia").tissue_type()
            context['tissue_donation_request_veins'] = DonationRequest.objects.filter(tissue_name__iexact="Veins").tissue_type()
            context['tissue_donation_request_nerves'] = DonationRequest.objects.filter(tissue_name__iexact="Nerves").tissue_type()
            context['tissue_donation_request_corneas'] = DonationRequest.objects.filter(tissue_name__iexact="Corneas").tissue_type()
            context['tissue_donation_request_sclera'] = DonationRequest.objects.filter(tissue_name__iexact="Sclera").tissue_type()
            context['tissue_donation_request_heart_valves'] = DonationRequest.objects.filter(tissue_name__iexact="Heart Valves").tissue_type()
            context['tissue_donation_request_skin'] = DonationRequest.objects.filter(tissue_name__iexact="Skin").tissue_type()
        # Report Data Ends
        return context

    def user_passes_test(self, request):
        if self.request.user.is_superuser:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(AdminBankChartFilterTemplateView, self).dispatch(request, *args, **kwargs)
