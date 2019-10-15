from django import forms
from django.contrib.auth.models import User
from django.template.defaultfilters import filesizeformat
import datetime
import re
import os
from django.conf import settings
from ckeditor.widgets import CKEditorWidget
from .models import Blog, Attachment
from .fields import MultiFileField, MultiMediaField, MultiImageField
from django.http import Http404

class AttachmentForm(forms.ModelForm):
    # attachments_fake = MultiFileField(
    #     min_num=1, max_num=3, max_file_size=1024*1024*5, required=False)
    def __init__(self, *args, **kwargs):
        super(AttachmentForm, self).__init__(*args, **kwargs)
        self.object = self.instance
        self.fields['file'] = forms.FileField(
            widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
        self.fields['file'].label = "Attachments"
        self.fields['file'].help_text = "Select attachments..."
        self.fields['file'].widget.attrs.update({
            'id': 'blog_file_input',
            'multiple': True,
        })
        # try:
        #     attach_qs = Attachment.objects.filter(blog=self.object)
        #     if attach_qs.exists() and attach_qs.count() >= 3:
        #         self.fields.pop("file")
        # # except Blog.DoesNotExist:
        # #     print("Not Found!")
        # except:
        #     pass
        #     # raise Http404("Something went wrong !!!")
    class Meta:
        model = Attachment
        fields = ['file']
        exclude = ['blog']

    # def clean_file(self):
    #     file = self.cleaned_data.get('file')
    #     if not file == None:
    #         file_extension = os.path.splitext(file.name)[1]
    #         allowed_file_types = settings.ALLOWED_FILE_TYPES
    #         content_type = file.content_type.split('/')[0]
    #         if not file_extension in allowed_file_types:
    #             raise forms.ValidationError("Only %s file formats are supported! Current file format is %s" % (
    #                 allowed_file_types, file_extension))
    #         if file.size > settings.MAX_UPLOAD_SIZE:
    #             raise forms.ValidationError("Please keep filesize under %s. Current filesize %s" % (
    #                 filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(file.size)))
    #     return file


class BlogManageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.object = kwargs.pop('object', None)
        attach_kwargs = kwargs.copy()
        attach_kwargs['instance'] = self.object
        self.attachment_form = AttachmentForm(*args, **attach_kwargs)
        super(BlogManageForm, self).__init__(*args, **kwargs)
        self.fields.update(self.attachment_form.fields)
        self.initial.update(self.attachment_form.initial)
        self.fields['title'].help_text = "Enter post title..."
        self.fields['title'].widget.attrs.update({
            'id': 'blog_title_input',
            'placeholder': 'Give post title...',
            'maxlength': 150,
            'pattern': "^[_A-z0-9 +-.,#]{1,}$",
        })
        self.fields['details'].help_text = "Enter details..."
        self.fields['details'].widget.attrs.update({
            'id': 'blog_details_input',
            'placeholder': 'Enter details...',
            'rows': 4,
            'cols': 2,
        })
        self.fields['tags'].help_text = "Enter related tags..."
        self.fields['tags'].widget.attrs.update({
            'id': 'blog_tags_input',
            'placeholder': 'Enter related tags...',
            'maxlength': 100,
            'pattern': "^[_A-z0-9 +-.,#]{1,}$",
        })

    class Meta:
        model = Blog
        fields = ['title', 'details', 'tags']
        exclude = ['user', 'slug', 'created_at', 'updated_at']
        widgets = {
            'details': CKEditorWidget(),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title == None:
            allowed_chars = re.match(r'^[_A-z0-9 +-.,#]+$', title)
            length = len(title)
            if not allowed_chars:
                raise forms.ValidationError(
                    "Only '_A-z0-9+-.,#' these characters and spaces are allowed.")
            if length > 150:
                raise forms.ValidationError(
                    f"Maximum 150 characters allowed. [currently using: {length}]")
        return title

    def clean_details(self):
        details = self.cleaned_data.get('details')
        if not details == None:
            length = len(details)
            if length > 5000:
                raise forms.ValidationError(
                    f"Maximum 5000 characters allowed. [currently using: {length}]")
        return details

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        if not tags == None:
            allowed_chars = re.match(r'^[_A-z0-9 +-.,#]+$', tags)
            length = len(tags)
            if not allowed_chars:
                raise forms.ValidationError(
                    "Only '_A-z0-9+-.,#' these characters and spaces are allowed.")
            if length > 100:
                raise forms.ValidationError(
                    f"Maximum 100 characters allowed. [currently using: {length}]")
        return tags
