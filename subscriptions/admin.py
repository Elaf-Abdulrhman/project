from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'user', 'amount', 'status', 'created_at')
    search_fields = ('payment_id', 'user__username', 'status')
    list_filter = ('status', 'created_at')
