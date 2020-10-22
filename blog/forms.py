"""Custom forms. Types of fields define validation. If entered data is invalid
will be throw forms.ValidationError.

"""
from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    """A user comment form for a post."""

    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


class EmailPostForm(forms.Form):
    """Form for share a Post by email.

    Attributes:
        name(CharField): Email sender name.
        email(EmailField): Sender email for reply.
        destination(EmailField): Recipient's mail.
        comments(CharField): Comment for email.
    """
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    destination = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class SearchForm(forms.Form):
    """Search form for posts on the site.

    Attributes:
        query: A CharField with user search query.
    """
    query = forms.CharField(label='')