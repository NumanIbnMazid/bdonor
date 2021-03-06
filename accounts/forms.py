# from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, UserReport, UserPermission
from django.template.defaultfilters import filesizeformat
from django.conf import settings
import datetime
import re
import os
from ckeditor.widgets import CKEditorWidget


# class DateInput(forms.DateInput):
#     input_type = 'date'


# class CustomSignupForm(SignupForm):
#     def signup(self, request, user):
#         user.save()
#         userprofile, created = self.get_or_create(user=user)
#         user.userprofile.save()


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['last_name', 'first_name']


class UserProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # magic
        self.user = kwargs['instance'].user
        user_kwargs = kwargs.copy()
        user_kwargs['instance'] = self.user
        self.uf = UserForm(*args, **user_kwargs)
        # magic end

        super(UserProfileUpdateForm, self).__init__(*args, **kwargs)

        self.fields.update(self.uf.fields)
        self.initial.update(self.uf.initial)

        # self.fields.keyOrder = [
        #     'first_name',
        #     'last_name',
        #     'gender',
        #     'dob',
        #     'blood_group',
        #     'contact',
        #     'address',
        #     'about',
        #     'facebook',
        #     'linkedin',
        #     'website',
        #     'image',
        # ]

        self.fields['first_name'] = forms.CharField(required=False,
                                                    widget=forms.TextInput(attrs={'placeholder': 'Enter your first name...'}))
        self.fields['first_name'].widget.attrs.update({
            'id': 'profile_first_name',
            'maxlength': 15,
            'pattern': "^[A-Za-z.,\- ]{1,}$",
        })
        self.fields['last_name'] = forms.CharField(required=False,
                                                   widget=forms.TextInput(attrs={'placeholder': 'Enter your last name...'}))
        self.fields['last_name'].widget.attrs.update({
            'id': 'profile_last_name',
            'maxlength': 20,
            'pattern': "^[A-Za-z.,\- ]{1,}$"
        })
        self.fields['dob'].widget.attrs.update({
            'placeholder': 'Ex: 1996-02-27',
            'id': 'profile_dob',
        })
        self.fields['contact'] = forms.CharField(required=False,
                                                 widget=forms.TextInput())
        self.fields['contact'].widget.attrs.update({
            'id': 'profile_contact',
            'onkeyup': "resetMessage()",
            'maxlength': 20,
        })
        self.fields['address'].widget.attrs.update({
            'id': 'profile_address',
            'rows': 2,
            'cols': 2,
            'placeholder': 'Enter your address',
            'maxlength': 100
        })
        self.fields['city'].widget.attrs.update({
            'id': 'profile_city',
            'placeholder': 'Enter city...',
            'maxlength': 25,
        })
        self.fields['state'].widget.attrs.update({
            'id': 'profile_state',
            'placeholder': 'Enter state...',
            'maxlength': 25,
        })
        self.fields['country'].widget.attrs.update({
            'id': 'profile_country',
            'placeholder': 'Select country...',
            'maxlength': 25,
        })
        self.fields['facebook'].widget.attrs.update({
            'placeholder': 'Enter your facebook profile link...',
            'maxlength': 150
        })
        self.fields['linkedin'].widget.attrs.update({
            'placeholder': 'Enter your linkedin profile link...',
            'maxlength': 150
        })
        self.fields['website'].widget.attrs.update({
            'placeholder': 'Enter your website link...',
            'maxlength': 150
        })
        self.fields['about'] = forms.CharField(required=False, max_length=250,
                                               widget=forms.Textarea(attrs={'rows': 2, 'cols': 2, 'placeholder': 'Enter more about you...'}))
        # Help Texts
        self.fields['first_name'].help_text = "Maximum length 15 and only these 'A-Za-z.,-' characters and spaces are allowed."
        self.fields['last_name'].help_text = "Maximum length 20 and only these 'A-Za-z.,-' characters and spaces are allowed."
        self.fields['gender'].help_text = 'Enter your Gender.'
        self.fields['dob'].help_text = 'Enter your Date of Birth.'
        self.fields['dob'].label = "Date of Birth"
        self.fields['blood_group'].help_text = 'Enter your Blood Group.'
        self.fields['contact'].help_text = 'Phone number must be valid and start with +880'
        self.fields['address'].help_text = 'Enter your Address.'
        self.fields['city'].help_text = 'Enter your City.'
        self.fields['state'].help_text = 'Enter your State.'
        self.fields['country'].help_text = 'Select your Country.'
        self.fields['about'].help_text = 'Enter More About You.'
        self.fields['facebook'].help_text = 'Enter your Facebook Profile Link.'
        self.fields['linkedin'].help_text = 'Enter your Linkedin Profile Link.'
        self.fields['website'].help_text = 'Enter your Website Link.'
        self.fields[
            'image'].help_text = 'Enter your Profile Picture. Only JPEG/JPG/PNG Files (Maximum 1.5 MB) are allowed.'

    class Meta:
        model = UserProfile
        fields = ['about', 'website', 'linkedin', 'facebook', 'address', 'country',
                  'state', 'city', 'image', 'dob', 'contact', 'gender', 'blood_group']
        # fields = ['gender', 'dob', 'blood_group',
        #           'contact', 'image', 'address', 'about', 'facebook', 'linkedin', 'website']
        # exclude = ['user', 'slug', 'account_type', 'is_volunteer']
        # widgets = {
        #     'dob': DateInput(),
        # }

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if first_name != "":
            allowed_char = re.match(r'^[A-Za-z-., ]+$', first_name)
            length = len(first_name)
            if length > 15:
                raise forms.ValidationError("Maximum 15 characters allowed !")
            if not allowed_char:
                raise forms.ValidationError(
                    "Only 'A-Za-z.,-' these characters and spaces are allowed.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if last_name != "":
            allowed_char = re.match(r'^[A-Za-z-., ]+$', last_name)
            length = len(last_name)
            if length > 20:
                raise forms.ValidationError("Maximum 20 characters allowed !")
            if not allowed_char:
                raise forms.ValidationError(
                    "Only 'A-Za-z.,-' these characters and spaces are allowed.")
        return last_name

    # def clean_contact(self):
    #     contact = self.cleaned_data.get("contact")
    #     if contact != '':
    #         appears_special = contact.count('+')
    #         country_code = '+880'
    #         starts_with_code = contact.startswith(country_code)
    #         allowed_char = re.match(r'^[0-9+]+$', contact)
    #         length = len(contact)

    #         if not allowed_char or not starts_with_code or appears_special > 1 or length < 11:
    #             raise forms.ValidationError(
    #                 "Must be valid phone number and start with (+880).</br> Ex: +8801000000000")
    #     return contact

    def clean_contact(self):
        contact = self.cleaned_data.get("contact")
        if contact != '':
            allowed_char = re.match(r'^[0-9]+$', contact)
            if not allowed_char:
                raise forms.ValidationError(
                    "Please enter a valid contact number!")
        return contact

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image == None and not image == False:
            image_extension = os.path.splitext(image.name)[1]
            allowed_image_types = settings.ALLOWED_IMAGE_TYPES
            if not image_extension in allowed_image_types:
                raise forms.ValidationError("Only %s file formats are supported! Current file format is %s" % (
                    allowed_image_types, image_extension))
            if image.size > settings.MAX_IMAGE_UPLOAD_SIZE:
                raise forms.ValidationError("Please keep filesize under %s. Current filesize %s" % (
                    filesizeformat(settings.MAX_IMAGE_UPLOAD_SIZE), filesizeformat(image.size)))
        return image

    def clean_dob(self):
        dob = self.cleaned_data.get('dob')
        if not dob == None:
            today = datetime.date.today()
            if dob > today:
                raise forms.ValidationError(
                    "Please enter valid Date of Birth. Date cannot be greater than today!")
        return dob

    def clean_address(self):
        address = self.cleaned_data.get('address')
        if not address == None:
            length = len(address)
            if length > 100:
                raise forms.ValidationError(
                    f"Maximum 100 characters allowed. [currently using: {length}]")
        return address

    def clean_city(self):
        city = self.cleaned_data.get('city')
        if not city == None:
            length = len(city)
            if length > 25:
                raise forms.ValidationError(
                    f"Maximum 25 characters allowed. [currently using: {length}]")
        return city

    def clean_state(self):
        state = self.cleaned_data.get('state')
        if not state == None:
            length = len(state)
            if length > 25:
                raise forms.ValidationError(
                    f"Maximum 25 characters allowed. [currently using: {length}]")
        return state

    def clean_country(self):
        country = self.cleaned_data.get('country')
        if not country == None:
            length = len(country)
            if length > 25:
                raise forms.ValidationError(
                    f"Maximum 25 characters allowed. [currently using: {length}]")
        return country

    def clean_about(self):
        about = self.cleaned_data.get('about')
        if not about == None:
            length = len(about)
            if length > 250:
                raise forms.ValidationError("Maximum 250 characters allowed !")
        return about

    def clean_facebook(self):
        facebook = self.cleaned_data.get('facebook')
        if not facebook == None:
            length = len(facebook)
            starts_with_http = facebook.startswith("http://")
            starts_with_https = facebook.startswith("https://")
            if length > 150:
                raise forms.ValidationError("Maximum 150 characters allowed !")
            if starts_with_http or starts_with_https:
                return facebook
            else:
                raise forms.ValidationError(
                    "Please enter a valid URL. URL must start with 'http://' or 'https://'")
        return facebook

    def clean_linkedin(self):
        linkedin = self.cleaned_data.get('linkedin')
        if not linkedin == None:
            length = len(linkedin)
            if length > 150:
                raise forms.ValidationError("Maximum 150 characters allowed !")
            starts_with_http = linkedin.startswith("http://")
            starts_with_https = linkedin.startswith("https://")
            if starts_with_http or starts_with_https:
                return linkedin
            else:
                raise forms.ValidationError(
                    "Please enter a valid URL. URL must start with 'http://' or 'https://'")
        return linkedin

    def clean_website(self):
        website = self.cleaned_data.get('website')
        if not website == None:
            length = len(website)
            if length > 150:
                raise forms.ValidationError("Maximum 150 characters allowed !")
            starts_with_http = website.startswith("http://")
            starts_with_https = website.startswith("https://")
            if starts_with_http or starts_with_https:
                return website
            else:
                raise forms.ValidationError(
                    "Please enter a valid URL. URL must start with 'http://' or 'https://'")
        return website

    def save(self, *args, **kwargs):
        self.uf.save(*args, **kwargs)
        return super(UserProfileUpdateForm, self).save(*args, **kwargs)



class UserReportManageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserReportManageForm, self).__init__(*args, **kwargs)
        self.fields['category'].help_text = "Select a report category..."
        self.fields['category'].widget.attrs.update({
            'id': 'report_category_input',
        })
        self.fields['details'].help_text = "Enter details..."
        self.fields['details'].widget.attrs.update({
            'id': 'report_details_input',
            'placeholder': 'Enter details...',
            'rows': 4,
            'cols': 2,
        })

    class Meta:
        model = UserReport
        fields = ['category', 'details']
        exclude = ['user', 'slug', 'created_at', 'updated_at']

    def clean_details(self):
        details = self.cleaned_data.get('details')
        if not details == None:
            length = len(details)
            if length > 600:
                raise forms.ValidationError(
                    f"Maximum 600 characters allowed. [currently using: {length}]")
        return details


