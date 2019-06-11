self.fields['title'].help_text = "Maximum 50 characters allowed. Keep it short. Only '_A-z0-9+-.,' these characters and spaces are allowed."
self.fields['title'].widget.attrs.update({
    'placeholder': 'Give a title to your post...',
    'id': 'donation_title_input',
    'maxlength': 50,
    'pattern': "^[_A-z0-9 +-.,]{1,}$"
})

def clean_title(self):
    title = self.cleaned_data.get('title')
    if not title == None:
        allowed_chars = re.match(r'^[_A-z0-9 +-.,]+$', title)
        length = len(title)
        if not allowed_chars:
            raise forms.ValidationError(
                "Only '_A-z0-9+-.,' these characters and spaces are allowed.")
        if length > 50:
            raise forms.ValidationError("Maximum 50 characters allowed.")
    return title