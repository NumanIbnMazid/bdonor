from django.contrib import admin
from .models import DonationBank, DonationBankSetting, BankMember, MemberRequest

class DonationBankAdmin(admin.ModelAdmin):
    list_display = ['institute', 'city',
                    'state', 'country', 'contact', 'email']

    class Meta:
        model = DonationBank


class DonationBankSettingAdmin(admin.ModelAdmin):
    list_display = ['bank', 'member_request', 'created_at', 'updated_at']

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

admin.site.register(DonationBank, DonationBankAdmin)
admin.site.register(DonationBankSetting, DonationBankSettingAdmin)
admin.site.register(BankMember, BankMemberAdmin)
admin.site.register(MemberRequest, MemberRequestAdmin)
