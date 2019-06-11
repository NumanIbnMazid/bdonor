from django import forms


class ComposeForm(forms.Form):
    message = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "id": "chat_box_input",
                'rows': 2,
                'cols': 2,
                'maxlength': 450
            }
        )
    )
