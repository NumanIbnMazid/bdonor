from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, UserStripe, UserReport

UserAdmin.list_display += ('is_active',)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'slug', 'account_type', 'gender',
                    'dob', 'blood_group', 'created_at', 'updated_at']

    class Meta:
        model = UserProfile


class UserStripeAdmin(admin.ModelAdmin):
    list_display = ['user', 'stripe_id', 'created_at', 'updated_at']

    class Meta:
        model = UserStripe


class UserReportAdmin(admin.ModelAdmin):
    list_display = ['user', 'reported_by', 'slug',
                    'category', 'created_at', 'updated_at']

    class Meta:
        model = UserReport


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserStripe, UserStripeAdmin)
admin.site.register(UserReport, UserReportAdmin)
