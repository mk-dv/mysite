from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


class EmailPostForm(forms.Form):
    # Types of fields define validation. If entered data is invalid will be
    # throw forms.ValidationError.
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class SearchForm(forms.Form):
    """Search form for posts on the site.

    Attributes:
        query: A CharField with user search query.
    """
    query = forms.CharField()