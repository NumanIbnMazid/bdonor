from django.urls import path
from .views import checkout, CheckoutListView

urlpatterns = [
    path('payment/<slug>/', checkout, name='checkout'),
    path('checkouts/list/', CheckoutListView.as_view(), name='checkout_list'),
]
