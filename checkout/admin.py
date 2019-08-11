from django.contrib import admin
from .models import Checkout

# Register your models here.


class CheckoutAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'created_at', 'updated_at']

    class Meta:
        model = Checkout

admin.site.register(Checkout, CheckoutAdmin)
