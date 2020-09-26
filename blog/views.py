from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post
from .forms import EmailPostForm


def post_list(request, posts_on_page=3):
    # posts = Post.published.all()
    published_posts = Post.published.all()
    paginator = Paginator(published_posts, posts_on_page)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        # If the page number passed in the request is greater than the number of existing page numbers.
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year,
                             publish__month=month, publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})


def post_share(request, post_id):
    # Get Post by id
    # In theory get_object_or_404 using django orm (objects.get)
    # , they are equivalent anyway.
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # Pass data from request to form for validate
        form = EmailPostForm(request.POST)
        # List of validatior errors contain in forms.errors
        if form.is_valid():
            # Contain only valid fields
            cd = form.cleared_data

            # Sending email
            # .get_absolute_url returns the path relative from the application
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f'''{cd['name']} ({cd['email']}) recommends you reading {post.title}'''
            message = f'''Read "{post.title}" at {post.url}\n\n{cd['name']}'s comments:{cd['comments']}'''
            from_email = 'django.framework.email.test@gmail.com'
            send_mail(subject, message, from_email, [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
        return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})
