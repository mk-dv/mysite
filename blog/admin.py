"""Django admin panel configuration."""
from django.contrib import admin

from blog.models import Post, Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Register the user comment model in the admin panel.

    Attributes:
        list_display (tuple[str]):
            Names of displayed fields.
        list_filter (tuple[str]):
            Adds a panel to the right to filter by the specified field names
            (only fields with different values are used).
        search_fields (tuple[str]):
            A tuple of strings fields names. Add a search bar for search by
            specified fields.
    """
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Register the Post model in the admin panel.

    Attributes:
        date_hierarchy (str):
            Adds date navigation links below the search bar.
        list_display (tuple[str]):
            Names of displayed fields.
        list_filter (tuple[str]):
            Adds a panel to the right to filter by the specified field names
            (only fields with different values are used).
        prepopulated_fields (dict[str, tuple]):
            When adding a record (in the admin panel) - the slug takes the value
            from the header field. The field is filled in immediately when
            filling in the header field when creating a post (with a delay),
            while transliteration is used for the slug.
        raw_id_fields (tuple[str]):
            Replaces a specified field widget with a search box with raw data.
        search_fields (tuple[str]):
            A tuple of strings fields names. Add a search bar for search by
            specified fields.
    """
    date_hierarchy = 'publish'
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    ordering = ('status', 'publish')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    search_fields = ('title', 'body')
