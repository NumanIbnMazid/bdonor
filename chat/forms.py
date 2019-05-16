from django import forms


class ComposeForm(forms.Form):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                'rows': 2,
                'cols': 2,
                'maxlength': 450
            }
        )
    )
