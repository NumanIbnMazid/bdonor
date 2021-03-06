from django import forms
from .models import Donation, DonationProgress, DonationRespond
from accounts.models import UserProfile
import re
from ckeditor.widgets import CKEditorWidget
import datetime


class DonationForm(forms.ModelForm):
    details_fake = forms.CharField(required=False, widget=CKEditorWidget())

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.object = kwargs.pop('object', None)
        self.date_with_time_val = self.request.POST.get("datetime")
        super(DonationForm, self).__init__(*args, **kwargs)
        user_profile_filter = UserProfile.objects.filter(
            user=self.request.user)
        if self.request.user.is_superuser == True:
            self.fields.pop("type")
            self.fields.pop("organ_name")
            self.fields.pop("tissue_name")
            self.fields.pop("quantity")
            self.fields.pop("blood_group")
            self.fields.pop("blood_bag")
            self.fields.pop("contact")
            self.fields.pop("contact2")
            self.fields.pop("contact3")
            self.fields.pop("location")
            self.fields.pop("city")
            self.fields.pop("state")
            self.fields.pop("country")
            self.fields.pop("hospital")
            self.fields.pop("details")
            self.fields.pop("details_fake")
            self.fields.pop("preferred_date")
            self.fields.pop("preferred_date_from")
            self.fields.pop("preferred_date_to")
            self.fields.pop("priority")
            self.fields.pop("publication_status")
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
            # self.fields['title'].help_text = "Maximum 50 characters allowed. Keep it short. Only '_A-z0-9+-.,' these characters and spaces are allowed."
            # self.fields['title'].widget.attrs.update({
            #     'placeholder': 'I need . . .',
            #     'id': 'donation_title_input',
            #     'maxlength': 50,
            #     'pattern': "^[_A-z0-9 +-.,]{1,}$"
            # })
            self.fields['type'].help_text = "Select donation type."
            self.fields['type'].widget.attrs.update({
                'id': 'donation_type_input',
                'onchange': "typeFunction()",
            })
            # self.fields['custom_type'].help_text = "Maximum 30 characters allowed. Only '_A-z-' these characters and spaces are allowed."
            # self.fields['custom_type'].widget.attrs.update({
            #     'id': 'donation_custom_type_input',
            #     'placeholder': 'Enter donation type name...',
            #     'maxlength': 30,
            #     'pattern': "^[_A-z -]{1,}$",
            #     'onkeyup': "resetMessage()"
            # })
            # if user_profile_filter.exists() and not user_profile_filter.first().blood_group == "":
            #     self.initial['blood_group'] = user_profile_filter.first().blood_group
            self.fields['blood_group'].help_text = "Select blood group."
            self.fields['blood_group'].widget.attrs.update({
                'id': 'donation_blood_group_input',
                'onchange': "resetMessage()"
            })
            if user_profile_filter.exists() and not user_profile_filter.first().blood_group == "" and self.object == None:
                self.initial['blood_group'] = user_profile_filter.first().blood_group
            self.fields['blood_bag'].help_text = "Enter quantity."
            self.fields['blood_bag'].widget.attrs.update({
                'id': 'donation_blood_bag_input',
                'placeholder': 'Enter blood bag quantity...',
                'onchange': "resetMessage()"
            })
            self.fields['organ_name'].help_text = "Select organ."
            self.fields['organ_name'].widget.attrs.update({
                'id': 'donation_organ_name_input',
                'onchange': "resetMessage(), organFunction()"
            })
            self.fields['tissue_name'].help_text = "Select tissue."
            self.fields['tissue_name'].widget.attrs.update({
                'id': 'donation_tissue_name_input',
                'onchange': "resetMessage(), tissueFunction()"
            })
            self.fields['quantity'].help_text = "Enter quantity."
            self.fields['quantity'].widget.attrs.update({
                'id': 'donation_quantity_input',
                'placeholder': 'Enter quantity...',
                'onkeyup': "resetMessage(), quantityFunction()"
            })
            # self.fields['organ_name'].help_text = "Maximum 30 characters, '_A-z -' and spaces allowed."
            # self.fields['organ_name'].widget.attrs.update({
            #     'id': 'donation_organ_name_input',
            #     'placeholder': 'Type organ name...',
            #     'maxlength': 30,
            #     'onkeyup': "resetMessage()",
            #     'pattern': "^[_A-z -]{1,}$"
            # })
            self.fields['details'].help_text = "Maximum 400 characters allowed."
            self.fields['details'].widget.attrs.update({
                'id': 'donation_details_input',
                'placeholder': 'Type details...',
                'maxlength': 400,
                'rows': 2,
                'cols': 2
            })
            # self.fields['details'].help_text = "Enter details information..."
            self.fields['details_fake'].label = "Details"
            self.fields['details_fake'].widget.attrs.update({
                'id': 'donation_details_fake_input',
                # 'placeholder': 'Type details...',
                # 'maxlength': 400,
                # 'rows': 2,
                # 'cols': 2
            })
            self.fields['contact'].help_text = "Type contact number..."
            self.fields['contact'].widget.attrs.update({
                'id': 'donation_contact_input',
                # 'placeholder': 'Type contact number...',
                'maxlength': 20,
                'minlength': 5,
            })
            if user_profile_filter.exists() and not user_profile_filter.first().contact == "" and self.object == None:
                self.initial['contact'] = user_profile_filter.first().contact
            self.fields['contact2'].help_text = "Type second contact number..."
            self.fields['contact2'].widget.attrs.update({
                'id': 'donation_contact2_input',
                # 'placeholder': 'Type second contact number...',
                'maxlength': 20,
                'minlength': 5,
            })
            self.fields['contact3'].help_text = "Type third contact number..."
            self.fields['contact3'].widget.attrs.update({
                'id': 'donation_contact3_input',
                # 'placeholder': 'Type third contact number...',
                'maxlength': 20,
                'minlength': 5,
            })

            self.fields['preferred_date'].help_text = "Select date that you prefer to manage donation."
            self.fields['preferred_date'].widget.attrs.update({
                'id': 'donation_preferred_date_input',
                'placeholder': 'Select your preferred date...',
            })
            if not self.object == None and self.object.preferred_date is not None:
                if self.object.preferred_date.strftime("%H:%M:%S") == "00:00:00":
                    self.initial['preferred_date'] = self.object.preferred_date.strftime(
                        "%Y-%m-%d")
                else:
                    self.initial['preferred_date'] = self.object.preferred_date.strftime(
                        "%Y-%m-%d %H:%M")

            self.fields['preferred_date_from'].help_text = "Select date from that you prefer to manage donation."
            self.fields['preferred_date_from'].widget.attrs.update({
                'id': 'donation_preferred_date_from_input',
                'placeholder': 'Preferred date starts from...',
            })
            if not self.object == None and self.object.preferred_date_from is not None:
                if self.object.preferred_date_from.strftime("%H:%M:%S") == "00:00:00":
                    self.initial['preferred_date_from'] = self.object.preferred_date_from.strftime(
                        "%Y-%m-%d")
                else:
                    self.initial['preferred_date_from'] = self.object.preferred_date_from.strftime(
                        "%Y-%m-%d %H:%M")

            self.fields['preferred_date_to'].help_text = "Select date to that you prefer to manage donation."
            self.fields['preferred_date_to'].widget.attrs.update({
                'id': 'donation_preferred_date_to_input',
                'placeholder': 'Preferred date ends at...',
            })
            if not self.object == None and self.object.preferred_date_to is not None:
                if self.object.preferred_date_to.strftime("%H:%M:%S") == "00:00:00":
                    self.initial['preferred_date_to'] = self.object.preferred_date_to.strftime(
                        "%Y-%m-%d")
                else:
                    self.initial['preferred_date_to'] = self.object.preferred_date_to.strftime(
                        "%Y-%m-%d %H:%M")

            self.fields['location'].help_text = "Maximum 180 characters, only '_A-z0-9+-.#,/' these characters and spaces are allowed."
            self.fields['location'].widget.attrs.update({
                'id': 'donation_location_input',
                'placeholder': 'Type preferred location...',
                'maxlength': 180,
                'pattern': "^[_A-z0-9 +-.,#/]{1,}$",
            })
            self.fields['city'].help_text = 'Enter your City.'
            self.fields['city'].widget.attrs.update({
                'id': 'donation_city_input',
                'placeholder': 'Enter city...',
                'maxlength': 25,
            })
            if user_profile_filter.exists() and not user_profile_filter.first().city == "" and self.object == None:
                self.initial['city'] = user_profile_filter.first().city
            self.fields['state'].help_text = 'Enter your State.'
            self.fields['state'].widget.attrs.update({
                'id': 'donation_state_input',
                'placeholder': 'Enter state...',
                'maxlength': 25,
            })
            if user_profile_filter.exists() and not user_profile_filter.first().state == "" and self.object == None:
                self.initial['state'] = user_profile_filter.first().state
            self.fields['country'].help_text = 'Select your Country.'
            self.fields['country'].widget.attrs.update({
                'id': 'donation_country_input',
                'placeholder': 'Select country...',
                'maxlength': 25,
            })
            if user_profile_filter.exists() and not user_profile_filter.first().country == "" and self.object == None:
                self.initial['country'] = user_profile_filter.first().country
            self.fields['hospital'].help_text = "Maximum 180 characters, only '_A-z0-9+-.#,/' these characters and spaces are allowed."
            self.fields['hospital'].widget.attrs.update({
                'id': 'donation_hospital_input',
                'placeholder': 'Type preferred hospital...',
                'maxlength': 180,
                'pattern': "^[_A-z0-9 +-.,#/]{1,}$"
            })
            self.fields['priority'].help_text = "Selecting priority as important helps to draw attention of viewers."
            self.fields['priority'].widget.attrs.update({
                'id': 'donation_priority_input',
            })
            self.fields[
                'publication_status'].help_text = "Selecting publication status as unpublished will save your post as draft."
            self.fields['publication_status'].widget.attrs.update({
                'id': 'donation_publication_status_input',
            })

    class Meta:
        model = Donation
        fields = ['type', 'organ_name', 'tissue_name', 'quantity', 'blood_group', 'blood_bag', 'contact', 'contact2',
                  'contact3', 'location', 'city', 'state', 'country', 'hospital', 'details', 'details_fake',
                  'preferred_date', 'preferred_date_from', 'preferred_date_to', 'priority', 'publication_status', 'is_verified']
        exclude = ['user', 'slug', 'category',
                   'donate_type', 'created_at', 'updated_at']

    # def clean_title(self):
    #     title = self.cleaned_data.get('title')
    #     if not title == None:
    #         allowed_chars = re.match(r'^[_A-z0-9 +-.,]+$', title)
    #         length = len(title)
    #         if not allowed_chars:
    #             raise forms.ValidationError(
    #                 "Only '_A-z0-9+-.,' these characters and spaces are allowed.")
    #         if length > 50:
    #             raise forms.ValidationError(
    #                 f"Maximum 50 characters allowed. [currently using: {length}]")
    #     return title

    # def clean_type(self):
    #     type = self.cleaned_data.get('type')
    #     if not type == None:

    #         raise forms.ValidationError(".")
    #     return type

    # def clean_custom_type(self):
    #     custom_type = self.cleaned_data.get('custom_type')
    #     if not custom_type == None:
    #         allowed_chars = re.match(r'^[_A-z -]+$', custom_type)
    #         length = len(custom_type)
    #         if not allowed_chars:
    #             raise forms.ValidationError(
    #                 "Only '_A-z-' these characters and spaces are allowed.")
    #         if length > 30:
    #             raise forms.ValidationError(
    #                 f"Maximum 30 characters allowed. [currently using: {length}]")
    #     return custom_type

    # def clean_organ_name(self):
    #     organ_name = self.cleaned_data.get('organ_name')
    #     if not organ_name == None:
    #         allowed_chars = re.match(r'^[_A-z -]+$', organ_name)
    #         length = len(organ_name)
    #         if not allowed_chars:
    #             raise forms.ValidationError(
    #                 "Only '_A-z-' these characters and spaces are allowed.")
    #         if length > 50:
    #             raise forms.ValidationError(
    #                 f"Maximum 50 characters allowed. [currently using: {length}]")
    #     return organ_name

    def clean_details(self):
        details = self.cleaned_data.get('details')
        if not details == None:
            length = len(details)
            if length > 500:
                raise forms.ValidationError(
                    f"Maximum 500 characters allowed. [currently using: {length}]")
        return details

    def clean_details_fake(self):
        details_fake = self.cleaned_data.get('details_fake')
        if not details_fake == None:
            length = len(details_fake)
            if length > 5000:
                raise forms.ValidationError(
                    f"Maximum 5000 characters allowed. [currently using: {length}]")
        return details_fake

    def clean_preferred_date(self):
        preferred_date = self.cleaned_data.get('preferred_date')
        today = datetime.datetime.now()
        if not preferred_date == None:
            if not self.object == None and not self.object.preferred_date == None and self.object.preferred_date == preferred_date:
            # if self.object == None or self.object.preferred_date == None and not preferred_date == self.object.preferred_date:
                return preferred_date
            else:
                if self.date_with_time_val == 'true':
                    # if not preferred_date.strftime('%H:%M:%S') == "00:00:00":
                    if preferred_date < today:
                        raise forms.ValidationError(
                            'You cannot select previous date as Preferred Date!')
                    # if preferred_date.strftime('%H:%M:%S') == "00:00:00":
                    #     raise forms.ValidationError('Time "00:00:00" is reserved! Please select one minute earlier or later.')
                if self.date_with_time_val == 'false':
                    if preferred_date.strftime('%Y-%m-%d') < today.strftime('%Y-%m-%d'):
                        raise forms.ValidationError(
                            'You cannot select previous date as Preferred Date!')
        return preferred_date

    def clean_preferred_date_from(self):
        preferred_date_from = self.cleaned_data.get('preferred_date_from')
        # if not preferred_date_from == None :
        #     today = datetime.datetime.now()
        #     if preferred_date_from < today:
        #         raise forms.ValidationError('You cannot select previous date as Preferred Date starts from!')
        today = datetime.datetime.now()
        if not preferred_date_from == None:
            if not self.object == None and not self.object.preferred_date_from == None and preferred_date_from == self.object.preferred_date_from:
            # if self.object == None or self.object.preferred_date_from == None and not preferred_date_from == self.object.preferred_date_from:
                return preferred_date_from
            else:
                if self.date_with_time_val == 'true':
                    if preferred_date_from < today:
                        raise forms.ValidationError(
                            'You cannot select previous date!')
                if self.date_with_time_val == 'false':
                    if preferred_date_from.strftime('%Y-%m-%d') < today.strftime('%Y-%m-%d'):
                        raise forms.ValidationError(
                            'You cannot select previous date!')
        return preferred_date_from

    def clean_preferred_date_to(self):
        preferred_date_to = self.cleaned_data.get('preferred_date_to')
        preferred_date_from = self.cleaned_data.get('preferred_date_from')
        today = datetime.datetime.now()
        if not preferred_date_to == None and not preferred_date_from == None:
            # delta = preferred_date_to - preferred_date_from
            # Delta time format
            # total_secs = delta.seconds
            # secs = total_secs % 60
            # total_mins = total_secs / 60
            # mins = total_mins % 60
            # hours = total_mins / 60
            # print(delta)
            # Delta time format
            if preferred_date_from >= preferred_date_to:
                raise forms.ValidationError(
                    'Preferred Date to must be greater than Preferred Date From!')
            # if not delta.days >= 1:
            #     raise forms.ValidationError(
            #         f'Difference between Preferred Date From and Preferred Date To must be at least one day! <br> [Current difference is {delta.days} days, {hours} hours, {mins} minutes.]'
            #     )
            if preferred_date_to.strftime('%Y-%m-%d') == preferred_date_from.strftime('%Y-%m-%d'):
                raise forms.ValidationError(
                    'You cannot select preferred date to as same as preferred date from! Choose deffrent date from preferred date from.')
            if not self.object == None and not self.object.preferred_date_to == None and preferred_date_to == self.object.preferred_date_to:
            # if self.object == None or self.object.preferred_date_to == None and not preferred_date_to == self.object.preferred_date_to:
                return preferred_date_to
            else:
                if self.date_with_time_val == 'true':
                    if preferred_date_to < today:
                        raise forms.ValidationError(
                            'You cannot select previous date!')
                if self.date_with_time_val == 'false':
                    if preferred_date_to.strftime('%Y-%m-%d') < today.strftime('%Y-%m-%d'):
                        raise forms.ValidationError(
                            'You cannot select previous date!')
        return preferred_date_to

    def clean_location(self):
        location = self.cleaned_data.get('location')
        if not location == None:
            allowed_chars = re.match(r'^[_A-z0-9 +-.#,/]+$', location)
            length = len(location)
            if not allowed_chars:
                raise forms.ValidationError(
                    "Only '_A-z0-9+-.#,/' these characters and spaces are allowed.")
            if length > 180:
                raise forms.ValidationError(
                    f"Maximum 180 characters allowed. [currently using: {length}]")
        return location

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

    def clean_hospital(self):
        hospital = self.cleaned_data.get('hospital')
        if not hospital == None:
            allowed_chars = re.match(r'^[_A-z0-9 +-.#,/]+$', hospital)
            length = len(hospital)
            if not allowed_chars:
                raise forms.ValidationError(
                    "Only '_A-z0-9+-.#,/' these characters and spaces are allowed.")
            if length > 180:
                raise forms.ValidationError(
                    f"Maximum 180 characters allowed. [currently using: {length}]")
        return hospital


class DonationRespondForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.object = kwargs.pop('object', None)
        super(DonationRespondForm, self).__init__(*args, **kwargs)
        user_profile_filter = UserProfile.objects.filter(
            user=self.request.user)
        self.fields['contact'].help_text = "Type contact number..."
        self.fields['contact'].widget.attrs.update({
            'id': 'donation_contact_input',
            # 'placeholder': 'Type contact number...',
            'onkeyup': "resetMessage()",
            'maxlength': 20,
        })
        if user_profile_filter.exists() and not user_profile_filter.first().contact == "" and self.object == None:
            self.initial['contact'] = user_profile_filter.first().contact
        self.fields['message'].help_text = "Maximum 200 characters allowed."
        self.fields['message'].widget.attrs.update({
            'id': 'donation_message_input',
            'placeholder': 'Provide some additional message...',
            'maxlength': 200,
            'rows': 2,
            'cols': 2
        })
        if self.object == None:
            self.initial['message'] = "Please contact with me ..."

    class Meta:
        model = DonationRespond
        fields = ['contact', 'message']
        exclude = ['donation', 'respondent', 'created_at', 'updated_at']

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if not message == None:
            length = len(message)
            if length > 200:
                raise forms.ValidationError(
                    f"Maximum 200 characters allowed. [currently using: {length}]")
        return message


