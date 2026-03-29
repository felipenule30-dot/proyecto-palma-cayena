from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['reference', 'order', 'gateway', 'amount', 'status', 'created_at']
    list_filter = ['status', 'gateway', 'created_at']
    search_fields = ['reference', 'transaction_id', 'order__order_number']
    readonly_fields = ['created_at', 'updated_at', 'gateway_response']
