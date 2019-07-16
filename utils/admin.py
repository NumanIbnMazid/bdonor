from django.contrib import admin
from .models import SitePreference, Location, Notification


class SitePreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'logo_header_color', 'navbar_header_color',
                    'sidebar_color', 'background_color', 'sidebar_type', 'scroll_to_top', 'chat_with_others', 'created_at', 'updated_at']

    class Meta:
        model = SitePreference


class LocationAdmin(admin.ModelAdmin):
    list_display = ['provider', 'location_type', 'location', 'hit', 'created_at', 'updated_at']

    class Meta:
        model = Location


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'slug', 'category', 'identifier', 'subject']

    class Meta:
        model = Notification


admin.site.register(SitePreference, SitePreferenceAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Notification, NotificationAdmin)
