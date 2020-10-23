"""blog application models."""
from taggit.managers import TaggableManager

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class PublishedManager(models.Manager):
    """A custom Model Manager for Post."""

    def get_queryset(self):
        return super().get_queryset().filter(status='PUBLISHED')


class Post(models.Model):
    """Post model.

    Attributes:
        DRAFT (str):
            Constant used in STATUS_CHOICES.
        PUBLISHED (str):
            Constant used in STATUS_CHOICES.
        STATUS_CHOICES (tuple):
            Choices for 'status'.
        title (CharField):
            Post title.
        slug (SlugField):
            Post slug. Can contain characters, numbers, hyphens, and
            underscores.
        author (ForeignKey):
            Post author.
        body (TextField):
            Post body.
        publish (DateTimeField):
            Post publish.
        created (DateTimeField):
            Post created.
        updated (DateTimeField):
            Post updated.
        status (CharField):
            Post status.
        objects (Manager):
            Default Django object-relation manager.
        published (PublishedManager):
            Custom object-relation manager.
        tags (TaggableManager):
            Post tags manager.
    """
    DRAFT = 'DRAFT'
    PUBLISHED = 'PUBLISHED'
    STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default=DRAFT)

    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()

    class Meta:
        ordering = ('-publish', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year, self.publish.month,
                             self.publish.day, self.slug])


class Comment(models.Model):
    """A user comment model for a post.

    Attributes:
        post (ForeignKey):
            The post to which the comment belongs.
        name (CharField):
            Commenter name.
        email (TextField):
            Commenter email.
        body (TextField):
            Comment body.
        created (DateTimeField):
            The time the comment were created.
        active (BooleanField):
            Comment display state. True - show the comment.
    """
    # A related_name allows access to article comments ('post.comments.all()')
    # , in addition to accessing the article from a comment ('comment.post').
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE,
        related_name='comments'
    )
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
