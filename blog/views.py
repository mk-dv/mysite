from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.shortcuts import render, get_object_or_404

from taggit.models import Tag

from .forms import EmailPostForm, CommentForm
from .models import Post


# TODO(mk-dv): Check comments in this file for grammar.
# TODO(mk-dv): Add a docstring
def post_list(request, posts_on_page=3, tag_slug=None):
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


# TODO(mk-dv): Add a docstring
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year, publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active=True)
    new_comment = None
    comment_form = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create comment
            new_comment = comment_form.save(commit=False)
            # Link comment to current post
            new_comment.post = post
            new_comment.save()
        else:
            # if form is invalid - return form
            comment_form = CommentForm()
    # Forming similar posts list.
    post_tags_ids = post.tags.values_list('id', flat=True)
    all_posts_with_same_tags = Post.published.filter(tags__in=post_tags_ids)
    similar_posts = all_posts_with_same_tags.exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))
    # TODO(mk-dv): Remove magic number.
    similar_posts = similar_posts.order_by('-same_tags', '-publish')[:4]
    return render(request, 'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form,
                   'similar_posts': similar_posts})


# TODO(mk-dv): Add a docstring
def post_share(request, post_id):
    # Get Post object by id. In theory get_object_or_404 using django orm
    # (objects.get), they are equivalent anyway.
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # Pass data from request to form for validate
        form = EmailPostForm(request.POST)
        # List of validation errors contain in forms.errors
        if form.is_valid():
            # Contain only valid fields
            cd = form.cleaned_data

            # Sending email
            # get_absolute_url() returns the path relative from the application.
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = (f"{cd['name']} ({cd['email']}) recommends you reading "
                       f"{post.title}")
            message = (f'Read "{post.title}" at {post_url}\n\n'
                       f"{cd['name']}'s comments:{cd['comments']}")
            from_email = 'django.framework.email.test@gmail.com'
            send_mail(subject, message, from_email, [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html',
                  {'post': post, 'form': form, 'sent': sent})
