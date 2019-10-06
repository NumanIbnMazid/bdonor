from django.shortcuts import render
from .models import Suspicious
from django.views.generic import UpdateView, DetailView, ListView, CreateView
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from .utils import block_suspicious_user


@method_decorator(login_required, name='dispatch')
class SuspiciousListView(ListView):
    template_name = 'suspicious/list.html'

    def get_queryset(self):
        qs = Suspicious.objects.all()
        return qs

    def get_context_data(self, **kwargs):
        context = super(SuspiciousListView,
                        self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        context['page_title'] = "Suspicious User's List"
        return context

    def user_passes_test(self, request):
        if request.user.is_superuser:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(SuspiciousListView, self).dispatch(request, *args, **kwargs)
