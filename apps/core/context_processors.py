from .models import SiteConfig, SocialLink


def site_config(request):
    config = SiteConfig.get()
    social_links = SocialLink.objects.filter(is_active=True)
    return {
        'site_config': config,
        'social_links': social_links,
    }
