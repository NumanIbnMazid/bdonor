from django.urls import path
from .views import (
    BlogPostCreateView, BlogAjaxListView, BlogDetailView, MyPostsAjaxListView,
    BlogPostUpdateView, delete_attachment, blog_delete, create_comment, reply_comment
)

urlpatterns = [
    path('post/create/', BlogPostCreateView.as_view(), name='blog_post_create'),
    path('list/all/', BlogAjaxListView.as_view(), name='blog_list'),
    path('my/posts/', MyPostsAjaxListView.as_view(), name='blog_my_posts_list'),
    path('<slug>/details/', BlogDetailView.as_view(), name='blog_detail'),
    path('<slug>/update/', BlogPostUpdateView.as_view(), name='blog_update'),
    path('attachment/delete/', delete_attachment, name='attachment_delete'),
    path('delete/', blog_delete, name='blog_delete'),
    path('<slug>/comment/create/', create_comment, name='comment_create'),
    path('comment/reply/', reply_comment, name='reply_comment'),
]