class UserPermissionManageForm(forms.ModelForm):
    # details_fake = forms.CharField()
    details_fake = forms.CharField(required=False, widget=CKEditorWidget())
    def __init__(self, *args, **kwargs):
        super(UserPermissionManageForm, self).__init__(*args, **kwargs)
        self.fields['can_browse'].help_text = "Select browse permission..."
        self.fields['can_browse'].widget.attrs.update({
            'id': 'permission_can_browse_input',
        })
        self.fields['can_donate'].help_text = "Select donating permission..."
        self.fields['can_donate'].widget.attrs.update({
            'id': 'permission_can_donate_input',
        })
        self.fields['can_ask_for_a_donor'].help_text = "Select asking for a donor permission..."
        self.fields['can_ask_for_a_donor'].widget.attrs.update({
            'id': 'permission_can_ask_for_a_donor_input',
        })
        self.fields['can_manage_bank'].help_text = "Select managing bank's permission..."
        self.fields['can_manage_bank'].widget.attrs.update({
            'id': 'permission_can_manage_bank_input',
        })
        self.fields['can_chat'].help_text = "Select chatting permission..."
        self.fields['can_chat'].widget.attrs.update({
            'id': 'permission_can_chat_input',
        })
        # self.fields['details_fake'] = forms.CharField(
        #         label="Message", required=False, widget=forms.Textarea())
        self.fields['details_fake'].help_text = "Provide information to user about the reason and other facts..."
        # self.fields['details_fake'].widget.attrs.update({
        #     'id': 'permission_details_fake_input',
        #     'placeholder': 'Provide message to user...',
        #     'maxlength': 500,
        #     'rows': 2,
        #     'cols': 3
        # })
        self.fields['details_fake'].label = "Message"
        self.fields['details_fake'].widget.attrs.update({
            'id': 'permission_details_fake_input'
        })

    class Meta:
        model = UserPermission
        fields = ['can_browse', 'can_donate', 'can_ask_for_a_donor',
                  'can_manage_bank', 'can_chat', 'details_fake']
        exclude = ['user', 'created_at', 'updated_at']

    def clean_details_fake(self):
        details_fake = self.cleaned_data.get('details_fake')
        if not details_fake == None:
            length = len(details_fake)
            if length > 500:
                raise forms.ValidationError(
                    f"Maximum 500 characters allowed. [currently using: {length}]")
        return details_fake
