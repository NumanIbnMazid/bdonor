from django.urls import path
from .views import checkout

urlpatterns = [
    path('payment/<slug>/', checkout, name='checkout'),
]