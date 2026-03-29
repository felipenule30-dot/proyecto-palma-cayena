from django.db import models
from django.utils.translation import gettext_lazy as _


class SiteConfig(models.Model):
    """Configuración global del sitio — solo debe existir un registro."""
    site_name = models.CharField('Nombre del sitio', max_length=100, default='Palma Cayena')
    site_tagline = models.CharField('Tagline', max_length=200, blank=True, default='Born from the sea.')
    logo = models.ImageField('Logo', upload_to='brand/', blank=True, null=True)
    logo_dark = models.ImageField('Logo oscuro', upload_to='brand/', blank=True, null=True)
    favicon = models.ImageField('Favicon', upload_to='brand/', blank=True, null=True)
    email = models.EmailField('Email de contacto', blank=True, default='hola@palmacayena.com')
    phone = models.CharField('Teléfono', max_length=30, blank=True)
    address = models.TextField('Dirección', blank=True)
    city = models.CharField('Ciudad', max_length=100, blank=True, default='Cartagena, Colombia')
    default_meta_title = models.CharField('Meta title por defecto', max_length=160, blank=True)
    default_meta_description = models.TextField('Meta description por defecto', blank=True)
    google_analytics_id = models.CharField('Google Analytics ID', max_length=50, blank=True)
    facebook_pixel_id = models.CharField('Facebook Pixel ID', max_length=50, blank=True)
    maintenance_mode = models.BooleanField('Modo mantenimiento', default=False)
    free_shipping_threshold = models.DecimalField(
        'Envío gratis desde (COP)', max_digits=12, decimal_places=2, default=250000
    )
    shipping_cost = models.DecimalField(
        'Costo de envío estándar (COP)', max_digits=10, decimal_places=2, default=15000
    )
    currency = models.CharField('Moneda', max_length=10, default='COP')
    currency_symbol = models.CharField('Símbolo de moneda', max_length=5, default='$')

    class Meta:
        verbose_name = 'Configuración del sitio'
        verbose_name_plural = 'Configuración del sitio'

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        # Solo un registro
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SocialLink(models.Model):
    PLATFORM_CHOICES = [
        ('instagram', 'Instagram'),
        ('tiktok', 'TikTok'),
        ('facebook', 'Facebook'),
        ('pinterest', 'Pinterest'),
        ('youtube', 'YouTube'),
        ('whatsapp', 'WhatsApp'),
    ]
    platform = models.CharField('Plataforma', max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField('URL', max_length=300)
    is_active = models.BooleanField('Activo', default=True)
    order = models.PositiveSmallIntegerField('Orden', default=0)

    class Meta:
        verbose_name = 'Red social'
        verbose_name_plural = 'Redes sociales'
        ordering = ['order']

    def __str__(self):
        return f'{self.get_platform_display()}'
