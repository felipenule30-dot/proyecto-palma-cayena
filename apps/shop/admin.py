from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Collection, Color, Size, Tag, Product, ProductImage, ProductVariant


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'order', 'product_count']
    list_editable = ['is_active', 'order']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Productos'


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'is_featured', 'order', 'product_count']
    list_editable = ['is_active', 'is_featured', 'order']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Productos'


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'color_preview', 'hex_code', 'order']
    list_editable = ['hex_code', 'order']

    def color_preview(self, obj):
        if obj.hex_code:
            return format_html(
                '<span style="display:inline-block;width:20px;height:20px;background:{};border-radius:50%;border:1px solid #ccc;"></span>',
                obj.hex_code
            )
        return '—'
    color_preview.short_description = 'Color'


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'order']
    list_editable = ['order']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text', 'is_main', 'order', 'image_preview']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px;object-fit:cover;border-radius:4px;">', obj.image.url)
        return '—'
    image_preview.short_description = 'Vista previa'


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ['size', 'color', 'sku', 'stock', 'price_override', 'is_active']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_thumb', 'name', 'category', 'collection', 'price', 'status',
                    'is_featured', 'is_new', 'stock_total', 'created_at']
    list_display_links = ['product_thumb', 'name']
    list_editable = ['status', 'is_featured', 'is_new']
    list_filter = ['status', 'is_featured', 'is_new', 'is_bestseller', 'category', 'collection']
    search_fields = ['name', 'sku', 'description']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['tags', 'colors', 'sizes']
    inlines = [ProductImageInline, ProductVariantInline]
    save_on_top = True
    fieldsets = (
        ('Información básica', {
            'fields': ('name', 'slug', 'sku', 'category', 'collection', 'tags')
        }),
        ('Descripción', {
            'fields': ('short_description', 'description', 'care_instructions', 'composition')
        }),
        ('Precios', {
            'fields': ('price', 'compare_price')
        }),
        ('Variantes disponibles', {
            'fields': ('colors', 'sizes')
        }),
        ('Estado y visibilidad', {
            'fields': ('status', 'is_featured', 'is_new', 'is_bestseller', 'order')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'og_image'),
            'classes': ('collapse',)
        }),
    )

    def product_thumb(self, obj):
        img = obj.main_image
        if img:
            return format_html('<img src="{}" style="height:50px;width:50px;object-fit:cover;border-radius:6px;">', img.image.url)
        return '—'
    product_thumb.short_description = ''

    def stock_total(self, obj):
        total = sum(v.stock for v in obj.variants.all())
        color = '#27ae60' if total > 0 else '#e74c3c'
        return format_html('<span style="color:{};font-weight:600;">{}</span>', color, total)
    stock_total.short_description = 'Stock'
