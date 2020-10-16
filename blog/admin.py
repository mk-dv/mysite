from django.contrib import admin

from blog.models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # TODO: перевести эти комментарии
    # Отображать эти поля
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    # Добавляет справа панель для фильтрации по указанным полям, при этом
    # отображаются только поля включ разные значения.
    list_filter = ('status', 'created', 'publish', 'author')
    # Добавляет панель поиска(строка поиска добавляется для моделей с
    # определённым attr search_fields).
    search_fields = ('title', 'body')
    # При добавлении записи - слаг берёт val из поля title. Поле заполняется
    # прямо во время заполнения поля title при создании
    # записи(с небольшой задержкой), при этом для слага используется транслит.
    prepopulated_fields = {'slug': ('title',)}
    # Заменяет lst выбора на строку поиска.
    raw_id_fields = ('author',)
    # Добавляет под строкой поиска ссылки навигации по дате.
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
