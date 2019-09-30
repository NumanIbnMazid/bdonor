from django import template
from utils.models import SitePreference, Notification
from accounts.models import UserProfile
from donationBank.models import BankMember, DonationBank
from checkout.models import Checkout
from chat.models import ChatMessage, Thread
from django.db.models import Q
import datetime
from dateutil.relativedelta import relativedelta
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.contrib.auth.models import User


register = template.Library()


@register.simple_tag(takes_context=True)
def get_superuser(context):
    super_user_qs = User.objects.filter(is_superuser=True)
    superuser = None
    if super_user_qs.exists():
        superuser = super_user_qs.first()
    return superuser

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

    
# @register.simple_tag(takes_context=True)
# def get_is_premium_user(context):
#     request = context['request']
#     user = request.user
#     if request.user.is_authenticated:
#         profile_qs = UserProfile.objects.filter(user=user)
#         if profile_qs.exists():
#             checkout_qs = Checkout.objects.filter(user=user)
#             if checkout_qs.exists():
#                 last_checkout = checkout_qs.latest('created_at')
#                 expiration_date = (last_checkout.created_at + relativedelta(months=last_checkout.plan.expiration_cycle))
#                 if not datetime.datetime.now() > expiration_date:
#                     if profile_qs.first().account_type == 0:
#                         profile_qs.update(account_type=1)
#                     return True
#                 else:
#                     profile_qs.update(account_type=0)
#                     # Sending Email
#                     mail_msg = f"Hello {request.user.profile.get_username()} ! <br> Your subscription of BDonor has been expired. Please renew your subscription. <br> Have a good day. <br>Thanks for being with us."
#                     mail_subject = 'BDonor Subscription'
#                     mail_from = 'admin@bdonor.com'
#                     mail_text = 'Please do not Reply'
#                     subject = mail_subject
#                     from_email = mail_from
#                     to = [request.user.email]
#                     text_content = mail_text
#                     html_content = mail_msg
#                     msg = EmailMultiAlternatives(
#                         subject, text_content, from_email, [to])
#                     msg.attach_alternative(html_content, "text/html")
#                     msg.send()
#                     messages.add_message(request, messages.WARNING,
#                                         "Your subscription of BDonor has been expired. Please renew your subscription.")
#     return False


@register.simple_tag(takes_context=True)
def get_is_premium_user(context):
    request = context['request']
    user = request.user
    if request.user.is_authenticated:
        profile_qs = UserProfile.objects.filter(user=user)
        if profile_qs.exists():
            bank_member_qs = BankMember.objects.filter(user=request.user)
            if bank_member_qs.exists():
                membership = bank_member_qs.first()
                if membership.role == 0:
                    checkout_qs = Checkout.objects.filter(user=user)
                    if checkout_qs.exists():
                        last_checkout = checkout_qs.latest('created_at')
                        expiration_date = (last_checkout.created_at + relativedelta(months=last_checkout.plan.expiration_cycle))
                        if not datetime.datetime.now() > expiration_date:
                            if profile_qs.first().account_type == 0:
                                profile_qs.update(account_type=1)
                            return True
                        else:
                            profile_qs.update(account_type=0)
                            # Sending Email
                            mail_msg = f"Hello {request.user.profile.get_username()} ! <br> Your subscription of BDonor Donation Bank has been expired. Please renew your subscription. <br> Have a good day. <br>Thanks for being with us."
                            mail_subject = 'BDonor Subscription'
                            mail_from = 'admin@bdonor.com'
                            mail_text = 'Please do not Reply'
                            subject = mail_subject
                            from_email = mail_from
                            to = [request.user.email]
                            text_content = mail_text
                            html_content = mail_msg
                            msg = EmailMultiAlternatives(
                                subject, text_content, from_email, [to])
                            msg.attach_alternative(html_content, "text/html")
                            msg.send()
                            messages.add_message(request, messages.WARNING,
                                                "Your subscription of BDonor Donation Bank has been expired. Please renew your subscription.")
                if membership.role == 1:
                    bank_creator_qs = BankMember.objects.filter(
                        bank=membership.bank, role=0
                    )
                    if bank_creator_qs.exists():
                        creator = bank_creator_qs.first()
                        creator_profile_qs = UserProfile.objects.filter(
                            user=creator.user
                        )
                        if creator_profile_qs.exists():
                            checkout_qs = Checkout.objects.filter(user=creator.user)
                            if checkout_qs.exists():
                                last_checkout = checkout_qs.latest('created_at')
                                expiration_date = (
                                    last_checkout.created_at + relativedelta(months=last_checkout.plan.expiration_cycle))
                                if not datetime.datetime.now() > expiration_date:
                                    if creator_profile_qs.first().account_type == 0:
                                        creator_profile_qs.update(account_type=1)
                                    if profile_qs.first().account_type == 0:
                                        profile_qs.update(account_type=1)
                                    return True
                                else:
                                    creator_profile_qs.update(account_type=0)
                                    profile_qs.update(account_type=0)
                                    # Sending Email
                                    mail_msg = f"Hello {creator.user.profile.get_username()} ! <br> Your subscription of BDonor has been expired. Please renew your subscription. <br> Have a good day. <br>Thanks for being with us."
                                    mail_subject = 'BDonor Subscription'
                                    mail_from = 'admin@bdonor.com'
                                    mail_text = 'Please do not Reply'
                                    subject = mail_subject
                                    from_email = mail_from
                                    to = [request.user.email]
                                    text_content = mail_text
                                    html_content = mail_msg
                                    msg = EmailMultiAlternatives(
                                        subject, text_content, from_email, [to])
                                    msg.attach_alternative(html_content, "text/html")
                                    msg.send()
                                    messages.add_message(request, messages.WARNING,
                                                        "Your Donation Bank's subscription has been expired. Please ask your Donation Bank's administrator to renew subscription.")
    return False


@register.simple_tag(takes_context=True)
def get_notifications_tag(context):
    request = context['request']
    user = request.user
    if user.is_authenticated:
        notification_filter = Notification.objects.filter(
            receiver=user).order_by('-updated_at')
        return notification_filter
    return None


@register.simple_tag(takes_context=True)
def get_notifications_unread_counter_tag(context):
    request = context['request']
    user = request.user
    if user.is_authenticated:
        notification_filter = Notification.objects.filter(
            receiver=user, is_seen=False).order_by('-updated_at')
        return notification_filter.count()
    return None
