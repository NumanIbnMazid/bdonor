from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, UserStripe

UserAdmin.list_display += ('is_active',)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'slug', 'account_type', 'gender',
                    'dob', 'blood_group', 'is_volunteer', 'created_at', 'updated_at']

    class Meta:
        model = UserProfile


class UserStripeAdmin(admin.ModelAdmin):
    list_display = ['user', 'stripe_id', 'created_at', 'updated_at']

    class Meta:
        model = UserStripe


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserStripe, UserStripeAdmin)
