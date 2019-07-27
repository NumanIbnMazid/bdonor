from django.urls import path
from .views import (OfferDonationCreateView,
                    MyDonationOffersListView, DonationOffersCardListView, DonationOffersListView,
                    DonationDetailView, OfferDonationUpdateView, donation_delete,
                    DonationRespondCreateView, withdraw_respond, DonationFilteredListView,
                    DonationRequestCreateView, DonationRequestUpdateView,
                    MyDonationRequestsListView, DonationRequestsCardListView, DonationRequestsListView,
                    ManageProgressStatus,)

urlpatterns = [
    path('offer/', OfferDonationCreateView.as_view(), name='offer_donation'),
    path('my/offers/', MyDonationOffersListView.as_view(),
         name='my_donation_offers'),
    path('offers/list/card/', DonationOffersCardListView.as_view(),
         name='donation_offers_list_card'),
    path('offers/list/', DonationOffersListView.as_view(),
         name='donation_offers_list'),
    path('offer/<slug>/update/', OfferDonationUpdateView.as_view(),
         name='donation_update'),
    # Donation Requests
    path('request/', DonationRequestCreateView.as_view(), name='request_donation'),
    path('my/requests/', MyDonationRequestsListView.as_view(),
         name='my_donation_requests'),
    path('requests/list/card/', DonationRequestsCardListView.as_view(),
         name='donation_requests_list_card'),
    path('requests/list/', DonationRequestsListView.as_view(),
         name='donation_requests_list'),
    path('request/<slug>/update/', DonationRequestUpdateView.as_view(),
         name='donation_request_update'),
    # Donation Mixed Request + Offer
    path('delete/', donation_delete, name='donation_delete'),
    path('respond/<slug>/', DonationRespondCreateView.as_view(),
         name='donation_respond_create'),
    path('withdraw/response/', withdraw_respond, name='withdraw_respond'),
    path('<slug>/details/', DonationDetailView.as_view(), name='donation_details'),
    path('<slug>/progress-status/', ManageProgressStatus.as_view(), name='donation_progress'),
    # Donation Filter
    path('filter/', DonationFilteredListView.as_view(), name='donation_filter'),
]
