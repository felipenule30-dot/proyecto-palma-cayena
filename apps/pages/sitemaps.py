from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import StaticPage, JournalPost


class PageSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return StaticPage.objects.filter(is_published=True)

    def location(self, obj):
        return obj.get_absolute_url()
