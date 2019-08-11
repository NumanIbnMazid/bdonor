from django.contrib import admin
from .models import Plan


class PlanAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'amount', 'currency',
                    'expiration_cycle', 'created_at', 'updated_at']

    class Meta:
        model = Plan


admin.site.register(Plan, PlanAdmin)
