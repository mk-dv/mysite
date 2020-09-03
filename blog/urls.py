from django.urls import path

from . import views


# Define an application namespace for grouping URLs and using their names to access them.
# For example - access to app templates using namespaces.
# Details: https://docs.djangoproject.com/en/2.0/topics/http/urls/#url-namespaces
app_name = 'blog'

urlpatterns = [
    # Post views
    path('', views.post_list, name='post_list'),
    # Any values, define as a <parameter> returns as a string.
    # <[converter]:parameter> explicitly indicates that the value should be retrieved as a specific types.
    # Details: https://docs.djangoproject.com/en/2.0/topics/http/urls/#path-converters
    # Alternate: re_path(), details: https://docs.django-project.com/en/2.0/ref/urls/#django.urls.re_path
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
]