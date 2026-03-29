from django import template
from decimal import Decimal

register = template.Library()


@register.filter
def cop(value):
    """
    Formatea un número como peso colombiano.
    Ejemplo: 180000 → $ 180.000
    """
    try:
        value = Decimal(str(value))
        # Separador de miles con punto (estándar colombiano)
        formatted = f"{int(value):,}".replace(",", ".")
        return f"$ {formatted}"
    except (TypeError, ValueError):
        return value


@register.filter
def cop_full(value):
    """
    Formatea con símbolo y código de moneda.
    Ejemplo: 180000 → $ 180.000 COP
    """
    try:
        value = Decimal(str(value))
        formatted = f"{int(value):,}".replace(",", ".")
        return f"$ {formatted} COP"
    except (TypeError, ValueError):
        return value


@register.filter
def cop_short(value):
    """
    Formato corto sin símbolo para usar en contextos donde ya está el $.
    Ejemplo: 180000 → 180.000
    """
    try:
        value = Decimal(str(value))
        return f"{int(value):,}".replace(",", ".")
    except (TypeError, ValueError):
        return value
