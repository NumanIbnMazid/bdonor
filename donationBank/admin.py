from django.contrib import admin
from .models import (DonationBank, DonationBankSetting, BankMember, MemberRequest,
                     Donation, DonationRequest, DonationProgress, Campaign, DonationRequestProgress
                     )


class DonationBankAdmin(admin.ModelAdmin):
    list_display = ['institute', 'city',
                    'state', 'country', 'contact', 'email', 'services', 'is_verified']

    class Meta:
        model = DonationBank


class DonationBankSettingAdmin(admin.ModelAdmin):
    list_display = ['bank', 'member_request', 'privacy', 'created_at', 'updated_at']

    class Meta:
        model = DonationBankSetting


class BankMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'bank', 'role', 'created_at', 'updated_at']

    class Meta:
        model = BankMember


class MemberRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'bank', 'created_at', 'updated_at']

    class Meta:
        model = MemberRequest


class DonationAdmin(admin.ModelAdmin):
    list_display = ['bank', 'first_name', 'last_name', 'gender', 'blood_group',
                    'country', 'donation_type']

    class Meta:
        model = Donation


class DonationRequestAdmin(admin.ModelAdmin):
    list_display = ['bank', 'slug', 'donation_type', 'blood_group']

    class Meta:
        model = DonationRequest


class DonationProgressAdmin(admin.ModelAdmin):
    list_display = ['donation', 'progress_status', 'completion_date']

    class Meta:
        model = DonationProgress


class DonationRequestProgressAdmin(admin.ModelAdmin):
    list_display = ['donation', 'progress_status', 'completion_date']

    class Meta:
        model = DonationRequestProgress


class CampaignAdmin(admin.ModelAdmin):
    list_display = ['bank', 'title', 'held_date',
                    'end_date', 'contact', 'country']

    class Meta:
        model = Campaign


admin.site.register(DonationBank, DonationBankAdmin)
admin.site.register(DonationBankSetting, DonationBankSettingAdmin)
admin.site.register(BankMember, BankMemberAdmin)
admin.site.register(MemberRequest, MemberRequestAdmin)
admin.site.register(Donation, DonationAdmin)
admin.site.register(DonationRequest, DonationRequestAdmin)
admin.site.register(DonationProgress, DonationProgressAdmin)
admin.site.register(DonationRequestProgress, DonationRequestProgressAdmin)
admin.site.register(Campaign, CampaignAdmin)