class DonationProgressForm(forms.ModelForm):
    status_fake = forms.CharField(required=True, label="Status", initial="Mark as Completed", disabled=True)
    respondent_fake = forms.CharField()
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.object = kwargs.pop('object', None)
        super(DonationProgressForm, self).__init__(*args, **kwargs)
        self.fields['progress_status'].help_text = "Select progress status..."
        self.fields['progress_status'].widget.attrs.update({
            'id': 'donation_progress_status_input',
            # 'placeholder': 'Type contact number...',
        })
        # if not self.object == None:
        respond_qs = None
        if self.object.donation.category == 0 and not self.object.donation.user.user == self.request.user:
            self.fields.pop("respondent")
            self.fields.pop("progress_status")
            self.fields.pop("completion_date")
            self.fields.pop("management_status")
            self.fields.pop("details")
            respond_qs = DonationRespond.objects.filter(
                donation=self.object.donation, respondent=self.request.user
            )
            # self.fields['respondent_fake'] = forms.CharField(
            #     label="Respondent", required=True, widget=forms.ModelChoiceField(queryset=respond_qs))
            self.fields['respondent_fake'] = forms.ModelChoiceField(
                queryset=respond_qs, label="Respondent", required=True)
            if respond_qs.exists():
                self.fields['respondent_fake'].initial = respond_qs.first()
        if self.request.user.is_superuser or self.object.donation.user.user == self.request.user:
            if self.object.donation.category == 1 or self.object.donation.category == 0:
                self.fields.pop("respondent_fake")
                self.fields.pop("status_fake")
                if self.request.user.is_superuser:
                    respond_qs = DonationRespond.objects.filter(
                        donation=self.object.donation)
                else:
                    if self.object.donation.user.user == self.request.user and self.object.donation.category == 1:
                        respond_qs = DonationRespond.objects.filter(
                            donation=self.object.donation)
                    if self.object.donation.user.user == self.request.user and self.object.donation.category == 0:
                        respond_qs = DonationRespond.objects.filter(
                            donation=self.object.donation, is_applied_for_selection=True)
                RESPONDENT_QUERYSET = respond_qs
                if respond_qs.exists() and respond_qs.count() >= 1:
                    # if not self.object.donation.blood_bag == None and int(self.object.donation.blood_bag) > 1:
                    #     self.fields['respondent'] = forms.ModelMultipleChoiceField(
                    #         queryset=RESPONDENT_QUERYSET, required=False)
                    # elif not self.object.donation.quantity == None and int(self.object.donation.quantity) > 1:
                    #     self.fields['respondent'] = forms.ModelMultipleChoiceField(
                    #         queryset=RESPONDENT_QUERYSET, required=False)
                    # else:
                    #     self.fields['respondent'] = forms.ModelChoiceField(
                    #         queryset=RESPONDENT_QUERYSET, required=False)
                    self.fields['respondent'] = forms.ModelMultipleChoiceField(
                        queryset=RESPONDENT_QUERYSET, required=False)
                else:
                    # self.fields['respondent'] = forms.ModelChoiceField(
                    #     queryset=RESPONDENT_QUERYSET, empty_label="--- No Respondent Found ---", required=False)
                    self.fields['respondent'] = forms.ModelMultipleChoiceField(
                        queryset=RESPONDENT_QUERYSET, required=False)
            self.fields['respondent'].help_text = "Hold down 'Control', or 'Command' on a Mac, to select more than one"
            self.fields['respondent'].widget.attrs.update({
                'id': 'donation_respondent_input',
                # 'placeholder': 'Type contact number...',
            })
            self.fields['completion_date'].help_text = "Select completion date..."
            self.fields['completion_date'].widget.attrs.update({
                'id': 'donation_completion_date_input',
                # 'placeholder': 'Type contact number...',
            })
            self.fields['management_status'].help_text = "Select management status..."
            self.fields['management_status'].widget.attrs.update({
                'id': 'donation_management_status_input',
                # 'placeholder': 'Type contact number...',
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
        fields = ['progress_status', 'respondent', 'completion_date',
                  'management_status', 'details', 'status_fake', 'respondent_fake']
        exclude = ['donation', 'created_at', 'updated_at', 'is_pending']

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
