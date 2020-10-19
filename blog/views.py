from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.shortcuts import render, get_object_or_404

from taggit.models import Tag

from .forms import EmailPostForm, CommentForm
from .models import Post


def post_list(request, posts_on_page=3, tag_slug=None):
    """Displays the main blog page with paginated Post's.

    Args:
        request: An HttpRequest instance.
        posts_on_page: An integer post number on one page.
        tag_slug: Tag for Post filtering.

    Returns:
         A HttpResponse.
    """
    published_posts = Post.published.all()

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        published_posts = published_posts.filter(tags__in=[tag])

    paginator = Paginator(published_posts, posts_on_page)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        # If the page number passed in the request is greater than the number
        # of existing page numbers.
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html',
                  {'page': page, 'posts': posts, 'tag': tag})


def post_detail(request, year, month, day, post):
    """Displays a Post page with comments and a list of similar Posts.

    Args:
        request: A HttpRequest instance.
        year: Integer year of Post Published.
        month: Integer month of Post Published.
        day: Integer day of Post Published.
        post: String Post slug.

    Returns:
         A HttpResponse.
    """
    post = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year, publish__month=month,
                             publish__day=day)

    comments = post.comments.filter(active=True)
    new_comment = None
    comment_form = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create a comment.
            new_comment = comment_form.save(commit=False)
            # Bind a comment to the current post.
            new_comment.post = post
            new_comment.save()
        else:
            # If the form is valid, then return the form with the data.
            comment_form = CommentForm()

    # Forming a similar posts list.
    post_tags_ids = post.tags.values_list('id', flat=True)
    all_posts_with_same_tags = Post.published.filter(tags__in=post_tags_ids)
    other_posts_with_same_tags = all_posts_with_same_tags.exclude(id=post.id)
    # TODO(mk-dv): Get rid of the magic number.
    similar_posts = (other_posts_with_same_tags
                     .annotate(same_tags=Count('tags'))
                     .order_by('-same_tags', '-publish'))[:4]
    return render(request, 'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form,
                   'similar_posts': similar_posts})


def post_share_by_email(request, post_id):
    """Displays a share Post by email page.

    Args:
        request: A HttpRequest instance.
        post_id: An integer Post primary key.

    Returns:
         A HttpResponse.
    """
    # Get a Post object by id. In theory get_object_or_404 uses Django ORM
    # (objects.get), they are equivalent anyway.
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    sent_failed = False
    if request.method == 'POST':
        # Pass data from request to form for validate.
        form = EmailPostForm(request.POST)
        # List of validation errors contain in forms.errors.
        if form.is_valid():
            # Contain only valid fields.
            cd = form.cleaned_data

            # Sending email.
            # get_absolute_url() returns the path relative from the application.
            post_url = request.build_absolute_uri(post.get_absolute_url())

            subject = (f"{cd['name']} ({cd['email']}) recommends you reading "
                       f"{post.title}")

            message = (f'Read "{post.title}" at {post_url}\n\n'
                       f"{cd['name']}'s comments:{cd['comments']}")

            from_email = 'django.framework.email.test@gmail.com'
            try:
                send_mail(subject, message, from_email, [cd['to']])
                sent = True
            except Exception:
                sent_failed = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html',
                  {'post': post, 'form': form, 'sent': sent,
                   'sent_failed': sent_failed})
