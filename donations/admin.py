from django.contrib import admin
from .models import Donation, DonationProgress


class DonationAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user', 'slug', 'category',
                    'type', 'priority', 'created_at', 'updated_at']

    class Meta:
        model = Donation


class DonationProgressAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'progress_status',
                    'management_status', 'created_at', 'updated_at']

    class Meta:
        model = DonationProgress


admin.site.register(Donation, DonationAdmin)
admin.site.register(DonationProgress, DonationProgressAdmin)
