from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'variant_info', 'sku', 'quantity', 'unit_price', 'total_price']
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'email', 'city', 'total_display',
                    'status_badge', 'payment_status', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['order_number', 'first_name', 'last_name', 'email', 'phone']
    readonly_fields = ['order_number', 'created_at', 'updated_at', 'subtotal', 'total']
    inlines = [OrderItemInline]
    save_on_top = True
    date_hierarchy = 'created_at'
    actions = ['mark_processing', 'mark_shipped', 'mark_delivered', 'mark_cancelled']

    fieldsets = (
        ('Pedido', {
            'fields': ('order_number', 'status', 'admin_notes')
        }),
        ('Cliente', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Envío', {
            'fields': ('country', 'department', 'city', 'address', 'postal_code', 'notes',
                       'tracking_number', 'carrier')
        }),
        ('Totales', {
            'fields': ('subtotal', 'shipping_cost', 'discount', 'total')
        }),
        ('Pago', {
            'fields': ('payment_method', 'payment_status', 'wompi_transaction_id', 'paid_at')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at', 'shipped_at'),
            'classes': ('collapse',)
        }),
    )

    def status_badge(self, obj):
        colors = {
            'pending': '#f39c12',
            'paid': '#27ae60',
            'processing': '#3498db',
            'shipped': '#9b59b6',
            'delivered': '#1abc9c',
            'cancelled': '#e74c3c',
            'refunded': '#95a5a6',
        }
        color = colors.get(obj.status, '#666')
        return format_html(
            '<span style="background:{};color:#fff;padding:3px 10px;border-radius:20px;font-size:12px;font-weight:600;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Estado'

    def total_display(self, obj):
        return format_html('<strong>${:,.0f}</strong>', obj.total)
    total_display.short_description = 'Total'

    def mark_processing(self, request, queryset):
        queryset.update(status=Order.STATUS_PROCESSING)
    mark_processing.short_description = 'Marcar como: En preparación'

    def mark_shipped(self, request, queryset):
        queryset.update(status=Order.STATUS_SHIPPED, shipped_at=timezone.now())
    mark_shipped.short_description = 'Marcar como: Enviado'

    def mark_delivered(self, request, queryset):
        queryset.update(status=Order.STATUS_DELIVERED)
    mark_delivered.short_description = 'Marcar como: Entregado'

    def mark_cancelled(self, request, queryset):
        queryset.update(status=Order.STATUS_CANCELLED)
    mark_cancelled.short_description = 'Marcar como: Cancelado'
