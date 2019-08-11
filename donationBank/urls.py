from django.urls import path
from .views import (
    DonationBankCreateView, BankDashboardView, DonationBankDetailView, DonationBankUpdateView,
    DonationBankListView, donationBank_delete, member_request_create, DonationBankSettingUpdateView,
    member_request_delete, member_request_accept, member_request_reject, BankMembersListView,
    membership_remove,
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
]
