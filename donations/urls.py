from django.urls import path
from .views import (OfferDonationCreateView,
                    MyDonationOffersListView, DonationOffersListView,
                    DonationDetailView, OfferDonationUpdateView, donation_delete,
                    DonationRespondCreateView, withdraw_respond)

urlpatterns = [
    path('offer/', OfferDonationCreateView.as_view(), name='offer_donation'),
    path('my/offers/', MyDonationOffersListView.as_view(),
         name='my_donation_offers'),
    path('offers/', DonationOffersListView.as_view(), name='donation_offers'),
    path('<slug>/details/', DonationDetailView.as_view(), name='donation_details'),
    path('<slug>/update/', OfferDonationUpdateView.as_view(), name='donation_update'),
    path('delete/', donation_delete, name='donation_delete'),
    path('respond/<slug>/', DonationRespondCreateView.as_view(), name='donation_respond_create'),
    path('withdraw/response/', withdraw_respond, name='withdraw_respond'),
]
