"""Used by the Django feed subsystem."""
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords

from .models import Post


class LatestPostsFeed(Feed):
    """Feed is the Django feed subsystem class. The attributes will be
    represented by RSS elements (XML tags) with corresponding names.

    Attributes:
        DESCRIPTION_LONG(int): The number of the first words of the
            description.
        POSTS_COUNT(int): The number of posts in the feed.
        title(str): Feed title.
        link(str): A relative link from root to feed.
        description(str): Feed description.
    """
    DESCRIPTION_LONG = 30
    POSTS_COUNT = 5
    title = 'My blog'
    link = '/blog/'
    description = 'New posts of my blog.'

    @staticmethod
    def items():
        """Get objects to be included in the RSS feed.

        Returns:
            A 'QuerySet' with 5 published posts.
        """
        return Post.published.all()[:POSTS_COUNT]

    def item_title(self, item):
        """Get the title for each object returned by items()."""
        return item.title

    def item_description(self, item):
        """Get the description for each object returned by items()."""
        return truncatewords(item.body, DESCRIPTION_LONG)
