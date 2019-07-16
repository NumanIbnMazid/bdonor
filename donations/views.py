from django.shortcuts import render
# model imports
from .models import Donation, DonationProgress, DonationRespond
from accounts.models import UserProfile
from utils.models import Notification
# generic view imports
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
# other imports
from .forms import DonationForm, DonationRespondForm
from utils.handlers import create_notification
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django import forms
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from el_pagination.views import AjaxListView
from suspicious.utils import block_suspicious_user
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
import zeep
from zeep import Client
from django.contrib.sites.models import Site
# Site.objects.get_current().domain


@method_decorator(login_required, name='dispatch')
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
        elif type == 1:
            finalized_type = "Organ"
            if form.instance.organ_name == "Heart":
                form.instance.quantity = 1
            if form.instance.organ_name == "Liver":
                form.instance.quantity = 1
        elif type == 2:
            finalized_type = "Tissue"
        else:
            finalized_type = "Undefined"
        form.instance.title = f"I want to donate {finalized_type}"
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
            if type == 0 and blood_group == None:
                form.add_error(
                    'blood_group', forms.ValidationError(
                        "You must select blood group."
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
                messages.add_message(self.request, messages.SUCCESS,
                                     "Your donation offer has been created successfully!")
                return super().form_valid(form)
        return super().form_invalid(form)

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
        context['page_title'] = "Create donation offer"
        last_blood_donated_filter = DonationProgress.objects.filter(
            donation__user=self.request.user.profile, donation__category=0, donation__type=0,
            progress_status=1
        )
        can_donate_blood = True
        if last_blood_donated_filter.exists():
            if not last_blood_donated_filter.last().completion_date == None:
                day_difference = datetime.datetime.now(
                ) - last_blood_donated_filter.last().completion_date
                if day_difference.days < 90:
                    can_donate_blood = False
                    context['last_donated_ago'] = day_difference.days
                    context['waiting_days_remaining'] = 90 - int(day_difference.days)
                    context['last_donated_object'] = last_blood_donated_filter.last()
        context['can_donate_blood'] = can_donate_blood
        return context


@method_decorator(login_required, name='dispatch')
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
        elif type == 1:
            finalized_type = "Organ"
            if form.instance.organ_name == "Heart":
                form.instance.quantity = 1
            if form.instance.organ_name == "Liver":
                form.instance.quantity = 1
        elif type == 2:
            finalized_type = "Tissue"
        else:
            finalized_type = "Undefined"
        form.instance.title = f"I want to donate {finalized_type}"
        if self.object.category == 0 and type == 0:
            form.instance.blood_bag = 1
        blood_group = form.instance.blood_group
        blood_bag = form.instance.blood_bag
        # organ_name = form.instance.organ_name
        details = form.instance.details
        details_fake = form.cleaned_data['details_fake']
        contact = form.instance.contact
        contact2 = form.instance.contact2
        contact3 = form.instance.contact3
        contact_privacy = self.request.POST.get("contact_privacy")
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
            if type == 0 and blood_group == None:
                form.add_error(
                    'blood_group', forms.ValidationError(
                        "You must select blood group."
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
                # form.instance.category = category
                messages.add_message(self.request, messages.SUCCESS,
                                     "Your donation offer has been updated successfully!")
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
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(OfferDonationUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('donations:my_donation_offers')

    def get_context_data(self, **kwargs):
        context = super(OfferDonationUpdateView,
                        self).get_context_data(**kwargs)
        context['page_title'] = "Update donation offer"
        last_blood_donated_filter = DonationProgress.objects.filter(
            donation__user=self.request.user.profile, donation__category=0, donation__type=0,
            progress_status=1
        )
        can_donate_blood = True
        if last_blood_donated_filter.exists():
            if not last_blood_donated_filter.last().completion_date == None:
                day_difference = datetime.datetime.now(
                ) - last_blood_donated_filter.last().completion_date
                if day_difference.days < 90:
                    can_donate_blood = False
                    context['last_donated_ago'] = day_difference.days
                    context['waiting_days_remaining'] = 90 - \
                        int(day_difference.days)
                    context['last_donated_object'] = last_blood_donated_filter.last()
        context['can_donate_blood'] = can_donate_blood
        return context


@csrf_exempt
@login_required
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


@method_decorator(login_required, name='dispatch')
class DonationOffersListView(AjaxListView):
    template_name = 'donations/donation-list.html'
    page_template = 'donations/snippets/page_template_list.html'

    def get_queryset(self):
        qs = Donation.objects.all().offers().latest().is_published()
        if qs.exists():
            return qs
        return None

    def get_context_data(self, **kwargs):
        context = super(DonationOffersListView,
                        self).get_context_data(**kwargs)
        context['page_title'] = "Donation Offers"
        return context


@method_decorator(login_required, name='dispatch')
class MyDonationOffersListView(AjaxListView):
    template_name = 'donations/donation-list.html'
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
        context['page_title'] = "My Offers"
        return context


@method_decorator(login_required, name='dispatch')
class DonationDetailView(DetailView):
    template_name = 'donations/donation-details.html'

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        return Donation.objects.get_by_slug(slug, self.request)

    def get_context_data(self, **kwargs):
        context = super(DonationDetailView, self).get_context_data(**kwargs)
        context['page_title'] = "Donation Details"
        return context


class DonationRespondCreateView(CreateView):
    template_name = 'donations/respond.html'
    form_class = DonationRespondForm

    # def get_object(self, *args, **kwargs):
    #     slug = self.kwargs.get('slug')
    #     return Donation.objects.get_by_slug(slug, self.request)

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
            respondent = self.request.user.profile.get_dynamic_name()
            respondent_receiver = donation.user.get_dynamic_name()
            receiver_email = donation.user.user.email
            receiver_contact = donation.contact
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
            mail_from = 'admin@bdonar.com'
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
            receiver = donation.user.user
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
        slug = self.kwargs.get('slug')
        donation = Donation.objects.get_by_slug(slug, self.request)
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
                day_difference = datetime.datetime.now(
                ) - last_blood_donated_filter.last().completion_date
                if day_difference.days < 90:
                    can_donate_blood = False
                    context['last_donated_ago'] = day_difference.days
                    context['waiting_days_remaining'] = 90 - \
                        int(day_difference.days)
                    context['last_donated_object'] = last_blood_donated_filter.last()
        context['can_donate_blood'] = can_donate_blood
        return context


@csrf_exempt
@login_required
def withdraw_respond(request):
    url = reverse('home')
    user = request.user
    if request.method == "POST":
        slug = request.POST.get("slug")
        qs = DonationRespond.objects.filter(donation__slug=slug, respondent=user)
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
