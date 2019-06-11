from django.contrib import admin
from .models import SitePreference


class SitePreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'logo_header_color', 'navbar_header_color',
                    'sidebar_color', 'background_color', 'sidebar_type', 'scroll_to_top', 'chat_with_others', 'created_at', 'updated_at']

    class Meta:
        model = SitePreference


admin.site.register(SitePreference, SitePreferenceAdmin)
