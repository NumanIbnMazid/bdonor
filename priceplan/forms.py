from django import forms
from .models import Plan
import re


class PlanForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PlanForm, self).__init__(*args, **kwargs)
        self.fields['title'].help_text = "Only '_A-z0-9+-.,' these characters and spaces are allowed."
        self.fields['title'].widget.attrs.update({
            'id': 'plan_title_input',
            'placeholder': 'Enter plan title...',
            'maxlength': 50,
            'pattern': "^[_A-z0-9 +-.,]{1,}$"
        })
        self.fields['amount'].help_text = "Enter plan price."
        self.fields['amount'].widget.attrs.update({
            'id': 'plan_amount_input',
            'placeholder': 'Enter price...',
            'maxlength': 8
        })
        self.fields['currency'].help_text = "Select price currency."
        self.fields['currency'].widget.attrs.update({
            'id': 'plan_currency_input',
        })
        self.fields['expiration_cycle'].help_text = "Select expiration cycle."
        self.fields['expiration_cycle'].widget.attrs.update({
            'id': 'plan_expiration_cycle_input'
        })
        self.fields['description'].help_text = "Enter short description about the price plan."
        self.fields['description'].widget.attrs.update({
            'id': 'plan_description_input',
            'placeholder': 'Enter short description...',
            'maxlength': 100,
            'rows': 2,
            'cols': 2
        })

    class Meta:
        model = Plan
        fields = ['title', 'amount', 'currency',
                  'expiration_cycle', 'description']
        exclude = ['slug', 'created_at', 'updated_at']

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

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if not amount == None:
            if not amount >= 0:
                raise forms.ValidationError(
                    f"Please enter a valid amount and it must be a positive value.")
        return amount

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description == None:
            length = len(description)
            if length > 100:
                raise forms.ValidationError(
                    f"Maximum 100 characters allowed. [currently using: {length}]")
        return description
