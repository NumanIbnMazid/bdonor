from django import forms
import re
from .models import (DonationBank, DonationBankSetting, Donation, 
                    DonationRequest, DonationProgress, Campaign)
import datetime
from ckeditor.widgets import CKEditorWidget
from django.template.defaultfilters import filesizeformat
from django.conf import settings
import os


class DonationBankForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(DonationBankForm, self).__init__(*args, **kwargs)
        fields = ['institute', 'address', 'city',
                  'state', 'country', 'contact', 'email', 'description', 'is_verified']
        if self.request.user.is_superuser == True:
            self.fields.pop("institute")
            self.fields.pop("address")
            self.fields.pop("city")
            self.fields.pop("state")
            self.fields.pop("country")
            self.fields.pop("contact")
            self.fields.pop("email")
            self.fields.pop("services")
            self.fields.pop("description")
            VERIFICATION_OPTIONS = (
                (True, "Verified"),
                (False, "Not Verified"),
            )
            self.fields['is_verified'] = forms.ChoiceField(
                required=True, choices=VERIFICATION_OPTIONS)
            self.fields['is_verified'].widget.attrs.update({
                'id': 'donation_is_verified_input',
            })
            self.fields['is_verified'].help_text = "Select verification status."
            self.fields['is_verified'].label = "Verification Status"
        else:
            self.fields.pop("is_verified")
            self.fields['institute'].help_text = "Only '_A-z0-9+-.,' these characters and spaces are allowed."
            self.fields['institute'].widget.attrs.update({
                'id': 'bank_institute_input',
                'placeholder': 'Enter institute name...',
                'maxlength': 50,
                'pattern': "^[_A-z0-9 +-.,]{1,}$"
            })
            self.fields['address'].help_text = "Enter Address of the institute."
            self.fields['address'].widget.attrs.update({
                'id': 'bank_address_input',
                'placeholder': 'Enter address...',
                'maxlength': 100,
            })
            self.fields['city'].help_text = "Enter the name of the city."
            self.fields['city'].widget.attrs.update({
                'id': 'bank_city_input',
                'placeholder': 'Enter city...',
                'maxlength': 25,
            })
            self.fields['state'].help_text = "Enter the name of the state."
            self.fields['state'].widget.attrs.update({
                'id': 'bank_state_input',
                'placeholder': 'Enter state...',
                'maxlength': 25,
            })
            self.fields['country'].help_text = "Enter the name of the country."
            self.fields['country'].widget.attrs.update({
                'id': 'bank_country_input',
                'placeholder': 'Enter country...',
                'maxlength': 25,
            })
            self.fields['contact'].help_text = "Enter contact number..."
            self.fields['contact'].widget.attrs.update({
                'id': 'bank_contact_input',
                'placeholder': 'Enter contact number...',
                'maxlength': 20,
                'minlength': 5,
                'pattern': "^[0-9+]{1,}$"
            })
            self.fields['email'].help_text = "Enter email address..."
            self.fields['email'].widget.attrs.update({
                'id': 'bank_email_input',
                'placeholder': 'Enter email address...',
            })
            # SERVICES_CHOICES = (
            #     ("Blood", 'Blood'),
            #     ("Organ", 'Organ'),
            #     ("Tissue", 'Tissue'),
            # )
            # self.fields['services'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
            #                                                     choices=SERVICES_CHOICES, required=True)
            self.fields['services'].help_text = "Select services provided by the bank..."
            self.fields['services'].widget.attrs.update({
                'id': 'bank_services_input',
                'placeholder': 'Select services...',
            })
            self.fields['description'].help_text = "Maximum 400 characters allowed."
            self.fields['description'].widget.attrs.update({
                'id': 'bank_description_input',
                'placeholder': 'Type description...',
                'maxlength': 400,
                'rows': 2,
                'cols': 2
            })

    class Meta:
        model = DonationBank
        fields = ['institute', 'address', 'city',
                  'state', 'country', 'contact', 'email', 'services', 'description', 'is_verified']
        exclude = ['slug', 'created_at', 'updated_at']

    def clean_institute(self):
        institute = self.cleaned_data.get('institute')
        if not institute == None:
            allowed_chars = re.match(r'^[_A-z0-9 +-.,]+$', institute)
            length = len(institute)
            if not allowed_chars:
                raise forms.ValidationError(
                    "Only '_A-z0-9+-.,' these characters and spaces are allowed.")
            if length > 50:
                raise forms.ValidationError(
                    f"Maximum 50 characters allowed. [currently using: {length}]")
        return institute

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

    def clean_contact(self):
        contact = self.cleaned_data.get('contact')
        if not contact == None:
            allowed_chars = re.match(r'^[0-9+]+$', contact)
            if not allowed_chars:
                raise forms.ValidationError(
                    "Only '+0-9' these characters and spaces are allowed.")
            length = len(contact)
            if length > 20:
                raise forms.ValidationError(
                    f"Maximum 20 characters allowed. [currently using: {length}]")
        return contact

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description == None:
            length = len(description)
            if length > 400:
                raise forms.ValidationError(
                    f"Maximum 400 characters allowed. [currently using: {length}]")
        return description


class DonationBankSettingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DonationBankSettingForm, self).__init__(*args, **kwargs)
        self.fields['member_request'].help_text = "If set to 'Not Allow', users won't be able to send member request to your donation bank."
        self.fields['member_request'].widget.attrs.update({
            'id': 'bankSetting_member_request_input',
        })
        self.fields['privacy'].help_text = "Changing privacy to private restricts users to find your bank in bank list."
        self.fields['privacy'].widget.attrs.update({
            'id': 'bankSetting_privacy_input',
        })

    class Meta:
        model = DonationBankSetting
        fields = ['member_request', 'privacy']
        exclude = ['bank', 'created_at', 'updated_at']


class DonationManageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.object = kwargs.pop('object', None)
        super(DonationManageForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].help_text = "Enter first name of donor. Only 'A-Za-z.,\-' these characters and spaces are allowed."
        self.fields['first_name'].widget.attrs.update({
            'id': 'donation_first_name_input',
            'placeholder': 'Enter first name...',
            'maxlength': 30,
            'pattern': "^[A-Za-z.,\- ]{1,}$",
        })
        self.fields['last_name'].help_text = "Enter last name of donor. Only 'A-Za-z.,\-' these characters and spaces are allowed."
        self.fields['last_name'].widget.attrs.update({
            'id': 'donation_last_name_input',
            'placeholder': 'Enter last name...',
            'maxlength': 30,
            'pattern': "^[A-Za-z.,\- ]{1,}$",
        })
        self.fields['email'].help_text = "Enter donor's/donor relative's email address."
        self.fields['email'].widget.attrs.update({
            'id': 'donation_email_input',
            'placeholder': 'Enter email address...',
        })
        self.fields['gender'].help_text = "Select gender."
        self.fields['gender'].widget.attrs.update({
            'id': 'donation_gender_input',
        })
        self.fields['dob'].help_text = "Enter date of birth."
        self.fields['dob'].widget.attrs.update({
            'placeholder': 'Ex: 1996-02-27',
            'id': 'donation_dob_input',
            'onchange': "resetMessage()",
        })
        self.fields['blood_group'].help_text = "Select blood group."
        self.fields['blood_group'].widget.attrs.update({
            'id': 'donation_blood_group_input',
        })
        self.fields['diseases'].help_text = "Enter disease information about donor(if he/she has any diseases)."
        self.fields['diseases'].widget.attrs.update({
            'id': 'donation_diseases_input',
            'placeholder': 'Enter disease information (if any)...',
            'maxlength': 200,
        })
        self.fields['contact'].help_text = "Type contact number..."
        self.fields['contact'].widget.attrs.update({
            'id': 'donation_contact_input',
            'placeholder': 'Ex: +8801680000000',
            'maxlength': 20,
            'minlength': 5,
            'onkeyup': "resetMessage()",
        })
        self.fields['address'].help_text = "Enter Address of the donor."
        self.fields['address'].widget.attrs.update({
            'id': 'donation_address_input',
            'placeholder': 'Enter address...',
            'maxlength': 100,
        })
        self.fields['city'].help_text = "Enter the name of city."
        self.fields['city'].widget.attrs.update({
            'id': 'donation_city_input',
            'placeholder': 'Enter city...',
            'maxlength': 25,
        })
        self.fields['state'].help_text = "Enter the name of the state."
        self.fields['state'].widget.attrs.update({
            'id': 'donation_state_input',
            'placeholder': 'Enter state...',
            'maxlength': 25,
        })
        self.fields['country'].help_text = "Select country."
        self.fields['country'].widget.attrs.update({
            'id': 'donation_country_input',
            'placeholder': 'Select country...',
            'maxlength': 25,
        })
        self.fields['donation_type'].help_text = "Select donation type."
        self.fields['donation_type'].widget.attrs.update({
            'id': 'donation_donation_type_input',
            'onchange': "donationTypeFunction()",
        })
        self.fields['organ_name'].help_text = "Select organ."
        self.fields['organ_name'].widget.attrs.update({
            'id': 'donation_organ_name_input',
            'onchange': "resetMessage(), organFunction()"
        })
        self.fields['tissue_name'].help_text = "Select tissue."
        self.fields['tissue_name'].widget.attrs.update({
            'id': 'donation_tissue_name_input',
            'onchange': "resetMessage()"
        })
        self.fields['quantity'].help_text = "Enter quantity."
        self.fields['quantity'].widget.attrs.update({
            'id': 'donation_quantity_input',
            'placeholder': 'Enter quantity...',
            'onkeyup': "resetMessage()"
        })
        self.fields['description'].help_text = "Maximum 400 characters allowed."
        self.fields['description'].widget.attrs.update({
            'id': 'donation_description_input',
            'placeholder': 'Type description...',
            'maxlength': 400,
            'rows': 2,
            'cols': 2
        })
        self.fields['collection_date'].help_text = "Enter collection date."
        self.fields['collection_date'].widget.attrs.update({
            'placeholder': 'Ex: 2019-02-27',
            'id': 'donation_collection_date_input',
            'onchange': "resetMessage()"
        })
        self.fields['expiration_date'].help_text = "Enter expiration date of donated item."
        self.fields['expiration_date'].widget.attrs.update({
            'placeholder': 'Ex: 2019-02-28',
            'id': 'donation_expiration_date_input',
            'onchange': "resetMessage()"
        })

    class Meta:
        model = Donation
        fields = ['first_name', 'last_name', 'gender', 'dob', 'diseases', 'contact', 'email',
                  'address', 'city', 'state', 'country', 'donation_type', 'blood_group', 'organ_name', 'tissue_name', 'quantity', 'collection_date', 'expiration_date', 'description']
        exclude = ['bank', 'slug', 'created_at', 'updated_at']

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if not first_name == None:
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
        if not last_name == None:
            allowed_char = re.match(r'^[A-Za-z-., ]+$', last_name)
            length = len(last_name)
            if length > 20:
                raise forms.ValidationError("Maximum 20 characters allowed !")
            if not allowed_char:
                raise forms.ValidationError(
                    "Only 'A-Za-z.,-' these characters and spaces are allowed.")
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email == None:
            length = len(email)
            if length > 150:
                raise forms.ValidationError(
                    "Maximum 150 characters allowed !")
        return email

    def clean_dob(self):
        dob = self.cleaned_data.get('dob')
        if not dob == None:
            today = datetime.date.today()
            if dob > today:
                raise forms.ValidationError(
                    "Please enter valid Date of Birth. Date cannot be greater than today!")
            age = today.year - dob.year - \
                ((today.month, today.day) < (dob.month, dob.day))
            if age < 18:
                raise forms.ValidationError(
                    "Donor is too young! A donor must be at least 18 years old in order to donate.")
        return dob

    def clean_diseases(self):
        diseases = self.cleaned_data.get("diseases")
        if not diseases == None:
            length = len(diseases)
            if length > 200:
                raise forms.ValidationError(
                    "Maximum 200 characters allowed !")
        return diseases

    def clean_contact(self):
        contact = self.cleaned_data.get("contact")
        if not contact == None:
            allowed_char = re.match(r'^[0-9+]+$', contact)
            if not allowed_char:
                raise forms.ValidationError(
                    "Please enter a valid contact number!")
            length = len(contact)
            if length > 20:
                raise forms.ValidationError(
                    "Maximum 20 characters allowed !")
        return contact

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

    def clean_quantity(self):
        quantity = self.cleaned_data.get("quantity")
        if not quantity == None:
            allowed_char = re.match(r'^[0-9]+$', str(quantity))
            if not allowed_char:
                raise forms.ValidationError(
                    "Please enter a valid quantity!")
            if quantity > 2:
                raise forms.ValidationError(
                    "Maximum quantity 2 is allowed!")
        return quantity

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description == None:
            length = len(description)
            if length > 400:
                raise forms.ValidationError(
                    f"Maximum 400 characters allowed. [currently using: {length}]")
        return description

    def clean_collection_date(self):
        collection_date = self.cleaned_data.get('collection_date')
        today = datetime.date.today()
        if not collection_date == None:
            # if not self.object == None and not self.object.collection_date == None and not collection_date == self.object.collection_date:
            if not self.object == None and not self.object.collection_date == None and collection_date == self.object.collection_date:
                return collection_date
            else:
                if collection_date > today:
                    raise forms.ValidationError(
                        "Date cannot be greater than today!")
                # if collection_date < today:
                #     raise forms.ValidationError(
                #         'You cannot select previous date!')
                # if collection_date.strftime('%Y-%m-%d') < today.strftime('%Y-%m-%d'):
                #     raise forms.ValidationError(
                #         'You cannot select previous date!')
        return collection_date

    def clean_expiration_date(self):
        expiration_date = self.cleaned_data.get('expiration_date')
        collection_date = self.cleaned_data.get('collection_date')
        today = datetime.date.today()
        if not expiration_date == None and not collection_date == None:
            # if not self.object == None and not self.object.expiration_date == None and not expiration_date == self.object.expiration_date:
            if not self.object == None and not self.object.expiration_date == None and expiration_date == self.object.expiration_date:
                return expiration_date
            else:
                if collection_date == today:
                    if not expiration_date >= collection_date:
                        raise forms.ValidationError(
                            'Expiration Date must be greater than or equal Collection Date!')
                else:
                    if not expiration_date > collection_date:
                        raise forms.ValidationError(
                            'Expiration Date must be greater than Collection Date and must be greater than or equal today!')
                if expiration_date < today:
                    raise forms.ValidationError(
                        'You cannot select previous date!')
                # if expiration_date.strftime('%Y-%m-%d') < today.strftime('%Y-%m-%d'):
                #     raise forms.ValidationError(
                #         'You cannot select previous date!')
        return expiration_date


class DonationRequestManageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.object = kwargs.pop('object', None)
        super(DonationRequestManageForm, self).__init__(*args, **kwargs)
        self.fields['donation_type'].help_text = "Select donation type."
        self.fields['donation_type'].widget.attrs.update({
            'id': 'donation_request_donation_type_input',
            'onchange': "donationTypeFunction()",
        })
        self.fields['blood_group'].help_text = "Select blood group."
        self.fields['blood_group'].widget.attrs.update({
            'id': 'donation_request_blood_group_input',
        })
        self.fields['organ_name'].help_text = "Select organ."
        self.fields['organ_name'].widget.attrs.update({
            'id': 'donation_request_organ_name_input',
            'onchange': "resetMessage(), organFunction()"
        })
        self.fields['tissue_name'].help_text = "Select tissue."
        self.fields['tissue_name'].widget.attrs.update({
            'id': 'donation_request_tissue_name_input',
            'onchange': "resetMessage()"
        })
        self.fields['quantity'].help_text = "Enter quantity."
        self.fields['quantity'].widget.attrs.update({
            'id': 'donation_request_quantity_input',
            'placeholder': 'Enter quantity...',
            'onkeyup': "resetMessage()"
        })
        self.fields['details'].help_text = "Maximum 2000 characters allowed."
        self.fields['details'].widget.attrs.update({
            'id': 'donation_request_details_input',
            'placeholder': 'Type details...',
            'maxlength': 2000,
            'rows': 2,
            'cols': 2
        })
        self.fields['publication_status'].help_text = "Select publication status."
        self.fields['publication_status'].widget.attrs.update({
            'id': 'donation_request_publication_status_input',
        })

    class Meta:
        model = DonationRequest
        fields = ['donation_type', 'blood_group',
                  'organ_name', 'tissue_name', 'quantity', 'details', 'publication_status']
        exclude = ['bank', 'slug', 'created_at', 'updated_at']
        widgets = {
            'details': CKEditorWidget(),
        }

    def clean_quantity(self):
        quantity = int(self.cleaned_data.get("quantity"))
        # print(type(quantity))
        if not quantity == None:
            allowed_char = re.match(r'^[0-9]+$', str(quantity))
            if not allowed_char:
                raise forms.ValidationError(
                    "Please enter a valid quantity!")
            if quantity > 100:
                raise forms.ValidationError(
                    "Maximum quantity 100 is allowed!")
        return quantity

    def clean_details(self):
        details = self.cleaned_data.get('details')
        if not details == None:
            length = len(details)
            if length > 2000:
                raise forms.ValidationError(
                    f"Maximum 2000 characters allowed. [currently using: {length}]")
        return details


class DonationProgressForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.object = kwargs.pop('object', None)
        super(DonationProgressForm, self).__init__(*args, **kwargs)
        self.fields['progress_status'].help_text = "Select progress status..."
        self.fields['progress_status'].widget.attrs.update({
            'id': 'donation_progress_status_input',
        })
        self.fields['completion_date'].help_text = "Select completion date..."
        self.fields['completion_date'].widget.attrs.update({
            'id': 'donation_progress_completion_date_input',
            'placeholder': 'Ex: 2019-02-27',
        })
        self.fields['first_name'].help_text = "Enter first name of donation receiver. Only 'A-Za-z.,\-' these characters and spaces are allowed."
        self.fields['first_name'].widget.attrs.update({
            'id': 'donation_progress_first_name_input',
            'placeholder': 'Enter first name...',
            'maxlength': 30,
            'pattern': "^[A-Za-z.,\- ]{1,}$",
        })
        self.fields['last_name'].help_text = "Enter last name of donation receiver. Only 'A-Za-z.,\-' these characters and spaces are allowed."
        self.fields['last_name'].widget.attrs.update({
            'id': 'donation_progress_last_name_input',
            'placeholder': 'Enter last name...',
            'maxlength': 30,
            'pattern': "^[A-Za-z.,\- ]{1,}$",
        })
        self.fields['email'].help_text = "Enter donation receiver's email address."
        self.fields['email'].widget.attrs.update({
            'id': 'donation_progress_email_input',
            'placeholder': 'Enter email address...',
        })
        self.fields['gender'].help_text = "Select gender."
        self.fields['gender'].widget.attrs.update({
            'id': 'donation_progress_gender_input',
        })
        self.fields['dob'].help_text = "Enter date of birth."
        self.fields['dob'].widget.attrs.update({
            'placeholder': 'Ex: 1996-02-27',
            'id': 'donation_progress_dob_input',
            'onchange': "resetMessage()",
        })
        self.fields['blood_group'].help_text = "Select blood group."
        self.fields['blood_group'].widget.attrs.update({
            'id': 'donation_progress_blood_group_input',
        })
        self.fields['contact'].help_text = "Type contact number..."
        self.fields['contact'].widget.attrs.update({
            'id': 'donation_progress_contact_input',
            'placeholder': 'Ex: +8801680000000',
            'maxlength': 20,
            'minlength': 5,
            'onkeyup': "resetMessage()",
        })
        self.fields['address'].help_text = "Enter Address of the donation receiver."
        self.fields['address'].widget.attrs.update({
            'id': 'donation_progress_address_input',
            'placeholder': 'Enter address...',
            'maxlength': 100,
        })
        self.fields['city'].help_text = "Enter the name of city."
        self.fields['city'].widget.attrs.update({
            'id': 'donation_progress_city_input',
            'placeholder': 'Enter city...',
            'maxlength': 25,
        })
        self.fields['state'].help_text = "Enter the name of the state."
        self.fields['state'].widget.attrs.update({
            'id': 'donation_progress_state_input',
            'placeholder': 'Enter state...',
            'maxlength': 25,
        })
        self.fields['country'].help_text = "Select country."
        self.fields['country'].widget.attrs.update({
            'id': 'donation_progress_country_input',
            'placeholder': 'Select country...',
            'maxlength': 25,
        })
        self.fields['details'].help_text = "Maximum 400 characters allowed."
        self.fields['details'].widget.attrs.update({
            'id': 'donation_progress_details_input',
            'placeholder': 'Provide some additional information...',
            'maxlength': 400,
            'rows': 2,
            'cols': 2
        })

    class Meta:
        model = DonationProgress
        fields = ['progress_status', 'completion_date', 'first_name', 'last_name',
                  'gender', 'blood_group', 'dob', 'contact', 'email', 'address', 'city', 'state', 'country', 'details']
        exclude = ['donation', 'created_at', 'updated_at']

    def clean_completion_date(self):
        completion_date = self.cleaned_data.get('completion_date')
        today = datetime.date.today()
        if not completion_date == None:
            if not self.object == None and not self.object.completion_date == None and completion_date == self.object.completion_date:
                return completion_date
            else:
                if completion_date > today:
                    raise forms.ValidationError(
                        "Completion date can't be greater than today!")
        return completion_date
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if not first_name == None:
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
        if not last_name == None:
            allowed_char = re.match(r'^[A-Za-z-., ]+$', last_name)
            length = len(last_name)
            if length > 20:
                raise forms.ValidationError("Maximum 20 characters allowed !")
            if not allowed_char:
                raise forms.ValidationError(
                    "Only 'A-Za-z.,-' these characters and spaces are allowed.")
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email == None:
            length = len(email)
            if length > 150:
                raise forms.ValidationError(
                    "Maximum 150 characters allowed !")
        return email

    def clean_dob(self):
        dob = self.cleaned_data.get('dob')
        if not dob == None:
            today = datetime.date.today()
            if dob > today:
                raise forms.ValidationError(
                    "Please enter valid Date of Birth. Date cannot be greater than today!")
        return dob

    def clean_contact(self):
        contact = self.cleaned_data.get("contact")
        if not contact == None:
            allowed_char = re.match(r'^[0-9+]+$', contact)
            if not allowed_char:
                raise forms.ValidationError(
                    "Please enter a valid contact number!")
            length = len(contact)
            if length > 20:
                raise forms.ValidationError(
                    "Maximum 20 characters allowed !")
        return contact

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

    def clean_details(self):
        details = self.cleaned_data.get('details')
        if not details == None:
            length = len(details)
            if length > 400:
                raise forms.ValidationError(
                    f"Maximum 400 characters allowed. [currently using: {length}]")
        return details


class CampaignManageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.object = kwargs.pop('object', None)
        super(CampaignManageForm, self).__init__(*args, **kwargs)
        bank_qs = DonationBank.objects.filter(bank_member__user=self.request.user)
        self.fields['title'].help_text = "Maximum 100 characters, only '_A-z0-9+-.#,' these characters and spaces are allowed."
        self.fields['title'].widget.attrs.update({
            'id': 'campaign_title_input',
            'placeholder': 'Enter campaign name...',
            'maxlength': 100,
            'pattern': "^[_A-z0-9 +-.,#]{1,}$",
        })
        self.fields['held_date'].help_text = "Select campaign held date time."
        self.fields['held_date'].widget.attrs.update({
            'id': 'campaign_held_date_input',
            'placeholder': 'Select campaign held date...',
        })
        self.fields['end_date'].help_text = "Select campaign end date time."
        self.fields['end_date'].widget.attrs.update({
            'id': 'campaign_end_date_input',
            'placeholder': 'Select campaign end date...',
        })
        self.fields['contact'].help_text = "Type contact number..."
        self.fields['contact'].widget.attrs.update({
            'id': 'campaign_contact_input',
            'placeholder': 'Type contact number...',
            'maxlength': 20,
            'minlength': 5,
            'pattern': "^[0-9+]{1,}$",
        })
        if bank_qs.exists() and not bank_qs.first().contact == "" and self.object == None:
            self.initial['contact'] = bank_qs.first().contact
        self.fields['email'].help_text = "Enter email address."
        self.fields['email'].widget.attrs.update({
            'id': 'campaign_email_input',
            'placeholder': 'Enter email address...',
        })
        if bank_qs.exists() and not bank_qs.first().email == "" and self.object == None:
            self.initial['email'] = bank_qs.first().email
        self.fields['address'].help_text = "Enter Address of the campaign."
        self.fields['address'].widget.attrs.update({
            'id': 'campaign_address_input',
            'placeholder': 'Enter address...',
            'maxlength': 100,
        })
        if bank_qs.exists() and not bank_qs.first().address == "" and self.object == None:
            self.initial['address'] = bank_qs.first().address
        self.fields['city'].help_text = "Enter the name of the city."
        self.fields['city'].widget.attrs.update({
            'id': 'campaign_city_input',
            'placeholder': 'Enter city...',
            'maxlength': 25,
        })
        if bank_qs.exists() and not bank_qs.first().city == "" and self.object == None:
            self.initial['city'] = bank_qs.first().city
        self.fields['state'].help_text = "Enter the name of the state."
        self.fields['state'].widget.attrs.update({
            'id': 'campaign_state_input',
            'placeholder': 'Enter state...',
            'maxlength': 25,
        })
        if bank_qs.exists() and not bank_qs.first().state == "" and self.object == None:
            self.initial['state'] = bank_qs.first().state
        self.fields['country'].help_text = "Enter the name of the country."
        self.fields['country'].widget.attrs.update({
            'id': 'campaign_country_input',
            'placeholder': 'Enter country...',
            'maxlength': 25,
        })
        if bank_qs.exists() and not bank_qs.first().country == "" and self.object == None:
            self.initial['country'] = bank_qs.first().country
        self.fields['details'].help_text = "Enter description and rules/regulations of campaign."
        # self.fields['details'] = forms.CharField(
        #     required=False, widget=CKEditorWidget())
        self.fields['details'].widget.attrs.update({
            'id': 'campaign_details_input',
            'placeholder': 'Enter description and rules/regulations...',
            'maxlength': 2000,
        })
        self.fields['image'].help_text = "Enter image/banner of the campaign"
        self.fields['image'].widget.attrs.update({
            'id': 'campaign_image_input',
            'placeholder': 'Select image/banner...',
        })

    class Meta:
        model = Campaign
        fields = ['title', 'held_date', 'end_date', 'contact', 'email', 'address',
                  'city', 'state', 'country', 'image', 'details']
        exclude = ['bank', 'slug', 'created_at', 'updated_at']
        widgets = {
            'details': CKEditorWidget(),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title == None:
            allowed_chars = re.match(r'^[_A-z0-9 +-.,]+$', title)
            length = len(title)
            if not allowed_chars:
                raise forms.ValidationError(
                    "Only '_A-z0-9+-.,' these characters and spaces are allowed.")
            if length > 50:
                raise forms.ValidationError(
                    f"Maximum 50 characters allowed. [currently using: {length}]")
        return title

    def clean_held_date(self):
        held_date = self.cleaned_data.get('held_date')
        today = datetime.datetime.now()
        if not held_date == None:
            if not self.object == None and not self.object.held_date == None and held_date == self.object.held_date:
                return held_date
            else:
                if held_date < today:
                    raise forms.ValidationError(
                        "Held date must be greater than or equal today!")
        return held_date
    
    def clean_end_date(self):
        held_date = self.cleaned_data.get('held_date')
        end_date = self.cleaned_data.get('end_date')
        today = datetime.datetime.now()
        if not held_date == None and not end_date == None:
            if not self.object == None and not self.object.end_date == None and end_date == self.object.end_date:
                return end_date
            else:
                if not end_date > held_date:
                    raise forms.ValidationError(
                        'End Date must be greater than equal Held Date!')
                if end_date < today:
                    raise forms.ValidationError(
                        'You cannot select previous date!')
        return end_date

    def clean_contact(self):
        contact = self.cleaned_data.get("contact")
        if not contact == None:
            allowed_char = re.match(r'^[0-9+]+$', contact)
            if not allowed_char:
                raise forms.ValidationError(
                    "Please enter a valid contact number!")
            length = len(contact)
            if length > 20:
                raise forms.ValidationError(
                    "Maximum 20 characters allowed !")
        return contact

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

    def clean_details(self):
        details = self.cleaned_data.get('details')
        if not details == None:
            length = len(details)
            if length > 2000:
                raise forms.ValidationError(
                    f"Maximum 2000 characters allowed. [currently using: {length}]")
        return details
