from django import forms
import re
from .models import DonationBank, DonationBankSetting, Donation, DonationProgress
import datetime

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
        self.fields['email'].help_text = "Enter donor's/donor's relative's email address."
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
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
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
            if not self.object == None and not self.object.collection_date == None and not collection_date == self.object.collection_date:
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
            if not self.object == None and not self.object.expiration_date == None and not expiration_date == self.object.expiration_date:
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
            'id': 'donation_completion_date_input',
        })
        self.fields['details'].help_text = "Maximum 400 characters allowed."
        self.fields['details'].widget.attrs.update({
            'id': 'donation_details_input',
            'placeholder': 'Provide some additional information...',
            'maxlength': 400,
            'rows': 2,
            'cols': 2
        })

    class Meta:
        model = DonationProgress
        fields = ['progress_status', 'completion_date', 'details']
        exclude = ['donation', 'created_at', 'updated_at']

    def clean_completion_date(self):
        completion_date = self.cleaned_data.get('completion_date')
        today = datetime.date.today()
        if not completion_date == None:
            if not self.object == None and not self.object.completion_date == None and self.object.completion_date == completion_date:
                return completion_date
            else:
                if completion_date > today:
                    raise forms.ValidationError(
                        "Completion date can't be greater than today!")
        return completion_date

    def clean_details(self):
        details = self.cleaned_data.get('details')
        if not details == None:
            length = len(details)
            if length > 400:
                raise forms.ValidationError(
                    f"Maximum 400 characters allowed. [currently using: {length}]")
        return details