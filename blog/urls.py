from django.urls import path
from .views import (
    BlogPostCreateView
)

urlpatterns = [
    path('post/create/', BlogPostCreateView.as_view(), name='blog_post_create'),
]
