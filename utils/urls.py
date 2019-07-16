from django.urls import path
from .views import (SitePreferenceView,
                    change_site_preference,
                    change_site_preference_default,
                    address_autocomplete_view,
                    hospital_autocomplete_view)

urlpatterns = [
    path('site/preference/', SitePreferenceView.as_view(), name='site_preference'),
    path('site/preference/change/',
         change_site_preference, name='site_preference_change'),
    path('site/preference/change/set-default/',
         change_site_preference_default, name='change_site_preference_default'),
    path('autocomplete/address/', address_autocomplete_view, name='address_autocomplete'),
    path('autocomplete/hospital/', hospital_autocomplete_view, name='hospital_autocomplete'),
]
