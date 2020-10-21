"""Application routes.

Attributes:
    appname (int): Define an application namespace for grouping URLs and using
        their names to access them. For example - access to app templates using
        namespaces. Details:
        https://docs.djangoproject.com/en/2.0/topics/http/urls/#url-namespaces
    urlpatterns (list): List of application routes.
"""
from django.urls import path

from . import views
from .feeds import LatestPostsFeed

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail,
         name='post_detail'),
    path('<int:post_id>/share/', views.post_share_by_email, name='post_share'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search'),
]
