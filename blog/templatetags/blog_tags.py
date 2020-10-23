"""Custom template tags.

Attributes:
    register (template.Library):
        To be a valid tag library, the module must contain a module-level
        variable named 'register' that is a template.Library instance, in which
        all the tags and filters are registered.
"""
import markdown

from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe

from blog.forms import SearchForm
from blog.models import Post

register = template.Library()


@register.simple_tag
def get_most_commented_posts(count=5):
    return (Post.published
                .filter(comments__gt=0)
                .annotate(total_comments=Count('comments'))
                .order_by('-total_comments')[:count])


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    # Including tags must only return a dict type for use in the context of the
    # template.
    return {'latest_posts': latest_posts}


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.simple_tag
def post_search_form():
    return SearchForm()
