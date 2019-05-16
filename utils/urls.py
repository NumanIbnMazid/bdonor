from django.urls import path
from .views import SitePreferenceView, change_site_preference, change_site_preference_default

urlpatterns = [
    path('site/preference/', SitePreferenceView.as_view(), name='site_preference'),
    path('site/preference/change/',
         change_site_preference, name='site_preference_change'),
    path('site/preference/change/set-default/',
         change_site_preference_default, name='change_site_preference_default')
]
