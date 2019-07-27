from django.shortcuts import render
from django.views.generic import UpdateView, DetailView, ListView
from .models import UserProfile
from suspicious.utils import block_suspicious_user
from .forms import UserProfileUpdateForm
from django import forms
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from el_pagination.views import AjaxListView


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
            base_template = 'admin/base.html'
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
            base_template = 'admin/base.html'
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
        contact = form.instance.contact
        # print(f"XXX___{contact}")
        contactFake = self.request.POST.get("contact_fake")
        # Save the form
        if contact is not "":
            form.instance.contact = contactFake + contact
        messages.add_message(self.request, messages.SUCCESS,
                             "Your profile has been updated successfully !")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin/base.html'
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
