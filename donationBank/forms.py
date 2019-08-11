from django import forms
import re
from .models import DonationBank, DonationBankSetting

class DonationBankForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DonationBankForm, self).__init__(*args, **kwargs)
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
                  'state', 'country', 'contact', 'email', 'description']
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

    class Meta:
        model = DonationBankSetting
        fields = ['member_request']
        exclude = ['bank', 'created_at', 'updated_at']
