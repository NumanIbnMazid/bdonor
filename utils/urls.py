from django.urls import path
from .views import (SitePreferenceView, change_site_preference, change_site_preference_default,
                    address_autocomplete_view, hospital_autocomplete_view,
                    NotificationListView, NotificationDetailView, mark_all_as_read,
                    update_user_country
                    )

urlpatterns = [
     path('site/preference/', SitePreferenceView.as_view(), name='site_preference'),
     path('site/preference/change/',
          change_site_preference, name='site_preference_change'),
     path('site/preference/change/set-default/',
          change_site_preference_default, name='change_site_preference_default'),
     path('autocomplete/address/', address_autocomplete_view,
          name='address_autocomplete'),
     path('autocomplete/hospital/', hospital_autocomplete_view,
          name='hospital_autocomplete'),
     path('set/user/country/', update_user_country,
          name='update_user_country'),
     path('notification/list/', NotificationListView.as_view(),
          name='notification_list'),
     path('notification/<slug>/details/', NotificationDetailView.as_view(),
          name='notification_details'),
     path('notification/mark-all/read/', mark_all_as_read,
          name='notification_mark_all_read'),
]
