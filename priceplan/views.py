from django.shortcuts import render
from .models import Plan
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.contrib import messages
from django import forms
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from suspicious.utils import block_suspicious_user
from django.views.decorators.csrf import csrf_exempt
import datetime
from .forms import PlanForm
from suspicious.models import Suspicious


@method_decorator(login_required, name='dispatch')
class PlanCreateView(CreateView):
    template_name = 'priceplan/manage.html'
    form_class = PlanForm

    def form_valid(self, form):
        title = form.instance.title
        qs = Plan.objects.filter(
            title__iexact=title)
        if qs.exists():
            form.add_error(
                'title', forms.ValidationError(
                    "This Plan is alreay exists!"
                )
            )
            return super().form_invalid(form)
        else:
            messages.add_message(self.request, messages.SUCCESS,
                                 "Price plan has been created successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('priceplan:plan_create')

    def get_context_data(self, **kwargs):
        context = super(PlanCreateView,
                        self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        context['page_title'] = "Create Price Plan"
        context['object_list'] = Plan.objects.all().order_by('-created_at')
        return context

    def user_passes_test(self, request):
        if request.user.is_superuser:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(PlanCreateView, self).dispatch(request, *args, **kwargs)


@csrf_exempt
@login_required
def priceplan_delete(request):
    url = reverse('home')
    if request.method == "POST":
        slug = request.POST.get("slug")
        qs = Plan.objects.filter(slug=slug)
        if qs.exists():
            if request.user.is_superuser:
                qs.delete()
                messages.add_message(request, messages.SUCCESS,
                                     "Price plan has been deleted successfully!")
                url = reverse('priceplan:plan_create')
            else:
                block_suspicious_user(request)
        else:
            messages.add_message(request, messages.WARNING,
                                 "Not found!")
    return HttpResponseRedirect(url)


@method_decorator(login_required, name='dispatch')
class PlanDetailView(DetailView):
    template_name = 'priceplan/details.html'

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        qs = Plan.objects.filter(slug=slug)
        if qs.exists():
            return qs.first()
        return None

    def get_context_data(self, **kwargs):
        context = super(PlanDetailView, self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        context['page_title'] = "Plan Details"
        context['object_list'] = Plan.objects.all().order_by('-created_at')
        return context

    def user_passes_test(self, request):
        if request.user.is_superuser:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(PlanDetailView, self).dispatch(request, *args, **kwargs)


class PlanUpdateView(UpdateView):
    template_name = 'priceplan/manage.html'
    form_class = PlanForm

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        qs = Plan.objects.filter(slug=slug)
        if qs.exists():
            return qs.first()
        return None

    def form_valid(self, form):
        self.object = self.get_object()
        title = form.instance.title
        if not title == self.object.title:
            qs = Plan.objects.filter(
                title__iexact=title)
            if qs.exists():
                form.add_error(
                    'title', forms.ValidationError(
                        "This Plan is alreay exists!"
                    )
                )
                return super().form_invalid(form)
            # else:
            #     messages.add_message(self.request, messages.SUCCESS,
            #                          "Price Plan has been updated successfully!")
        messages.add_message(self.request, messages.SUCCESS,
                             "Price Plan has been updated successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        self.object = self.get_object()
        return reverse('priceplan:plan_details', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super(PlanUpdateView,
                        self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        context['page_title'] = "Update Plan"
        context['object_list'] = Plan.objects.all().order_by('-created_at')
        return context
    
    def user_passes_test(self, request):
        if request.user.is_superuser:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(PlanUpdateView, self).dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class PricePlanListView(ListView):
    template_name = 'priceplan/priceplans.html'

    def get_queryset(self):
        qs = Plan.objects.all()
        if qs.exists():
            return qs
        return None

    def get_context_data(self, **kwargs):
        context = super(PricePlanListView, self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        return context
