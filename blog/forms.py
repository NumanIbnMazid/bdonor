from django import forms
from django.contrib.auth.models import User
from django.template.defaultfilters import filesizeformat
import datetime
import re
import os
from ckeditor.widgets import CKEditorWidget
from .models import Blog, Attachment
from .fields import MultiFileField, MultiMediaField, MultiImageField


class BlogManageForm(forms.ModelForm):
    # attachments_fake = forms.FileField(required=False, label="Attachments")
    attachments_fake = MultiFileField(
        min_num=1, max_num=3, max_file_size=1024*1024*5, required=False)
    def __init__(self, *args, **kwargs):
        super(BlogManageForm, self).__init__(*args, **kwargs)
        self.fields['title'].help_text = "Enter blog title..."
        self.fields['title'].widget.attrs.update({
            'id': 'blog_title_input',
            'placeholder': 'Give blog title...',
            'maxlength': 150,
            'pattern': "^[_A-z0-9 +-.,#]{1,}$",
        })
        self.fields['attachments_fake'].label = "Attachments"
        self.fields['attachments_fake'].help_text = "Select attachments..."
        self.fields['attachments_fake'].widget.attrs.update({
            'id': 'blog_attachments_fake_input',
            'multiple': True,
        })
        self.fields['details'].help_text = "Enter details..."
        self.fields['details'].widget.attrs.update({
            'id': 'blog_details_input',
            'placeholder': 'Enter details...',
            'rows': 4,
            'cols': 2,
        })

    class Meta:
        model = Blog
        fields = ['title', 'attachments_fake', 'details']
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
