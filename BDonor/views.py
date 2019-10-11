from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from el_pagination.decorators import page_template
from chat.models import Thread
from donationBank.models import Campaign
from donations.models import Donation
from django.db.models import Q
from accounts.models import UserPermission
# Custom Decorators Starts
from accounts.decorators import (
    can_browse_required, can_donate_required, can_ask_for_a_donor_required,
    can_manage_bank_required, can_chat_required
)
# Custom Decorators Ends

decorators = [login_required, can_browse_required]


class HomeView(TemplateView):
    def get(self, request, *args, **kwargs):
        user = request.user
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        # Ends Base Template Context
        campaigns = Campaign.objects.all().bank_is_public(
        ).bank_is_verified().end_date_not_expired().dynamic_order()[:20]
        donation_requests = Donation.objects.all().requests(
        ).is_published().is_verified().is_pending().dynamic_order()[:20]
        donation_offers = Donation.objects.all().offers(
        ).is_published().is_verified().is_pending().dynamic_order()[:20]
        blood_request_awaiting = Donation.objects.all(
        ).requests().blood_type().is_published().count()
        blood_offers_awaiting = Donation.objects.all(
        ).offers().blood_type().is_published().count()
        organ_requests_awaiting = Donation.objects.all(
        ).requests().organ_type().is_published().count()
        organ_offers_awaiting = Donation.objects.all(
        ).offers().organ_type().is_published().count()
        tissue_requests_awaiting = Donation.objects.all(
        ).requests().tissue_type().is_published().count()
        tissue_offers_awaiting = Donation.objects.all(
        ).offers().tissue_type().is_published().count()
        context = {
            'base_template': base_template,
            'campaigns': campaigns,
            'donation_requests': donation_requests,
            'donation_offers': donation_offers,
            'blood_requests_awaiting': blood_request_awaiting,
            'blood_offers_awaiting': blood_offers_awaiting,
            'organ_requests_awaiting': organ_requests_awaiting,
            'organ_offers_awaiting': organ_offers_awaiting,
            'tissue_requests_awaiting': tissue_requests_awaiting,
            'tissue_offers_awaiting': tissue_offers_awaiting,
        }
        if user.is_superuser:
            return render(request, "admin-site/pages/home.html", context=context)
        return render(request, "pages/home.html", context=context)


# @method_decorator(login_required, name='dispatch')
# class ChatListTemplateView(TemplateView):
#     def get(self, request, *args, **kwargs):
#         return render(request, "chat/chat-list.html")


@login_required
@can_browse_required
@can_chat_required
@page_template('chat/snippets/list.html')
def get_chat_list_template(request,
                           template='chat/chat-list.html',
                           extra_context=None):
    chat_list = None
    qs = Thread.objects.filter(Q(first=request.user) | Q(second=request.user))
    if qs.exists():
        chat_list = qs.order_by('-updated_at')
    # Starts Base Template Context
    if request.user.is_superuser:
        base_template = 'admin-site/base.html'
    else:
        base_template = 'base.html'
    # Ends Base Template Context
    context = {
        'chat_list': chat_list,
        'base_template': base_template
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


@method_decorator(login_required, name='dispatch')
class BlockedView(TemplateView):
    def get(self, request, *args, **kwargs):
        if self.request.user.user_permissions_user.can_browse == False:
            return render(request, "exceptions/blocked.html")
        return render(request, "exceptions/error.html")



@method_decorator(login_required, name='dispatch')
class AccessDeniedView(TemplateView):
    def get(self, request, *args, **kwargs):
        u_permission = self.request.user.user_permissions_user
        if u_permission.can_browse == False or u_permission.can_donate == False or u_permission.can_ask_for_a_donor == False or u_permission.can_manage_bank == False or u_permission.can_chat == False:
            permissions = UserPermission.objects.filter(user=self.request.user)
            if permissions.exists():
                context = {
                    'permission': permissions.first(),
                }
            return render(request, "exceptions/access-denied.html", context=context)
        return render(request, "exceptions/error.html")
