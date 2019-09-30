from django.urls import path
from .views import (
    DonationBankCreateView, BankDashboardView, DonationBankDetailView, DonationBankUpdateView,
    DonationBankListView, donationBank_delete, ManageProgressStatus, member_request_create, DonationBankSettingUpdateView,
    member_request_delete, member_request_accept, member_request_reject, BankMembersListView,
    membership_remove, DonationCreateView, DonationListView, DonationDetailView, DonationUpdateView,
    donation_delete, DonationRequestCreateView, CampaignCreateView, CampaignListView, CampaignDetailView, 
    CampaignUpdateView, campaign_delete, CampaignPublicListView,
)

urlpatterns = [
    path('create/', DonationBankCreateView.as_view(), name='bank_create'),
    path('update/settings/', DonationBankSettingUpdateView.as_view(),
         name='bank_setting_update'),
    path('dashboard/', BankDashboardView.as_view(), name='bank_dashboard'),
    path('<slug>/details/', DonationBankDetailView.as_view(), name='bank_details'),
    path('<slug>/update/', DonationBankUpdateView.as_view(), name='bank_update'),
    path('list/', DonationBankListView.as_view(), name='bank_list'),
    path('delete/', donationBank_delete, name='bank_delete'),
    path('member-request/send/', member_request_create, name='bank_member_request_create'),
    path('member-request/delete/', member_request_delete, name='bank_member_request_delete'),
    path('member-request/accept/', member_request_accept, name='bank_member_request_accept'),
    path('member-request/reject/', member_request_reject, name='bank_member_request_reject'),
    path('members/list/', BankMembersListView.as_view(), name='bank_members_list'),
    path('membership/remove/', membership_remove, name='bank_membership_remove'),
    # Donation OF Bank
#     Donation Store
    path('donation/add/', DonationCreateView.as_view(), name='bank_add_donation'),
    path('donation/list/', DonationListView.as_view(), name='bank_donation_list'),
    path('donation/<slug>/info/', DonationDetailView.as_view(), name='bank_donation_details'),
    path('donation/<slug>/update/', DonationUpdateView.as_view(), name='bank_donation_update'),
    path('donation/delete/', donation_delete, name='bank_donation_delete'),
    path('donation/<slug>/progress/', ManageProgressStatus.as_view(), name='bank_manage_progress_status'),
#     Donation Request
    path('donation/add/request/', DonationRequestCreateView.as_view(), name='bank_add_donation_request'),
    # Campaign URLs
    path('campaign/add/', CampaignCreateView.as_view(), name='bank_add_campaign'),
    path('campaign/list/', CampaignListView.as_view(), name='bank_campaign_list'),
    path('campaign/list/public/', CampaignPublicListView.as_view(),
         name='bank_campaign_list_public'),
    path('campaign/<slug>/info/', CampaignDetailView.as_view(),
         name='bank_campaign_details'),
    path('campaign/<slug>/update/', CampaignUpdateView.as_view(),
         name='bank_campaign_update'),
    path('campaign/delete/', campaign_delete, name='bank_campaign_delete'),
]
