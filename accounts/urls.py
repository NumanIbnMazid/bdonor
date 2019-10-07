from django.urls import path, include
from .views import (ProfileDetailView, ProfileUpdateView, UserListView,
                    UserReportCreateView, UserReportListView, UserReportDetailView,
                    SingleUserReportListView, report_delete, report_delete_all,
                    UserPermissionListView, UserPermissionUpdateView
)


urlpatterns = [
     path('', include('allauth.urls')),
     path('users/', UserListView.as_view(), name='user_list'),
     path('profile/<slug>/view/',
          ProfileDetailView.as_view(), name='profile_details'),
     path('profile/<slug>/update/',
          ProfileUpdateView.as_view(), name='profile_update'),
     # User Report
     path('user/<slug>/report/create/', UserReportCreateView.as_view(), name= 'user_report_create'),
     path('users/reports/list/', UserReportListView.as_view(),
          name='user_report_list'),
     path('user/report/<slug>/details/',
          UserReportDetailView.as_view(), name='user_report_detail'),
     path('user/<slug>/reports/',
          SingleUserReportListView.as_view(), name='user_report_list_single'),
     path('report/delete/', report_delete, name='user_report_delete'),
     path('report/delete/all/', report_delete_all, name='user_report_delete_all'),
     # User Permissions
     path('users/permissions/list/', UserPermissionListView.as_view(),
          name='user_permission_list'),
     path('user/<slug>/permissions/update/', UserPermissionUpdateView.as_view(),
          name='user_permission_update'),
]
