from django.urls import path, include
from .views import ProfileDetailView, ProfileUpdateView, UserListView

urlpatterns = [
    path('', include('allauth.urls')),
    path('users/', UserListView.as_view(), name='user_list'),
    path('profile/<slug>/view/',
         ProfileDetailView.as_view(), name='profile_details'),
    path('profile/<slug>/update/',
         ProfileUpdateView.as_view(), name='profile_update'),
]
