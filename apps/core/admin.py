from django.contrib import admin
from .models import SiteConfig, SocialLink


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Identidad', {
            'fields': ('site_name', 'site_tagline', 'logo', 'logo_dark', 'favicon')
        }),
        ('Contacto', {
            'fields': ('email', 'phone', 'address', 'city')
        }),
        ('SEO Global', {
            'fields': ('default_meta_title', 'default_meta_description')
        }),
        ('Analítica', {
            'fields': ('google_analytics_id', 'facebook_pixel_id')
        }),
        ('Tienda', {
            'fields': ('free_shipping_threshold', 'shipping_cost', 'currency', 'currency_symbol')
        }),
        ('Sistema', {
            'fields': ('maintenance_mode',)
        }),
    )

    def has_add_permission(self, request):
        return not SiteConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ['platform', 'url', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active']
