from django.contrib import admin

from blog.models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """


    """
    # Show these fields.
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    # Adds a panel to the right for filtering by the specified fields, with only
    # fields containing different values.
    list_filter = ('status', 'created', 'publish', 'author')
    # Adds search bar (search bar is added only for models specified in
    # 'search_fields').
    search_fields = ('title', 'body')
    # When adding a record (in the admin panel) - the slug takes value from the
    # title field. The field is filled in right when filling the title field
    # when creating a post (with a delay), wherein transliteration is used for
    # the slug.
    prepopulated_fields = {'slug': ('title',)}
    # Replaces a dropdown selection list with a search box.
    raw_id_fields = ('author',)
    # Adds date navigation links below the search bar.
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
