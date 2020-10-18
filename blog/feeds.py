# TODO(mk-dv): Translate comments.
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords

from .models import Post

# TODO(mk-dv): Add a docstring.
class LatestPostsFeed(Feed):
    # Feed - класс подсистемы фидов Django. Атрибуты будут представлены RSS
    # элементами(XML тегами) с соответствующими именами.
    title = 'My blog'
    link = '/blog/'
    description = 'New posts of my blog.'

    # TODO(mk-dv): Translate TODO
    # TODO(mk-dv): Кажется этот менеджер не сортирует посты по дате
    # Получает объекты включаемые в рассылку
    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        """Получает title для каждого object возвращаемого items()."""
        return item.title

    def item_description(self, item):
        """Получает description для каждого object возвращаемого items()."""
        return truncatewords(item.body, 30)