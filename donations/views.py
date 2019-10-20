from django.shortcuts import render
# model imports
from .models import Donation, DonationProgress, DonationRespond
from accounts.models import UserProfile
from utils.models import Notification
# generic view imports
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
# other imports
from .forms import DonationForm, DonationRespondForm, DonationProgressForm
from utils.handlers import create_notification
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django import forms
from django.contrib import messages
from el_pagination.views import AjaxListView
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from suspicious.utils import block_suspicious_user
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.db.models import Q
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
import zeep
from zeep import Client
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
# Site.objects.get_current().domain
# import socket
# Custom Decorators Starts
from accounts.decorators import (
    can_browse_required, can_donate_required, can_ask_for_a_donor_required,
    can_manage_bank_required, can_chat_required
)
# Custom Decorators Ends

decorators = [login_required, can_browse_required]


@method_decorator(decorators, name='dispatch')
@method_decorator(can_donate_required, name='dispatch')
class OfferDonationCreateView(CreateView):
    template_name = 'donations/donation-manage.html'
    form_class = DonationForm

    # inside CreateView class
    # def render_to_response(self, context, **response_kwargs):
    #     """ Allow AJAX requests to be handled more gracefully """
    #     if self.request.is_ajax():
    #         return JsonResponse('Success',safe=False, **response_kwargs)
    #     else:
    #         return super(OfferDonationCreateView,self).render_to_response(context, **response_kwargs)

    def form_valid(self, form):
        category = 0
        type = form.instance.type
        if type == 0:
            finalized_type = "Blood"
            finalized_type_child = form.instance.blood_group
            finalized_field_name = "blood_group"
        elif type == 1:
            finalized_type = "Organ"
            finalized_type_child = form.instance.organ_name
            finalized_field_name = "organ_name"
            if form.instance.organ_name == "Heart" or form.instance.organ_name == "Liver" or form.instance.organ_name == "Pancreas" or form.instance.organ_name == "Intestines":
                form.instance.quantity = 1
        elif type == 2:
            finalized_type = "Tissue"
            finalized_type_child = form.instance.tissue_name
            finalized_field_name = "tissue_name"
        else:
            finalized_type = "Undefined"
        title = f"I want to donate {finalized_type} [{finalized_type_child}]"
        donation_qs = Donation.objects.filter(
            user=self.request.user.profile, title__iexact=title, donation_progress__progress_status=0
        )
        form.instance.title = f"I want to donate {finalized_type} [{finalized_type_child}]"
        if type == 0:
            form.instance.blood_bag = 1
        blood_group = form.instance.blood_group
        blood_bag = form.instance.blood_bag
        # print(blood_bag)
        # organ_name = form.instance.organ_name
        details = form.instance.details
        details_fake = form.cleaned_data['details_fake']
        contact = form.instance.contact
        contact2 = form.instance.contact2
        contact3 = form.instance.contact3
        contact_privacy = self.request.POST.get("contact_privacy")
        donate_type = self.request.POST.get("donate-type")
        form.instance.donate_type = donate_type
        living_organs = ["Kidney", "Lungs"]
        deceased_organs = ["Heart", "Pancreas", "Liver", "Intestines"]
        if form.instance.type == 2:
            form.instance.donate_type = 1
        elif form.instance.type == 1 and form.instance.organ_name in deceased_organs:
            form.instance.donate_type = 1
        elif form.instance.type == 1 and form.instance.organ_name in living_organs and int(form.instance.quantity) > 1:
            form.instance.donate_type = 1
        else:
            form.instance.donate_type = 0
        if donate_type == "1" or donate_type == 1:
            form.instance.is_verified = False
        # print(contact_privacy)
        form.instance.contact_privacy = contact_privacy
        contactFake = self.request.POST.get("contact_fake")
        contact2Fake = self.request.POST.get("contact2_fake")
        contact3Fake = self.request.POST.get("contact3_fake")
        preferred_date = form.instance.preferred_date
        preferred_date_from = form.instance.preferred_date_from
        preferred_date_to = form.instance.preferred_date_to

        user_profile = UserProfile.objects.filter(user=self.request.user)
        if user_profile.exists():
            profile = user_profile.first()
            if donation_qs.exists():
                donation_qs_url = donation_qs.first().get_absolute_url()
                form.add_error(
                    f'{finalized_field_name}', forms.ValidationError(
                        f"You already have a pending post similar to this. Please update that post if you need any changes. click <a href='{donation_qs_url}'>here</a> to view the post."
                    )
                )
            elif blood_group == None:
                form.add_error(
                    'blood_group', forms.ValidationError(
                        "You must select blood group."
                    )
                )
            elif type == 0 and blood_bag == None:
                form.add_error(
                    'blood_bag', forms.ValidationError(
                        "You must enter blood bag quantity."
                    )
                )
            elif donate_type == "1" and contact2 == None:
                form.add_error(
                    'contact2', forms.ValidationError(
                        "You must enter second contact number (Contact number of your family member/friend)."
                    )
                )
            elif not contact2 == None and contact == contact2:
                form.add_error(
                    'contact2', forms.ValidationError(
                        "You have entered this contact in first contact. Please enter different one."
                    )
                )
            elif not contact3 == None and contact == contact3:
                form.add_error(
                    'contact3', forms.ValidationError(
                        "You have entered this contact in first contact. Please enter different one."
                    )
                )
            elif not contact2 == None and not contact3 == None and contact2 == contact3:
                form.add_error(
                    'contact3', forms.ValidationError(
                        "You have entered this contact in second contact. Please enter different one."
                    )
                )

            # elif type == 0 and blood_bag == None:
            #     form.add_error(
            #         'blood_bag', forms.ValidationError(
            #             "You must enter required blood bag quantity."
            #         )
            #     )
            # elif type == 1 and organ_name == None:
            #     form.add_error(
            #         'organ_name', forms.ValidationError(
            #             "You must enter organ name."
            #         )
            #     )
            elif preferred_date_from == None and preferred_date_to is not None:
                form.add_error(
                    'preferred_date_from', forms.ValidationError(
                        "You must select Preferred Date From if you select Preferred Date To."
                    )
                )
            elif preferred_date_to == None and preferred_date_from is not None:
                form.add_error(
                    'preferred_date_to', forms.ValidationError(
                        "You must select Preferred Date To if you select Preferred Date From."
                    )
                )
            elif type == 1 and form.instance.organ_name == None:
                form.add_error(
                    'organ_name', forms.ValidationError(
                        "You must select organ name."
                    )
                )
            elif type == 2 and form.instance.tissue_name == None:
                form.add_error(
                    'tissue_name', forms.ValidationError(
                        "You must select tissue name."
                    )
                )
            elif type == 1 and form.instance.quantity == None:
                form.add_error(
                    'quantity', forms.ValidationError(
                        "You must enter the quantity."
                    )
                )
            else:
                # Save the form
                if contact is not None:
                    form.instance.contact = contactFake + contact
                if contact2 is not None:
                    form.instance.contact2 = contact2Fake + contact2
                if contact3 is not None:
                    form.instance.contact3 = contact3Fake + contact3
                if details_fake != "":
                    form.instance.details = details_fake
                form.instance.user = profile
                form.instance.category = category
                if form.instance.donate_type == 1:
                    form.instance.preferred_date = None
                    form.instance.preferred_date_from = None
                    form.instance.preferred_date_to = None
                messages.add_message(self.request, messages.SUCCESS,
                                     "Your donation offer has been created successfully!")
                return super().form_valid(form)
            # print(donate_type)
        return super().form_invalid(form)

    def user_passes_test(self, request):
        if not request.user.is_superuser:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(OfferDonationCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(OfferDonationCreateView, self).get_form_kwargs()
        if self.form_class:
            kwargs.update({'request': self.request})
            kwargs.update({'object': None})
        return kwargs

    def get_success_url(self):
        return reverse('donations:my_donation_offers')

    def get_context_data(self, **kwargs):
        context = super(OfferDonationCreateView,
                        self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        context['page_title'] = "Create donation offer"
        context['page_type'] = "OFFER"
        last_blood_donated_filter = DonationProgress.objects.filter(
            donation__user=self.request.user.profile, donation__category=0, donation__type=0,
            progress_status=1
        )
        can_donate_blood = True
        if last_blood_donated_filter.exists():
            if not last_blood_donated_filter.last().completion_date == None:
                day_difference = datetime.date.today(
                ) - last_blood_donated_filter.last().completion_date
                if day_difference.days < 90:
                    can_donate_blood = False
                    context['last_donated_ago'] = day_difference.days
                    context['waiting_days_remaining'] = 90 - \
                        int(day_difference.days)
                    context['last_donated_object'] = last_blood_donated_filter.last()
        context['can_donate_blood'] = can_donate_blood
        return context


@method_decorator(decorators, name='dispatch')
@method_decorator(can_donate_required, name='dispatch')
class OfferDonationUpdateView(UpdateView):
    template_name = 'donations/donation-manage.html'
    form_class = DonationForm

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        return Donation.objects.get_by_slug(slug, self.request)

    def form_valid(self, form):
        # category = 0
        self.object = self.get_object()
        type = form.instance.type
        if type == 0:
            finalized_type = "Blood"
            finalized_type_child = form.instance.blood_group
            finalized_field_name = "blood_group"
        elif type == 1:
            finalized_type = "Organ"
            finalized_type_child = form.instance.organ_name
            finalized_field_name = "organ_name"
            if form.instance.organ_name == "Heart" or form.instance.organ_name == "Liver" or form.instance.organ_name == "Pancreas" or form.instance.organ_name == "Intestines":
                form.instance.quantity = 1
        elif type == 2:
            finalized_type = "Tissue"
            finalized_type_child = form.instance.tissue_name
            finalized_field_name = "tissue_name"
        else:
            finalized_type = "Undefined"
        title = f"I want to donate {finalized_type} [{finalized_type_child}]"
        donation_qs = Donation.objects.filter(
            user=self.request.user.profile, title__iexact=title, donation_progress__progress_status=0
        ).exclude(title__iexact=self.object.title)
        form.instance.title = f"I want to donate {finalized_type} [{finalized_type_child}]"
        if self.object.category == 0 and type == 0:
            form.instance.blood_bag = 1
        if type == 0:
            form.instance.blood_bag = 1
        blood_group = form.instance.blood_group
        blood_bag = form.instance.blood_bag
        # organ_name = form.instance.organ_name
        details = form.instance.details
        # if form.cleaned_data['details_fake'] != "":
        # if self.request.POST.get("details_fake") != "":
        # details_fake = form.cleaned_data['details_fake']
        details_fake = self.request.POST.get("details_fake")
        contact = form.instance.contact
        contact2 = form.instance.contact2
        contact3 = form.instance.contact3
        contact_privacy = self.request.POST.get("contact_privacy")
        if contact_privacy == None or contact_privacy == "":
            contact_privacy = 0
        donate_type = self.request.POST.get("donate-type")
        if donate_type == None or donate_type == "":
            donate_type = 0
        form.instance.donate_type = donate_type
        living_organs = ["Kidney", "Lungs"]
        deceased_organs = ["Heart", "Pancreas", "Liver", "Intestines"]
        if form.instance.type == 2:
            form.instance.donate_type = 1
        elif form.instance.type == 1 and form.instance.organ_name in deceased_organs:
            form.instance.donate_type = 1
        elif form.instance.type == 1 and form.instance.organ_name in living_organs and int(form.instance.quantity) > 1:
            form.instance.donate_type = 1
        else:
            form.instance.donate_type = 0
        # if donate_type == "1" or donate_type == 1:
        #     form.instance.is_verified = False
        # print(contact_privacy)
        form.instance.contact_privacy = contact_privacy
        contactFake = self.request.POST.get("contact_fake")
        contact2Fake = self.request.POST.get("contact2_fake")
        contact3Fake = self.request.POST.get("contact3_fake")
        preferred_date = form.instance.preferred_date
        preferred_date_from = form.instance.preferred_date_from
        preferred_date_to = form.instance.preferred_date_to

        user_profile = UserProfile.objects.filter(user=self.request.user)
        if user_profile.exists():
            profile = user_profile.first()
            if donation_qs.exists():
                donation_qs_url = donation_qs.first().get_absolute_url()
                if not self.request.user.is_superuser:
                    form.add_error(
                        f'{finalized_field_name}', forms.ValidationError(
                            f"You already have a pending post similar to this. Please update that post if you need any changes. click <a href='{donation_qs_url}'>here</a> to view the post."
                        )
                    )
            elif blood_group == None:
                form.add_error(
                    'blood_group', forms.ValidationError(
                        "You must select blood group."
                    )
                )
            elif type == 0 and blood_bag == None:
                form.add_error(
                    'blood_bag', forms.ValidationError(
                        "You must enter blood bag quantity."
                    )
                )
            elif donate_type == "1" and contact2 == None:
                form.add_error(
                    'contact2', forms.ValidationError(
                        "You must enter second contact number (Contact number of your family member/friend)."
                    )
                )
            elif not contact2 == None and contact == contact2:
                form.add_error(
                    'contact2', forms.ValidationError(
                        "You have entered this contact in first contact. Please enter different one."
                    )
                )
            elif not contact3 == None and contact == contact3:
                form.add_error(
                    'contact3', forms.ValidationError(
                        "You have entered this contact in first contact. Please enter different one."
                    )
                )
            elif not contact2 == None and not contact3 == None and contact2 == contact3:
                form.add_error(
                    'contact3', forms.ValidationError(
                        "You have entered this contact in second contact. Please enter different one."
                    )
                )

            # elif type == 0 and blood_bag == None:
            #     form.add_error(
            #         'blood_bag', forms.ValidationError(
            #             "You must enter required blood bag quantity."
            #         )
            #     )
            # elif type == 1 and organ_name == None:
            #     form.add_error(
            #         'organ_name', forms.ValidationError(
            #             "You must enter organ name."
            #         )
            #     )
            elif preferred_date_from == None and preferred_date_to is not None:
                form.add_error(
                    'preferred_date_from', forms.ValidationError(
                        "You must select Preferred Date From if you select Preferred Date To."
                    )
                )
            elif preferred_date_to == None and preferred_date_from is not None:
                form.add_error(
                    'preferred_date_to', forms.ValidationError(
                        "You must select Preferred Date To if you select Preferred Date From."
                    )
                )
            elif type == 1 and form.instance.organ_name == None:
                form.add_error(
                    'organ_name', forms.ValidationError(
                        "You must select organ name."
                    )
                )
            elif type == 2 and form.instance.tissue_name == None:
                form.add_error(
                    'tissue_name', forms.ValidationError(
                        "You must select tissue name."
                    )
                )
            elif type == 1 and form.instance.quantity == None:
                form.add_error(
                    'quantity', forms.ValidationError(
                        "You must enter the quantity."
                    )
                )
            else:
                # Save the form
                if contact is not None and not contactFake == None:
                    form.instance.contact = contactFake + contact
                if contact2 is not None and not contact2Fake == None:
                    form.instance.contact2 = contact2Fake + contact2
                if contact3 is not None and not contact3Fake == None:
                    form.instance.contact3 = contact3Fake + contact3
                if details_fake != "":
                    form.instance.details = details_fake
                if not self.request.user.is_superuser:
                    form.instance.user = profile
                # form.instance.category = category
                if form.instance.donate_type == 1:
                    form.instance.preferred_date = None
                    form.instance.preferred_date_from = None
                    form.instance.preferred_date_to = None
                messages.add_message(self.request, messages.SUCCESS,
                                     "Donation offer has been updated successfully!")
                return super().form_valid(form)
        return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(OfferDonationUpdateView, self).get_form_kwargs()
        if self.form_class:
            kwargs.update({'request': self.request})
            kwargs.update({'object': self.get_object()})
        return kwargs

    def user_passes_test(self, request):
        if request.user.is_authenticated:
            self.object = self.get_object()
            if self.object.user.user == request.user:
                if self.object.donation_progress.progress_status == 0 and self.object.has_response() == False:
                    return True
            elif self.request.user.is_superuser:
                return True
            else:
                return False
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(OfferDonationUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse('donations:donation_offers_list')
        return reverse('donations:my_donation_offers')

    def get_context_data(self, **kwargs):
        context = super(OfferDonationUpdateView,
                        self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        context['page_title'] = "Update donation offer"
        context['page_type'] = "OFFER"
        last_blood_donated_filter = DonationProgress.objects.filter(
            donation__user=self.request.user.profile, donation__category=0, donation__type=0,
            progress_status=1
        )
        can_donate_blood = True
        if last_blood_donated_filter.exists():
            if not last_blood_donated_filter.last().completion_date == None:
                day_difference = datetime.date.today(
                ) - last_blood_donated_filter.last().completion_date
                if day_difference.days < 90:
                    can_donate_blood = False
                    context['last_donated_ago'] = day_difference.days
                    context['waiting_days_remaining'] = 90 - \
                        int(day_difference.days)
                    context['last_donated_object'] = last_blood_donated_filter.last()
        context['can_donate_blood'] = can_donate_blood
        return context


@method_decorator(decorators, name='dispatch')
class DonationOffersCardListView(AjaxListView):
    template_name = 'donations/donation-list-card.html'
    page_template = 'donations/snippets/page_template_list.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            qs = Donation.objects.all().offers().is_published().dynamic_order()
        else:
            # qs = Donation.objects.all().offers().is_published(
            # ).living_donates().is_verified().dynamic_order()
            qs = Donation.objects.all().offers().is_published(
            ).is_verified().dynamic_order()
        # if qs.exists():
        #     return qs
        return qs

    def get_context_data(self, **kwargs):
        context = super(DonationOffersCardListView,
                        self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        context['page_title'] = "Donation Offers"
        context['can_filter'] = True
        context['page_type'] = "OFFER"
        return context


@method_decorator(decorators, name='dispatch')
class DonationOffersListView(ListView):
    template_name = 'donations/donation-list.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            qs = Donation.objects.all().offers().is_published().dynamic_order()
        else:
            # qs = Donation.objects.all().offers().is_published().living_donates().is_verified().dynamic_order()
            qs = Donation.objects.all().offers().is_published().is_verified().dynamic_order()
        # if qs.exists():
        #     return qs
        return qs

    def get_context_data(self, **kwargs):
        context = super(DonationOffersListView,
                        self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        context['page_title'] = "Donation Offers"
        context['can_filter'] = True
        context['page_type'] = "OFFER"
        return context


@method_decorator(decorators, name='dispatch')
class MyDonationOffersListView(AjaxListView):
    template_name = 'donations/donation-list-card.html'
    page_template = 'donations/snippets/page_template_list.html'

    def get_queryset(self):
        qs = Donation.objects.all().donations_by_user(
            self.request.user).offers().latest()
        if qs.exists():
            return qs
        return None

    def get_context_data(self, **kwargs):
        context = super(MyDonationOffersListView,
                        self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        context['page_title'] = "My Offers"
        context['can_filter'] = False
        context['page_type'] = "OFFER"
        return context


# ====================== Donation Requests ======================

@method_decorator(decorators, name='dispatch')
@method_decorator(can_ask_for_a_donor_required, name='dispatch')
class DonationRequestCreateView(CreateView):
    template_name = 'donations/donation-manage.html'
    form_class = DonationForm

    def form_valid(self, form):
        category = 1
        type = form.instance.type
        if type == 0:
            finalized_type = "Blood"
            finalized_type_child = form.instance.blood_group
            finalized_field_name = "blood_group"
        elif type == 1:
            finalized_type = "Organ"
            finalized_type_child = form.instance.organ_name
            finalized_field_name = "organ_name"
            if form.instance.organ_name == "Heart" or form.instance.organ_name == "Liver" or form.instance.organ_name == "Pancreas" or form.instance.organ_name == "Intestines":
                form.instance.quantity = 1
        elif type == 2:
            finalized_type = "Tissue"
            finalized_type_child = form.instance.tissue_name
            finalized_field_name = "tissue_name"
        else:
            finalized_type = "Undefined"
        title = f"I need {finalized_type} [{finalized_type_child}] donor"
        donation_qs = Donation.objects.filter(
            user=self.request.user.profile, title__iexact=title, donation_progress__progress_status=0
        )
        form.instance.title = f"I need {finalized_type} [{finalized_type_child}] donor"
        # if type == 0:
        #     form.instance.blood_bag = 1
        blood_group = form.instance.blood_group
        blood_bag = form.instance.blood_bag
        # print(blood_bag)
        # organ_name = form.instance.organ_name
        details = form.instance.details
        details_fake = form.cleaned_data['details_fake']
        contact = form.instance.contact
        contact2 = form.instance.contact2
        contact3 = form.instance.contact3
        contact_privacy = self.request.POST.get("contact_privacy")
        donate_type = self.request.POST.get("donate-type")
        form.instance.donate_type = donate_type
        living_organs = ["Kidney", "Lungs"]
        deceased_organs = ["Heart", "Pancreas", "Liver", "Intestines"]
        if form.instance.type == 2:
            form.instance.donate_type = 1
        elif form.instance.type == 1 and form.instance.organ_name in deceased_organs:
            form.instance.donate_type = 1
        elif form.instance.type == 1 and form.instance.organ_name in living_organs and int(form.instance.quantity) > 1:
            form.instance.donate_type = 1
        else:
            form.instance.donate_type = 0
        if donate_type == "1" or donate_type == 1:
            form.instance.is_verified = False
        # print(contact_privacy)
        form.instance.contact_privacy = contact_privacy
        contactFake = self.request.POST.get("contact_fake")
        contact2Fake = self.request.POST.get("contact2_fake")
        contact3Fake = self.request.POST.get("contact3_fake")
        preferred_date = form.instance.preferred_date
        preferred_date_from = form.instance.preferred_date_from
        preferred_date_to = form.instance.preferred_date_to

        user_profile = UserProfile.objects.filter(user=self.request.user)
        if user_profile.exists():
            profile = user_profile.first()
            if donation_qs.exists():
                donation_qs_url = donation_qs.first().get_absolute_url()
                form.add_error(
                    f'{finalized_field_name}', forms.ValidationError(
                        f"You already have a pending post similar to this. Please update that post if you need any changes. click <a href='{donation_qs_url}'>here</a> to view the post."
                    )
                )
            elif blood_group == None:
                form.add_error(
                    'blood_group', forms.ValidationError(
                        "You must select blood group."
                    )
                )
            elif type == 0 and blood_bag == None:
                form.add_error(
                    'blood_bag', forms.ValidationError(
                        "You must enter blood bag quantity."
                    )
                )
            elif donate_type == "1" and contact2 == None:
                form.add_error(
                    'contact2', forms.ValidationError(
                        "You must enter second contact number (Contact number of your family member/friend)."
                    )
                )
            elif not contact2 == None and contact == contact2:
                form.add_error(
                    'contact2', forms.ValidationError(
                        "You have entered this contact in first contact. Please enter different one."
                    )
                )
            elif not contact3 == None and contact == contact3:
                form.add_error(
                    'contact3', forms.ValidationError(
                        "You have entered this contact in first contact. Please enter different one."
                    )
                )
            elif not contact2 == None and not contact3 == None and contact2 == contact3:
                form.add_error(
                    'contact3', forms.ValidationError(
                        "You have entered this contact in second contact. Please enter different one."
                    )
                )
            elif preferred_date_from == None and preferred_date_to is not None:
                form.add_error(
                    'preferred_date_from', forms.ValidationError(
                        "You must select Preferred Date From if you select Preferred Date To."
                    )
                )
            elif preferred_date_to == None and preferred_date_from is not None:
                form.add_error(
                    'preferred_date_to', forms.ValidationError(
                        "You must select Preferred Date To if you select Preferred Date From."
                    )
                )
            elif type == 1 and form.instance.organ_name == None:
                form.add_error(
                    'organ_name', forms.ValidationError(
                        "You must select organ name."
                    )
                )
            elif type == 2 and form.instance.tissue_name == None:
                form.add_error(
                    'tissue_name', forms.ValidationError(
                        "You must select tissue name."
                    )
                )
            elif type == 1 and form.instance.quantity == None:
                form.add_error(
                    'quantity', forms.ValidationError(
                        "You must enter the quantity."
                    )
                )
            else:
                # Save the form
                if contact is not None:
                    form.instance.contact = contactFake + contact
                if contact2 is not None:
                    form.instance.contact2 = contact2Fake + contact2
                if contact3 is not None:
                    form.instance.contact3 = contact3Fake + contact3
                if details_fake != "":
                    form.instance.details = details_fake
                form.instance.user = profile
                form.instance.category = category
                if form.instance.donate_type == 1:
                    form.instance.preferred_date = None
                    form.instance.preferred_date_from = None
                    form.instance.preferred_date_to = None
                messages.add_message(self.request, messages.SUCCESS,
                                     "Your donation request has been created successfully!")
                return super().form_valid(form)
            # print(donate_type)
        return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(DonationRequestCreateView, self).get_form_kwargs()
        if self.form_class:
            kwargs.update({'request': self.request})
            kwargs.update({'object': None})
        return kwargs

    def get_success_url(self):
        return reverse('donations:my_donation_requests')

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
        context['page_title'] = "Create donation request"
        # last_blood_donated_filter = DonationProgress.objects.filter(
        #     donation__user=self.request.user.profile, donation__category=0, donation__type=0,
        #     progress_status=1
        # )
        # can_donate_blood = True
        # if last_blood_donated_filter.exists():
        #     if not last_blood_donated_filter.last().completion_date == None:
        #         day_difference = datetime.datetime.now(
        #         ) - last_blood_donated_filter.last().completion_date
        #         if day_difference.days < 90:
        #             can_donate_blood = False
        #             context['last_donated_ago'] = day_difference.days
        #             context['waiting_days_remaining'] = 90 - \
        #                 int(day_difference.days)
        #             context['last_donated_object'] = last_blood_donated_filter.last()
        context['can_donate_blood'] = True
        context['page_type'] = "REQUEST"
        return context


@method_decorator(decorators, name='dispatch')
@method_decorator(can_ask_for_a_donor_required, name='dispatch')
class DonationRequestUpdateView(UpdateView):
    template_name = 'donations/donation-manage.html'
    form_class = DonationForm

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        return Donation.objects.get_by_slug(slug, self.request)

    def form_valid(self, form):
        # category = 0
        self.object = self.get_object()
        type = form.instance.type
        if type == 0:
            finalized_type = "Blood"
            finalized_type_child = form.instance.blood_group
            finalized_field_name = "blood_group"
        elif type == 1:
            finalized_type = "Organ"
            finalized_type_child = form.instance.organ_name
            finalized_field_name = "organ_name"
            if form.instance.organ_name == "Heart" or form.instance.organ_name == "Liver" or form.instance.organ_name == "Pancreas" or form.instance.organ_name == "Intestines":
                form.instance.quantity = 1
        elif type == 2:
            finalized_type = "Tissue"
            finalized_type_child = form.instance.tissue_name
            finalized_field_name = "tissue_name"
        else:
            finalized_type = "Undefined"
        title = f"I need {finalized_type} [{finalized_type_child}] donor"
        donation_qs = Donation.objects.filter(
            user=self.request.user.profile, title__iexact=title, donation_progress__progress_status=0
        ).exclude(title__iexact=self.object.title)
        form.instance.title = f"I need {finalized_type} [{finalized_type_child}] donor"
        # if self.object.category == 0 and type == 0:
        #     form.instance.blood_bag = 1
        blood_group = form.instance.blood_group
        blood_bag = form.instance.blood_bag
        # organ_name = form.instance.organ_name
        details = form.instance.details
        details_fake = self.request.POST.get("details_fake")
        contact = form.instance.contact
        contact2 = form.instance.contact2
        contact3 = form.instance.contact3
        contact_privacy = self.request.POST.get("contact_privacy")
        if contact_privacy == None or contact_privacy == "":
            contact_privacy = 0
        donate_type = self.request.POST.get("donate-type")
        if donate_type == None or donate_type == "":
            donate_type = 0
        form.instance.donate_type = donate_type
        living_organs = ["Kidney", "Lungs"]
        deceased_organs = ["Heart", "Pancreas", "Liver", "Intestines"]
        if form.instance.type == 2:
            form.instance.donate_type = 1
        elif form.instance.type == 1 and form.instance.organ_name in deceased_organs:
            form.instance.donate_type = 1
        elif form.instance.type == 1 and form.instance.organ_name in living_organs and int(form.instance.quantity) > 1:
            form.instance.donate_type = 1
        else:
            form.instance.donate_type = 0
        # if donate_type == "1" or donate_type == 1:
        #     form.instance.is_verified = False
        # print(contact_privacy)
        form.instance.contact_privacy = contact_privacy
        contactFake = self.request.POST.get("contact_fake")
        contact2Fake = self.request.POST.get("contact2_fake")
        contact3Fake = self.request.POST.get("contact3_fake")
        preferred_date = form.instance.preferred_date
        preferred_date_from = form.instance.preferred_date_from
        preferred_date_to = form.instance.preferred_date_to

        user_profile = UserProfile.objects.filter(user=self.request.user)
        if user_profile.exists():
            profile = user_profile.first()
            if donation_qs.exists():
                donation_qs_url = donation_qs.first().get_absolute_url()
                if not self.request.user.is_superuser:
                    form.add_error(
                        f'{finalized_field_name}', forms.ValidationError(
                            f"You already have a pending post similar to this. Please update that post if you need any changes. click <a href='{donation_qs_url}'>here</a> to view the post."
                        )
                    )
            elif blood_group == None:
                form.add_error(
                    'blood_group', forms.ValidationError(
                        "You must select blood group."
                    )
                )
            elif type == 0 and blood_bag == None:
                form.add_error(
                    'blood_bag', forms.ValidationError(
                        "You must enter blood bag quantity."
                    )
                )
            elif donate_type == "1" and contact2 == None:
                form.add_error(
                    'contact2', forms.ValidationError(
                        "You must enter second contact number (Contact number of your family member/friend)."
                    )
                )
            elif not contact2 == None and contact == contact2:
                form.add_error(
                    'contact2', forms.ValidationError(
                        "You have entered this contact in first contact. Please enter different one."
                    )
                )
            elif not contact3 == None and contact == contact3:
                form.add_error(
                    'contact3', forms.ValidationError(
                        "You have entered this contact in first contact. Please enter different one."
                    )
                )
            elif not contact2 == None and not contact3 == None and contact2 == contact3:
                form.add_error(
                    'contact3', forms.ValidationError(
                        "You have entered this contact in second contact. Please enter different one."
                    )
                )
            elif preferred_date_from == None and preferred_date_to is not None:
                form.add_error(
                    'preferred_date_from', forms.ValidationError(
                        "You must select Preferred Date From if you select Preferred Date To."
                    )
                )
            elif preferred_date_to == None and preferred_date_from is not None:
                form.add_error(
                    'preferred_date_to', forms.ValidationError(
                        "You must select Preferred Date To if you select Preferred Date From."
                    )
                )
            elif type == 1 and form.instance.organ_name == None:
                form.add_error(
                    'organ_name', forms.ValidationError(
                        "You must select organ name."
                    )
                )
            elif type == 2 and form.instance.tissue_name == None:
                form.add_error(
                    'tissue_name', forms.ValidationError(
                        "You must select tissue name."
                    )
                )
            elif type == 1 and form.instance.quantity == None:
                form.add_error(
                    'quantity', forms.ValidationError(
                        "You must enter the quantity."
                    )
                )
            else:
                # Save the form
                if contact is not None and not contactFake == None:
                    form.instance.contact = contactFake + contact
                if contact2 is not None and not contact2Fake == None:
                    form.instance.contact2 = contact2Fake + contact2
                if contact3 is not None and not contact3Fake == None:
                    form.instance.contact3 = contact3Fake + contact3
                if details_fake != "":
                    form.instance.details = details_fake
                if not self.request.user.is_superuser:
                    form.instance.user = profile
                # form.instance.category = category
                if form.instance.donate_type == 1:
                    form.instance.preferred_date = None
                    form.instance.preferred_date_from = None
                    form.instance.preferred_date_to = None
                messages.add_message(self.request, messages.SUCCESS,
                                     "Donation request has been updated successfully!")
                return super().form_valid(form)
        return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(DonationRequestUpdateView, self).get_form_kwargs()
        if self.form_class:
            kwargs.update({'request': self.request})
            kwargs.update({'object': self.get_object()})
        return kwargs

    def user_passes_test(self, request):
        if request.user.is_authenticated:
            self.object = self.get_object()
            if self.object.user.user == request.user:
                if self.object.donation_progress.progress_status == 0 and self.object.has_response() == False:
                    return True
            elif self.request.user.is_superuser:
                return True
            else:
                return False
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(DonationRequestUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse('donations:donation_requests_list')
        return reverse('donations:my_donation_requests')

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
        context['page_title'] = "Update donation request"
        # last_blood_donated_filter = DonationProgress.objects.filter(
        #     donation__user=self.request.user.profile, donation__category=0, donation__type=0,
        #     progress_status=1
        # )
        # can_donate_blood = True
        # if last_blood_donated_filter.exists():
        #     if not last_blood_donated_filter.last().completion_date == None:
        #         day_difference = datetime.datetime.now(
        #         ) - last_blood_donated_filter.last().completion_date
        #         if day_difference.days < 90:
        #             can_donate_blood = False
        #             context['last_donated_ago'] = day_difference.days
        #             context['waiting_days_remaining'] = 90 - \
        #                 int(day_difference.days)
        #             context['last_donated_object'] = last_blood_donated_filter.last()
        context['can_donate_blood'] = True
        context['page_type'] = "REQUEST"
        return context


@method_decorator(decorators, name='dispatch')
class DonationRequestsCardListView(AjaxListView):
    template_name = 'donations/donation-list-card.html'
    page_template = 'donations/snippets/page_template_list.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            qs = Donation.objects.all().requests().is_published().dynamic_order()
        else:
            # qs = Donation.objects.all().requests().is_published(
            # ).living_donates().is_verified().dynamic_order()
            qs = Donation.objects.all().requests().is_published(
            ).is_verified().dynamic_order()
        # if qs.exists():
        #     return qs
        return qs

    def get_context_data(self, **kwargs):
        context = super(DonationRequestsCardListView,
                        self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        context['page_title'] = "Donation Requests"
        context['can_filter'] = True
        context['page_type'] = "REQUEST"
        return context


@method_decorator(decorators, name='dispatch')
class DonationRequestsListView(ListView):
    template_name = 'donations/donation-list.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            qs = Donation.objects.all().requests().is_published().dynamic_order()
        else:
            # qs = Donation.objects.all().requests().is_published(
            # ).living_donates().is_verified().dynamic_order()
            qs = Donation.objects.all().requests().is_published(
            ).is_verified().dynamic_order()
        # if qs.exists():
        #     return qs
        return qs

    def get_context_data(self, **kwargs):
        context = super(DonationRequestsListView,
                        self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        context['page_title'] = "Donation Requests"
        context['can_filter'] = True
        context['page_type'] = "REQUEST"
        return context


@method_decorator(decorators, name='dispatch')
class MyDonationRequestsListView(AjaxListView):
    template_name = 'donations/donation-list-card.html'
    page_template = 'donations/snippets/page_template_list.html'

    def get_queryset(self):
        qs = Donation.objects.all().donations_by_user(
            self.request.user).requests().latest()
        if qs.exists():
            return qs
        return None

    def get_context_data(self, **kwargs):
        context = super(MyDonationRequestsListView,
                        self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        context['page_title'] = "My Requests"
        context['can_filter'] = False
        context['page_type'] = "REQUEST"
        return context


# ==================== Donation All Dynamic Mixed ====================

@method_decorator(decorators, name='dispatch')
class DonationDetailView(DetailView):
    template_name = 'donations/donation-details.html'

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        return Donation.objects.get_by_slug(slug, self.request)

    def get_context_data(self, **kwargs):
        context = super(DonationDetailView, self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        context['page_title'] = "Donation Details"
        return context


@method_decorator(decorators, name='dispatch')
class DonationRespondCreateView(CreateView):
    template_name = 'donations/respond.html'
    form_class = DonationRespondForm

    # def get_object(self, *args, **kwargs):
    #     slug = self.kwargs.get('slug')
    #     return Donation.objects.get_by_slug(slug, self.request)

    def get(self, request, *args, **kwargs):
        response = super(DonationRespondCreateView, self).get(
            request, *args, **kwargs)
        if not self.request.user.profile.blood_group == None:
            slug = self.kwargs.get('slug')
            donation = Donation.objects.get_by_slug(slug, self.request)
            if not donation.blood_group == self.request.user.profile.blood_group:
                object_instance = "Undefined"
                if donation.category == 0:
                    object_instance = "Donor"
                if donation.category == 1:
                    object_instance = "Donation seeker"
                messages.add_message(self.request, messages.WARNING,
                                     f"Blood group don't matched! Blood group needs to be matched for transplantation. Please be carefull. Your blood group is '{request.user.profile.blood_group}' and {object_instance}'s blood group is '{donation.blood_group}' !")
                if donation.category == 1 or donation.category == 0:
                    return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', '/'))
        return response

    def form_valid(self, form):
        slug = self.kwargs.get('slug')
        donation = Donation.objects.get_by_slug(slug, self.request)
        donation_respond_filter = DonationRespond.objects.filter(
            donation=donation, respondent=self.request.user)
        if not donation_respond_filter.exists():
            contact = form.instance.contact
            contactFake = self.request.POST.get("contact_fake")
            message = form.instance.message
            if contact is not None:
                contact_bind = contactFake + contact
                form.instance.contact = contact_bind
            else:
                contact_bind = "Not Provided"
            if message is not None:
                message_bind = message
            else:
                message_bind = "Not Provided"
            # Respondent VS Receiver
            super_user_qs = User.objects.filter(is_superuser=True)
            respondent = self.request.user.profile.get_dynamic_name()
            if donation.donate_type == 0:
                receiver = donation.user.user
                respondent_receiver = donation.user.get_dynamic_name()
                receiver_email = donation.user.user.email
                receiver_contact = donation.contact
            else:
                receiver = super_user_qs.first()
                respondent_receiver = super_user_qs.first().profile.get_dynamic_name()
                receiver_email = super_user_qs.first().email
                if not super_user_qs.first().profile.contact == None:
                    receiver_contact = super_user_qs.first().profile.contact
                else:
                    receiver_contact = "Not Provided"
            # URL Prefix
            domain = self.request.META['HTTP_HOST']
            if self.request.is_secure():
                scheme = "https://"
            else:
                scheme = "http://"
            donation_url = reverse('donations:donation_details',
                                   kwargs={'slug': slug})
            redirect_url = f"{scheme}{domain}{donation_url}"

            # Send SMS
            # message_default = f"Hello from BDonar! {respondent} has responded to your post. Respondent Contact: {contact_bind}. Respondent Message: {message_bind}"
            # url = 'https://api2.onnorokomsms.com/sendsms.asmx?WSDL'
            # client = Client(url)
            # userName = settings.ONNOROKOM_USERNAME
            # password = settings.ONNOROKOM_PASSWORD
            # recipientNumber = receiver_contact
            # smsText = message_default
            # smsType = 'TEXT'
            # maskName = ''
            # campaignName = ''
            # client.service.OneToOne(userName, password, recipientNumber,
            #                         smsText, smsType, maskName, campaignName)

            # Sending Email
            mail_msg = f"Hello {respondent_receiver} ! <br> {respondent} has responded to your post. <br> click <a href='{redirect_url}' target='_blank'>here</a> to view. <br> <br> Respondent Contact: <b><a href='#'>{contact_bind}</a></b> <br> Respondent Message: {message_bind} <br> Have a good day. <br>Thanks for being with us."
            mail_subject = f'{respondent} has responded to your post.'
            mail_from = 'admin@bdonor.com'
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
            # Save form
            form.instance.donation = donation
            form.instance.respondent = self.request.user
            messages.add_message(self.request, messages.SUCCESS,
                                 "Your response has been made successfully!")
            # Create Notification
            request = self.request
            sender = self.request.user
            receiver = receiver
            category = 'donationRespond_Create'
            identifier = donation.slug
            subject = f"{respondent} has responded to your donation post"
            message = f"{respondent} has responded to your post : '<i>{donation.title}</i>'. <br> click <a href='{redirect_url}' target='_blank'>here</a> to view. <br> <br> Respondent Contact: <b><a href='#'>{contact_bind}</a></b> <br> Respondent Message: {message_bind}"
            create_notification(
                request=request, sender=sender, receiver=receiver, category=category, identifier=identifier, subject=subject, message=message
            )
            return super().form_valid(form)
        else:
            messages.add_message(self.request, messages.WARNING,
                                 "You have already responded to this post!")
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(DonationRespondCreateView, self).get_form_kwargs()
        if self.form_class:
            kwargs.update({'request': self.request})
            kwargs.update({'object': None})
        return kwargs

    def get_success_url(self):
        slug = self.kwargs.get('slug')
        return reverse('donations:donation_details', kwargs={'slug': slug})

    def get_context_data(self, **kwargs):
        context = super(DonationRespondCreateView,
                        self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        slug = self.kwargs.get('slug')
        donation = Donation.objects.get_by_slug(slug, self.request)
        context['object'] = donation
        donation_respond_filter = DonationRespond.objects.filter(
            donation=donation, respondent=self.request.user)
        if donation_respond_filter.exists():
            context['respondant_exists'] = True
        else:
            context['respondant_exists'] = False
        last_blood_donated_filter = DonationProgress.objects.filter(
            donation__user=self.request.user.profile, donation__category=0, donation__type=0,
            progress_status=1
        )
        can_donate_blood = True
        if last_blood_donated_filter.exists():
            if not last_blood_donated_filter.last().completion_date == None:
                day_difference = datetime.date.today(
                ) - last_blood_donated_filter.last().completion_date
                if day_difference.days < 90:
                    can_donate_blood = False
                    context['last_donated_ago'] = day_difference.days
                    context['waiting_days_remaining'] = 90 - \
                        int(day_difference.days)
                    context['last_donated_object'] = last_blood_donated_filter.last()
        context['can_donate_blood'] = can_donate_blood
        return context

    def user_passes_test(self, request):
        if request.user.is_authenticated:
            if not request.user.profile.blood_group == None and request.user.profile.blood_group != "":
                return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            # block_suspicious_user(request)
            messages.add_message(self.request, messages.INFO,
                                 "Please select your blood group by updating your profile!")
            return HttpResponseRedirect(
                reverse('profile_update', kwargs={
                        'slug': request.user.profile.slug})
            )
        slug = self.kwargs.get('slug')
        donation = Donation.objects.get_by_slug(slug, self.request)
        if self.request.user.user_permissions_user.can_donate == False and donation.category == 1:
            messages.add_message(self.request, messages.INFO,
                                 "You are not allowed to donate!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        if self.request.user.user_permissions_user.can_ask_for_a_donor == False and donation.category == 0:
            messages.add_message(self.request, messages.INFO,
                                 "You are not allowed to ask for a donor!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return super(DonationRespondCreateView, self).dispatch(request, *args, **kwargs)


@csrf_exempt
@login_required
@can_browse_required
def withdraw_respond(request):
    url = reverse('home')
    user = request.user
    if request.method == "POST":
        slug = request.POST.get("slug")
        qs = DonationRespond.objects.filter(
            donation__slug=slug, respondent=user)
        if qs.exists():
            qs.delete()
            messages.add_message(request, messages.SUCCESS,
                                 "Your response has been withdrawn successfully!")
            url = reverse('donations:donation_details',
                          kwargs={'slug': slug})
        else:
            messages.add_message(request, messages.WARNING,
                                 "Something went wrong!")
    return HttpResponseRedirect(url)


@csrf_exempt
@login_required
@can_browse_required
def donation_delete(request):
    url = reverse('home')
    user = request.user
    if request.method == "POST":
        slug = request.POST.get("slug")
        qs = Donation.objects.filter(slug=slug)
        if qs.exists():
            if qs.first().user == user.profile:
                qs.delete()
                messages.add_message(request, messages.SUCCESS,
                                     "Deleted successfully!")
                url = reverse('donations:my_donation_offers')
            else:
                block_suspicious_user(request)
        else:
            messages.add_message(request, messages.WARNING,
                                 "Not found!")
    return HttpResponseRedirect(url)


@method_decorator(decorators, name='dispatch')
class DonationFilteredListView(ListView):
    template_name = "donations/search-result.html"

    def get_context_data(self, *args, **kwargs):
        context = super(DonationFilteredListView,
                        self).get_context_data(*args, **kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        query = self.request.GET.get('q')
        query_type = self.request.GET.get('donation-filter-type')
        query_priority = self.request.GET.get('donation-filter-priority')
        query_status = self.request.GET.get('donation-filter-status')
        query_donate_type = self.request.GET.get('donation-filter-donate_type')
        query_is_verified = self.request.GET.get('donation-filter-is_verified')
        result_counter = self.object_list.count()
        context['query'] = query
        context['query_type'] = query_type
        context['query_priority'] = query_priority
        context['query_status'] = query_status
        context['query_donate_type'] = query_donate_type
        context['query_is_verified'] = query_is_verified
        context['count'] = result_counter
        context['page_type'] = self.request.GET.get('page-type', None)
        context['can_filter'] = True
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        method_dict = request.GET
        query = method_dict.get('q', None)
        page_type = method_dict.get('page-type', None)
        type_filtered = method_dict.get('donation-filter-type', None)
        priority_filtered = method_dict.get('donation-filter-priority', None)
        status_filtered = method_dict.get('donation-filter-status', None)
        donate_type_filtered = method_dict.get(
            'donation-filter-donate_type', None)
        is_verified_filtered = method_dict.get(
            'donation-filter-is_verified', None)
        if page_type == "OFFER":
            cat = 0
        else:
            cat = 1
        qs = Donation.objects.all().filter(category=cat)

        filter_modules_dict = {'type': type_filtered, 'priority': priority_filtered,
                               'donation_progress__progress_status': status_filtered,
                               'donate_type': donate_type_filtered,
                               'is_verified': is_verified_filtered}
        if not type_filtered == "" or not priority_filtered == "" or not status_filtered == "" or not donate_type_filtered == "" or not is_verified_filtered == "":
            #  ------------------------- Magic Starts -------------------------
            from collections import OrderedDict
            ordered_dict = OrderedDict(filter_modules_dict)

            list_pre = []
            for key, value in ordered_dict.items():
                if value:
                    list_pre.append(f"{key}- {value}")
            list_to_dict_like_string = ", ".join(list_pre)
            string_to_dict = dict((x.strip(), y.strip()) for x, y in (
                element.split('-') for element in list_to_dict_like_string.split(', ')))

            filter_dict = string_to_dict
        #  ------------------------- Magic Ends -------------------------
        else:
            filter_dict = {'publication_status': 0}

        # if not type_filtered == "" and not priority_filtered == "" and not status_filtered == "" and not donate_type_filtered == "" and not is_verified_filtered == "":
        #     filter_dict = {'type': type_filtered, 'priority': priority_filtered, 'donate_type': donate_type_filtered, 'is_verified': is_verified_filtered,
        #                    'donation_progress__progress_status': status_filtered}
        # else:
        #     filter_dict = {'publication_status': 0}

        # All
        # if not type_filtered == "" and not priority_filtered == "" and not status_filtered == "" and not donate_type_filtered == "" and not is_verified_filtered == "":
        #     filter_dict = {'type': type_filtered, 'priority': priority_filtered, 'donate_type': donate_type_filtered, 'is_verified': is_verified_filtered,
        #                    'donation_progress__progress_status': status_filtered}

        # # Solo
        # elif not type_filtered == "" and priority_filtered == "" and status_filtered == "" and donate_type_filtered == "" and is_verified_filtered == "":
        #     filter_dict = {'type': type_filtered}
        # elif type_filtered == "" and not priority_filtered == "" and status_filtered == "" and donate_type_filtered == "" and is_verified_filtered == "":
        #     filter_dict = {'priority': priority_filtered}
        # elif type_filtered == "" and priority_filtered == "" and not status_filtered == "" and donate_type_filtered == "" and is_verified_filtered == "":
        #     filter_dict = {'donation_progress__progress_status': status_filtered}
        # elif type_filtered == "" and priority_filtered == "" and status_filtered == "" and not donate_type_filtered == "" and is_verified_filtered == "":
        #     filter_dict = {
        #         'donate_type': donate_type_filtered}
        # elif type_filtered == "" and priority_filtered == "" and status_filtered == "" and donate_type_filtered == "" and not is_verified_filtered == "":
        #     filter_dict = {
        #         'is_verified': iis_verified_filtereds_verified_filtered}

        # # Type
        # elif not type_filtered == "" and not priority_filtered == "" and status_filtered == "" and donate_type_filtered == "" and is_verified_filtered == "":
        #     filter_dict = {'type': type_filtered, 'priority': priority_filtered}
        # elif not type_filtered == "" and priority_filtered == "" and not status_filtered == "" and donate_type_filtered == "" and is_verified_filtered == "":
        #     filter_dict = {'type': type_filtered,
        #                    'donation_progress__progress_status': status_filtered}
        # elif not type_filtered == "" and priority_filtered == "" and status_filtered == "" and not donate_type_filtered == "" and is_verified_filtered == "":
        #     filter_dict = {'type': type_filtered,
        #                    'donate_type': donate_type_filtered}
        # elif not type_filtered == "" and priority_filtered == "" and status_filtered == "" and donate_type_filtered == "" and not is_verified_filtered == "":
        #     filter_dict = {'type': type_filtered,
        #                    'is_verified': is_verified_filtered}

        # # Priority
        # # elif type_filtered == "" and not priority_filtered == "" and status_filtered == "" and donate_type_filtered == "" and is_verified_filtered == "":
        # #     filter_dict = {'type': type_filtered,
        # #                    'priority': priority_filtered}
        # elif type_filtered == "" and not priority_filtered == "" and not status_filtered == "" and donate_type_filtered == "" and is_verified_filtered == "":
        #     filter_dict = {'priority': priority_filtered,
        #                    'donation_progress__progress_status': status_filtered}
        # elif type_filtered == "" and not priority_filtered == "" and status_filtered == "" and not donate_type_filtered == "" and is_verified_filtered == "":
        #     filter_dict = {'priority': priority_filtered,
        #                    'donate_type': donate_type_filtered}
        # elif type_filtered == "" and not priority_filtered == "" and status_filtered == "" and donate_type_filtered == "" and not is_verified_filtered == "":
        #     filter_dict = {'priority': priority_filtered,
        #                    'is_verified': is_verified_filtered}

        # # Status
        # elif type_filtered == "" and not priority_filtered == "" and not status_filtered == "" and donate_type_filtered == "" and is_verified_filtered == "":
        #     filter_dict = {'donation_progress__progress_status': status_filtered,
        #                    'priority': priority_filtered}
        # # elif type_filtered == "" and priority_filtered == "" and not status_filtered == "" and donate_type_filtered == "" and is_verified_filtered == "":
        # #     filter_dict = {'type': type_filtered,
        # #                    'donation_progress__progress_status': status_filtered}
        # elif type_filtered == "" and priority_filtered == "" and not status_filtered == "" and not donate_type_filtered == "" and is_verified_filtered == "":
        #     filter_dict = {'donation_progress__progress_status': status_filtered,
        #                    'donate_type': donate_type_filtered}
        # elif type_filtered == "" and priority_filtered == "" and not status_filtered == "" and donate_type_filtered == "" and not is_verified_filtered == "":
        #     filter_dict = {'donation_progress__progress_status': status_filtered,
        #                    'is_verified': is_verified_filtered}

        # # Donate Type
        # elif type_filtered == "" and not priority_filtered == "" and status_filtered == "" and not donate_type_filtered == "" and is_verified_filtered == "":
        #     filter_dict = {'donate_type': donate_type_filtered,
        #                    'priority': priority_filtered}
        # elif type_filtered == "" and priority_filtered == "" and not status_filtered == "" and not donate_type_filtered == "" and is_verified_filtered == "":
        #     filter_dict = {'donate_type': donate_type_filtered,
        #                    'donation_progress__progress_status': status_filtered}
        # # elif not type_filtered == "" and priority_filtered == "" and status_filtered == "" and not donate_type_filtered == "" and is_verified_filtered == "":
        # #     filter_dict = {'type': type_filtered,
        # #                    'donate_type': donate_type_filtered}
        # elif type_filtered == "" and priority_filtered == "" and status_filtered == "" and not donate_type_filtered == "" and not is_verified_filtered == "":
        #     filter_dict = {'donate_type': donate_type_filtered,
        #                    'is_verified': is_verified_filtered}

        # # Is Verified
        # elif type_filtered == "" and not priority_filtered == "" and status_filtered == "" and donate_type_filtered == "" and not is_verified_filtered == "":
        #     filter_dict = {'is_verified': is_verified_filtered,
        #                    'priority': priority_filtered}
        # elif type_filtered == "" and priority_filtered == "" and not status_filtered == "" and donate_type_filtered == "" and not is_verified_filtered == "":
        #     filter_dict = {'is_verified': is_verified_filtered,
        #                    'donation_progress__progress_status': status_filtered}
        # elif type_filtered == "" and priority_filtered == "" and status_filtered == "" and not donate_type_filtered == "" and not is_verified_filtered == "":
        #     filter_dict = {'is_verified': is_verified_filtered,
        #                    'donate_type': donate_type_filtered}

        # ## More Than Two Chain
        # elif not type_filtered == "" and not priority_filtered == "" and not status_filtered == "" and donate_type_filtered == "" and is_verified_filtered == "":
        #     filter_dict = {'type': type_filtered,
        #                    'priority': priority_filtered, 'donation_progress__progress_status': status_filtered}
        # elif not type_filtered == "" and not priority_filtered == "" and not status_filtered == "" and not donate_type_filtered == "" and is_verified_filtered == "":
        #     filter_dict = {'type': type_filtered,
        #                    'priority': priority_filtered, 'donation_progress__progress_status': status_filtered,
        #                    'donate_type': donate_type_filtered}
        # elif not type_filtered == "" and priority_filtered == "" and not status_filtered == "" and not donate_type_filtered == "" and not is_verified_filtered == "":
        #     filter_dict = {'type': type_filtered,
        #                    'is_verified': is_verified_filtered, 'donation_progress__progress_status': status_filtered,
        #                    'donate_type': donate_type_filtered}
        # #
        # elif type_filtered == "" and priority_filtered == "" and not status_filtered == "" and not donate_type_filtered == "" and not is_verified_filtered == "":
        #     filter_dict = {'is_verified': is_verified_filtered, 'donation_progress__progress_status': status_filtered,
        #                    'donate_type': donate_type_filtered}
        # elif type_filtered == "" and not priority_filtered == "" and status_filtered == "" and not donate_type_filtered == "" and not is_verified_filtered == "":
        #     filter_dict = {'priority': priority_filtered,
        #                    'is_verified': is_verified_filtered, 'donate_type': donate_type_filtered}
        # elif not type_filtered == "" and priority_filtered == "" and status_filtered == "" and not donate_type_filtered == "" and not is_verified_filtered == "":
        #     filter_dict = {'type': type_filtered,
        #                    'is_verified': is_verified_filtered, 'donate_type': donate_type_filtered}
        # elif type_filtered == "" and priority_filtered == "" and not status_filtered == "" and not donate_type_filtered == "" and not is_verified_filtered == "":
        #     filter_dict = {'donation_progress__progress_status': status_filtered,
        #                    'is_verified': is_verified_filtered, 'donate_type': donate_type_filtered}
        # # 4 Chain
        # if type_filtered == "" and not priority_filtered == "" and not status_filtered == "" and not donate_type_filtered == "" and not is_verified_filtered == "":
        #     filter_dict = {'priority': priority_filtered, 'donate_type': donate_type_filtered, 'is_verified': is_verified_filtered,
        #                    'donation_progress__progress_status': status_filtered}
        # if not type_filtered == "" and priority_filtered == "" and not status_filtered == "" and not donate_type_filtered == "" and not is_verified_filtered == "":
        #     filter_dict = {'type': type_filtered, 'donate_type': donate_type_filtered, 'is_verified': is_verified_filtered,
        #                    'donation_progress__progress_status': status_filtered}
        # # 5 Chain
        # if not type_filtered == "" and not priority_filtered == "" and not status_filtered == "" and not donate_type_filtered == "" and not is_verified_filtered == "":
        #     filter_dict = {'type': type_filtered, 'priority': priority_filtered, 'donate_type': donate_type_filtered, 'is_verified': is_verified_filtered,
        #                    'donation_progress__progress_status': status_filtered}
        # else:
        #     filter_dict = {'publication_status': 0}
        if query is not None:
            if request.user.is_superuser:
                qs = Donation.objects.search(
                    query).filter(**filter_dict).filter(category=cat)
            else:
                qs = Donation.objects.search(
                    query).filter(**filter_dict).filter(category=cat).living_donates().is_verified()
        else:
            if request.user.is_superuser:
                qs = Donation.objects.filter(
                    **filter_dict).filter(category=cat)
            else:
                qs = Donation.objects.filter(
                    **filter_dict).filter(category=cat).living_donates().is_verified()
        # filter_dict = {'subcat__id__in': [1, 3, 5]}
        # print(filter_dict.get('priority'))
        # for key, value in filter_dict.items():
        #     if value is not None and not value == "":
        #         qs = Donation.objects.search(
        #             query).filter(**{key: value}).filter(category=cat)
        #         print(qs)
        # if query is not None:
        # if type_filtered is not None and not type_filtered == "":
        # variable_column = 'name'
        # search_type = 'contains'
        # filter = variable_column + '__' + search_type
        # info = Donation.objects.search(
        #     query).filter(**{filter: search_string})
        return qs


@method_decorator(decorators, name='dispatch')
class ManageProgressStatus(UpdateView):
    template_name = 'donations/manage-progress-status.html'
    form_class = DonationProgressForm

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        qs = DonationProgress.objects.filter(donation__slug=slug)
        if qs.exists():
            return qs.first()
        return None

    def form_valid(self, form):
        self.object = self.get_object()
        if self.object.donation.category == 0 and not self.request.user.is_superuser:
            if not self.request.user == self.object.donation.user.user and not self.request.user.is_superuser:
                respondent_fake = form.cleaned_data['respondent_fake']
                # print(respondent_fake)
                respondent_qs = DonationRespond.objects.filter(
                    donation=self.object.donation, respondent=self.request.user
                        )
                respondent_qs.update(is_applied_for_selection=True)
                # form.instance.progress_status = 0
                self.object.respondent.add(respondent_qs.first())
                form.instance.management_status = 0
                messages.add_message(self.request, messages.SUCCESS,
                                        f"Donation Progress Status has been updated successfully! Status is pending for {self.object.donation.user.get_smallname()}'s approval.'")
            else:
                # respondents = form.instance.respondent_set
                respondents = form.cleaned_data['respondent']
                # print(respondents)
                for respondent in respondents:
                    if not self.request.user.is_superuser:
                        respondent_qs = DonationRespond.objects.filter(
                            donation=self.object.donation, is_applied_for_selection=True,
                            respondent=respondent.respondent
                        )
                        if respondent_qs.exists():
                            respondent_qs.update(is_selected=True)
                        else:
                            form.instance.progress_status = 0
                    else:
                        respondent_qs = DonationRespond.objects.filter(
                            donation=self.object.donation,
                            respondent=respondent.respondent
                        )
                    if respondent_qs.exists():
                        respondent_qs.update(is_selected=True)
                messages.add_message(self.request, messages.SUCCESS,
                                     "Donation Progress Status has been updated successfully!")
        else:
            respondents = form.cleaned_data['respondent']
            for respondent in respondents:
                    respondent_qs = DonationRespond.objects.filter(
                        donation=self.object.donation,
                        respondent=respondent.respondent
                    )
                    if respondent_qs.exists():
                        respondent_qs.update(is_selected=True)
            messages.add_message(self.request, messages.SUCCESS,
                                    "Donation Progress Status has been updated successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        self.object = self.get_object()
        if self.object.donation.category == 0:
            if self.request.user.is_superuser:
                return reverse('donations:donation_offers_list')
            elif not self.object.donation.user.user == self.request.user and not self.request.user.is_superuser:
                return reverse('donations:my_responds')
            else:
                return reverse('donations:my_donation_offers')
        else:
            if self.request.user.is_superuser:
                return reverse('donations:donation_requests_list')
            else:
                return reverse('donations:my_donation_requests')
        return reverse('home')

    def get_form_kwargs(self):
        kwargs = super(ManageProgressStatus, self).get_form_kwargs()
        if self.form_class:
            kwargs.update({'request': self.request})
            kwargs.update({'object': self.get_object()})
        return kwargs

    def user_passes_test(self, request):
        if request.user.is_authenticated:
            self.object = self.get_object()
            if self.object.donation.donate_type == 0:
                if self.object.donation.category == 1:
                    if self.object.donation.user.user == self.request.user or self.request.user.is_superuser:
                        return True
                else:
                    respondent_qs = DonationRespond.objects.filter(
                        donation=self.object.donation, respondent=self.request.user
                    )
                    if respondent_qs.exists() or self.object.donation.user.user == self.request.user or self.request.user.is_superuser:
                        return True
            else:
                if self.request.user.is_superuser:
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
        return context


@method_decorator(decorators, name='dispatch')
class MyRespondsListView(AjaxListView):
    template_name = 'donations/donation-list-card.html'
    page_template = 'donations/snippets/page_template_list.html'

    def get_queryset(self):
        qs = DonationRespond.objects.filter(respondent=self.request.user)
        if qs.exists():
            return qs
        return None

    def get_context_data(self, **kwargs):
        context = super(MyRespondsListView,
                        self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        context['page_title'] = "My Responds"
        context['can_filter'] = False
        context['page_type'] = "RESPOND"
        return context
