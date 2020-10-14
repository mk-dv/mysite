from django.contrib import admin

from blog.models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Отображать эти поля
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    # Добавляет справа панель для фильтрации по указанным полям
    # При этом отображаются только поля включ разные vals
    list_filter = ('status', 'created', 'publish', 'author')
    # Добавляет панель поиска(строка поиска добавляется для моделей с определённым attr search_fields)
    search_fields = ('title', 'body')
    # при добавлении записи - слаг берёт val из поля title
    # Поле заполняется прямо во время заполнения поля title при создании записи(с небольшой задержкой)
    # При этом для слага используется транслит
    prepopulated_fields = {'slug': ('title',)}
    # заменяет lst выбора на строку поиска
    raw_id_fields = ('author',)
    # добавляет под строкой поиска ссылки навигации по дате
    date_hierarchy = 'publish'
    # ordering
    ordering = ('status', 'publish')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
