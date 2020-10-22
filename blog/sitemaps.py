from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    """Add a sitemap.xml for search engine bots.

    Attributes:
        changefreq: A string update frequency.
        priority: A float priority.
    """
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        """Returns the last update time for each item."""
        return obj.updated
