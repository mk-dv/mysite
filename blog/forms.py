from django import forms


class EmailPostForm(forms.Form):
    """
    Types of fields define validation.
    If entered data is invalid will be throw forms.ValidationError.
    """
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)