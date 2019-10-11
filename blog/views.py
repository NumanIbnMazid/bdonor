from django.views.generic import TemplateView, CreateView, UpdateView, View, DetailView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from el_pagination.decorators import page_template
from django.urls import reverse
from django.contrib import messages
from django import forms
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from .forms import BlogManageForm
from .models import Blog, Attachment
# Custom Decorators Starts
from accounts.decorators import (
    can_browse_required, can_donate_required, can_ask_for_a_donor_required,
    can_manage_bank_required, can_chat_required
)
# Custom Decorators Ends

decorators = [login_required, can_browse_required]



@method_decorator(decorators, name='dispatch')
class BlogPostCreateView(CreateView):
    template_name = 'blog/index.html'
    form_class = BlogManageForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        # print(self.object)
        if not form.cleaned_data['attachments_fake'] == None:
            for field in self.request.FILES.keys():
                for formfile in self.request.FILES.getlist(field):
                    file = Attachment(file=formfile,
                                      blog=self.object)
                    file.save()
        messages.add_message(self.request, messages.SUCCESS,
            "Blog post has been created successfully!"
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:blog_post_create')

    def get_context_data(self, **kwargs):
        context = super(BlogPostCreateView,
                        self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        context['page_title'] = "Create Blog Post"
        context['object_list'] = Blog.objects.all().order_by(
            '-created_at')
        return context

