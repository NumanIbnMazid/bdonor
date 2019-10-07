from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from django.views.generic.edit import FormMixin

from django.views.generic import DetailView, ListView

from .forms import ComposeForm
from .models import Thread, ChatMessage
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Custom Decorators Starts
from accounts.decorators import (
    can_browse_required, can_donate_required, can_ask_for_a_donor_required,
    can_manage_bank_required, can_chat_required
)
# Custom Decorators Ends

decorators = [can_browse_required]


@method_decorator(decorators, name='dispatch')
class InboxView(LoginRequiredMixin, ListView):
    template_name = 'chat/inbox.html'

    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super(InboxView, self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        return context


@method_decorator(decorators, name='dispatch')
class ThreadView(LoginRequiredMixin, FormMixin, DetailView):
    template_name = 'chat/thread.html'
    form_class = ComposeForm
    success_url = './'

    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

    def get_object(self):
        other_username = self.kwargs.get("username")
        if not self.request.user.username == other_username:
            obj, created = Thread.objects.get_or_new(
                self.request.user, other_username)
            qs = ChatMessage.objects.filter(
                ~Q(user=self.request.user) & Q(thread=obj))
            if qs.exists():
                qs.update(is_seen=True)
            if obj == None:
                raise Http404
            return obj
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        thread = self.get_object()
        user = self.request.user
        message = form.cleaned_data.get("message")
        ChatMessage.objects.create(user=user, thread=thread, message=message)
        return super().form_valid(form)

    def user_passes_test(self, request):
        other_username = self.kwargs.get("username")
        if not self.request.user.username == other_username:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            messages.add_message(self.request, messages.INFO,
                                 "You cannot chat with yourself!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return super(ThreadView, self).dispatch(request, *args, **kwargs)
