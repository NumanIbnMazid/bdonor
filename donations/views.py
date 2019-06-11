from django.shortcuts import render
# model imports
from .models import Donation, DonationProgress
from accounts.models import UserProfile
# generic view imports
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
# other imports
from .forms import DonationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django import forms
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from el_pagination.views import AjaxListView
from suspicious.utils import block_suspicious_user
from django.views.decorators.csrf import csrf_exempt


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
        blood_group = form.instance.blood_group
        blood_bag = form.instance.blood_bag
        organ_name = form.instance.organ_name
        details = form.instance.details
        details_fake = form.cleaned_data['details_fake']
        contact = form.instance.contact
        contact2 = form.instance.contact2
        contact3 = form.instance.contact3
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
            elif type == 0 and blood_bag == None:
                form.add_error(
                    'blood_bag', forms.ValidationError(
                        "You must enter required blood bag quantity."
                    )
                )
            elif type == 1 and organ_name == None:
                form.add_error(
                    'organ_name', forms.ValidationError(
                        "You must enter organ name."
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
        context = super(OfferDonationCreateView, self).get_context_data(**kwargs)
        context['page_title'] = "Create donation offer"
        return context



@method_decorator(login_required, name='dispatch')
class OfferDonationUpdateView(UpdateView):
    template_name = 'donations/donation-manage.html'
    form_class = DonationForm

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        return Donation.objects.get_by_slug(slug)

    def form_valid(self, form):
        category = 0
        type = form.instance.type
        blood_group = form.instance.blood_group
        blood_bag = form.instance.blood_bag
        organ_name = form.instance.organ_name
        details = form.instance.details
        details_fake = form.cleaned_data['details_fake']
        contact = form.instance.contact
        contact2 = form.instance.contact2
        contact3 = form.instance.contact3
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
            elif type == 0 and blood_bag == None:
                form.add_error(
                    'blood_bag', forms.ValidationError(
                        "You must enter required blood bag quantity."
                    )
                )
            elif type == 1 and organ_name == None:
                form.add_error(
                    'organ_name', forms.ValidationError(
                        "You must enter organ name."
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
            return self.object.user.user == request.user
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(OfferDonationUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('donations:my_donation_offers')

    def get_context_data(self, **kwargs):
        context = super(OfferDonationUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = "Update donation offer"
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
        context = super(DonationOffersListView, self).get_context_data(**kwargs)
        context['page_title'] = "Donation Offers"
        return context



@method_decorator(login_required, name='dispatch')
class MyDonationOffersListView(AjaxListView):
    template_name = 'donations/donation-list.html'
    page_template = 'donations/snippets/page_template_list.html'

    def get_queryset(self):
        qs = Donation.objects.all().donations_by_user(self.request.user).offers().latest()
        if qs.exists():
            return qs
        return None

    def get_context_data(self, **kwargs):
        context = super(MyDonationOffersListView, self).get_context_data(**kwargs)
        context['page_title'] = "My Offers"
        return context


@method_decorator(login_required, name='dispatch')
class DonationDetailView(DetailView):
    template_name = 'donations/donation-details.html'

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        return Donation.objects.get_by_slug(slug)

    def get_context_data(self, **kwargs):
        context = super(DonationDetailView, self).get_context_data(**kwargs)
        context['page_title'] = "Donation Details"
        return context