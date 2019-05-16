from allauth.account.adapter import DefaultAccountAdapter
from django.forms import ValidationError

class UsernameMaxAdapter(DefaultAccountAdapter):

    def clean_username(self, username, shallow=False):
        if len(username) >= 15:
            raise ValidationError('Please enter a username less than 15 characters')
        return DefaultAccountAdapter.clean_username(self,username) # For other default validations.