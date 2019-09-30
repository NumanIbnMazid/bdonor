from django.contrib import admin
from .models import Donation, DonationProgress, DonationUtil, DonationRespond


class DonationAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user', 'slug', 'category',
                    'type', 'donate_type', 'priority', 'created_at', 'updated_at']

    class Meta:
        model = Donation


class DonationProgressAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'get_donation_user', 'get_respondents', 'progress_status',
                    'management_status', 'created_at', 'updated_at']

    class Meta:
        model = DonationProgress


class DonationUtilAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user', 'created_at', 'updated_at']

    class Meta:
        model = DonationUtil


class DonationRespondAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'donation', 'respondent', 'contact', 'created_at', 'updated_at']

    class Meta:
        model = DonationRespond


admin.site.register(Donation, DonationAdmin)
admin.site.register(DonationProgress, DonationProgressAdmin)
admin.site.register(DonationUtil, DonationUtilAdmin)
admin.site.register(DonationRespond, DonationRespondAdmin)
