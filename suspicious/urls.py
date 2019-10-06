from django.urls import path
from .views import SuspiciousListView


urlpatterns = [
    path('list/', SuspiciousListView.as_view(),
         name='suspicious_list'),
]
