# TODO(mk-dv): Translate comments.
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords

from .models import Post


# TODO(mk-dv): Add a docstring.
class LatestPostsFeed(Feed):
    """Feed is the Django feed subsystem class. The attributes will be
     represented by RSS elements (XML tags) with corresponding names.

    Attributes:
        title:
        link:
        description:
    """

    title = 'My blog'
    link = '/blog/'
    description = 'New posts of my blog.'

    # TODO(mk-dv): This method does not seem to sort posts by date.
    @staticmethod
    def items():
        """Gets objects to be included in the RSS feed.

        Returns:
            A "QuerySet" with 5 published posts.
        """
        return Post.published.all()[:5]

    def item_title(self, item):
        """Получает title для каждого object возвращаемого items()."""
        return item.title

    def item_description(self, item):
        """Получает description для каждого object возвращаемого items()."""
        return truncatewords(item.body, 30)
