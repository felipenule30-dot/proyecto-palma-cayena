from django import template

from apps.core.images import resized_url

register = template.Library()


@register.filter
def photo(url, width):
    return resized_url(url, width)
