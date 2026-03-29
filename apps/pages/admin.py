from django.contrib import admin
from .models import (StaticPage, HeroSection, HomepageBlock, BenefitItem,
                     Testimonial, FAQ, NewsletterSubscriber, ContactMessage, JournalPost)


@admin.register(StaticPage)
class StaticPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'page_type', 'slug', 'is_published', 'updated_at']
    list_editable = ['is_published']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['page_type', 'is_published']
    search_fields = ['title', 'content']


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'order']
    list_editable = ['is_active', 'order']


@admin.register(HomepageBlock)
class HomepageBlockAdmin(admin.ModelAdmin):
    list_display = ['block_type', 'title', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    list_filter = ['block_type', 'is_active']


@admin.register(BenefitItem)
class BenefitItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'is_active', 'order']
    list_editable = ['is_active', 'order']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'rating', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    list_filter = ['rating', 'is_active']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    list_filter = ['category', 'is_active']
    search_fields = ['question', 'answer']


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'source', 'is_active', 'created_at']
    list_filter = ['is_active', 'source', 'created_at']
    search_fields = ['email', 'name']
    list_editable = ['is_active']
    readonly_fields = ['created_at']
    actions = ['export_emails']

    def export_emails(self, request, queryset):
        from django.http import HttpResponse
        emails = '\n'.join(queryset.values_list('email', flat=True))
        response = HttpResponse(emails, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="subscribers.txt"'
        return response
    export_emails.short_description = 'Exportar emails seleccionados'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['is_read']
    readonly_fields = ['name', 'email', 'phone', 'subject', 'message', 'created_at']


@admin.register(JournalPost)
class JournalPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_published', 'published_at']
    list_editable = ['is_published']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['is_published', 'published_at']
    search_fields = ['title', 'content', 'excerpt']
