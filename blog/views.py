from django.views.generic import TemplateView, CreateView, UpdateView, View, DetailView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from el_pagination.decorators import page_template
from django.urls import reverse
from django.contrib import messages
from django import forms
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
import os
from el_pagination.views import AjaxListView
from django.conf import settings
from django.template.defaultfilters import filesizeformat
from suspicious.utils import block_suspicious_user
from django.views.decorators.csrf import csrf_exempt
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
    template_name = 'blog/manage.html'
    form_class = BlogManageForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        # print(self.object)
        if not form.cleaned_data['file'] == None:
            for field in self.request.FILES.keys():
                for formfile in self.request.FILES.getlist(field):
                    file = Attachment(file=formfile,
                                      blog=self.object)
                    file.save()
            # for field in self.request.FILES.keys():
            #     for formfile in self.request.FILES.getlist(field):
            #         file_extension = os.path.splitext(formfile.name)[1]
            #         allowed_file_types = settings.ALLOWED_FILE_TYPES
            #         content_type = formfile.content_type.split('/')[0]
            #         if not file_extension in allowed_file_types:
            #             form.add_error(
            #                 'file', forms.ValidationError(
            #                     f"Only {allowed_file_types} file formats are supported! Current file format is {file_extension}"
            #                 )
            #             )
            #         elif formfile.size > settings.MAX_UPLOAD_SIZE:
            #             form.add_error(
            #                 'file', forms.ValidationError(
            #                     f"Please keep filesize under {filesizeformat(settings.MAX_UPLOAD_SIZE)}. Current filesize {filesizeformat(formfile.size)}"
            #                 )
            #             )
            #         else:
            #             file = Attachment(file=formfile,
            #                             blog=self.object)
            #             file.save()
            messages.add_message(self.request, messages.SUCCESS,
                "Blog post has been created successfully!"
            )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:blog_post_create')

    def get_form_kwargs(self):
        kwargs = super(BlogPostCreateView, self).get_form_kwargs()
        if self.form_class:
            kwargs.update({'request': self.request})
            kwargs.update({'object': None})
        return kwargs

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
        return context


@method_decorator(decorators, name='dispatch')
class BlogAjaxListView(AjaxListView):
    template_name = 'blog/list.html'
    page_template = 'snippets/common/ajax_list_page.html'
    # paginate_by = 3

    def get_queryset(self):
        qs = Blog.objects.all()
        return qs

    def get_context_data(self, **kwargs):
        context = super(BlogAjaxListView, self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        context['page_title'] = "All Blog Posts"
        context['include_template_var'] = "blog/snippets/blog-card.html"
        context['add_url'] = "blog:blog_post_create"
        return context


@method_decorator(decorators, name='dispatch')
class BlogDetailView(DetailView):
    template_name = 'blog/detail.html'

    def get_object(self):
        qs = Blog.objects.filter(slug=self.kwargs['slug'])
        if qs.exists():
            return qs.first()
        return None

    def get_context_data(self, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        context['page_title'] = "Post Details"
        host = self.request.META['HTTP_HOST']
        if self.request.is_secure():
            scheme = "https://"
        else:
            scheme = "http://"
        context['domain'] = f"{scheme}{host}"
        return context


@method_decorator(decorators, name='dispatch')
class MyPostsAjaxListView(AjaxListView):
    template_name = 'blog/list.html'
    page_template = 'snippets/common/ajax_list_page.html'
    # paginate_by = 3

    def get_queryset(self):
        qs = Blog.objects.filter(user=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super(MyPostsAjaxListView, self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        context['page_title'] = "My Blog Posts"
        context['include_template_var'] = "blog/snippets/blog-card.html"
        context['add_url'] = "blog:blog_post_create"
        return context


@method_decorator(decorators, name='dispatch')
class BlogPostUpdateView(UpdateView):
    template_name = 'blog/manage.html'
    form_class = BlogManageForm

    def get_object(self):
        qs = Blog.objects.filter(slug=self.kwargs['slug'])
        if qs.exists():
            return qs.first()
        return None

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        if not form.cleaned_data['file'] == None:
            for field in self.request.FILES.keys():
                for formfile in self.request.FILES.getlist(field):
                    file = Attachment(file=formfile,
                                      blog=self.object)
                    file.save()
            messages.add_message(self.request, messages.SUCCESS,
                                 "Blog post has been updated successfully!"
                                 )
        return super().form_valid(form)

    def get_success_url(self):
        self.object = self.get_object()
        return reverse('blog:blog_detail', kwargs={'slug': self.object.slug})

    def get_form_kwargs(self):
        kwargs = super(BlogPostUpdateView, self).get_form_kwargs()
        if self.form_class:
            kwargs.update({'request': self.request})
            kwargs.update({'object': self.get_object()})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(BlogPostUpdateView,
                        self).get_context_data(**kwargs)
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        # Ends Base Template Context
        context['page_title'] = "Update Blog Post"
        host = self.request.META['HTTP_HOST']
        if self.request.is_secure():
            scheme = "https://"
        else:
            scheme = "http://"
        context['domain'] = f"{scheme}{host}"
        # Attachment
        self.object = self.get_object()
        attach_qs = Attachment.objects.filter(blog=self.object)
        upload_remaining = 3
        if attach_qs.exists():
            upload_remaining = upload_remaining - attach_qs.count()
        context['upload_remaining'] = upload_remaining
        print(upload_remaining)
        return context

    def user_passes_test(self, request):
        if request.user.is_authenticated:
            self.object = self.get_object()
            if self.object.user == self.request.user:
                return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            block_suspicious_user(request)
            return HttpResponseRedirect(reverse('home'))
        return super(BlogPostUpdateView, self).dispatch(request, *args, **kwargs)


@csrf_exempt
@login_required
@can_browse_required
def delete_attachment(request):
    url = reverse('home')
    user = request.user
    if request.method == "POST":
        slug = request.POST.get("slug")
        qs = Attachment.objects.filter(slug=slug)
        if qs.exists():
            obj = qs.first()
            qs.delete()
            messages.add_message(request, messages.SUCCESS,
                                 "Attachment deleted successfully!")
            url = reverse('blog:blog_update',
                          kwargs={'slug': obj.blog.slug})
        else:
            messages.add_message(request, messages.WARNING,
                                 "Something went wrong!")
    return HttpResponseRedirect(url)


@csrf_exempt
@login_required
@can_browse_required
def blog_delete(request):
    url = reverse('home')
    user = request.user
    if request.method == "POST":
        slug = request.POST.get("slug")
        qs = Blog.objects.filter(slug=slug)
        if qs.exists():
            qs.delete()
            messages.add_message(request, messages.SUCCESS,
                                 "Blog Post has been deleted successfully!")
            url = reverse('blog:blog_my_posts_list')
        else:
            messages.add_message(request, messages.WARNING,
                                 "Something went wrong!")
    return HttpResponseRedirect(url)
