from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
    verbose_name = 'Configuración del sitio'

    def ready(self):
        from django.apps import apps
        from django.db.models import ImageField
        from django.db.models.signals import post_save

        from apps.core.images import ensure_variants

        def generate_variants(sender, instance, **kwargs):
            try:
                ensure_variants(instance)
            except Exception:
                import logging
                logging.getLogger(__name__).exception("No se pudieron generar las fotos reducidas")

        for model in apps.get_models():
            if any(isinstance(field, ImageField) for field in model._meta.fields):
                post_save.connect(
                    generate_variants,
                    sender=model,
                    dispatch_uid=f"opt-images-{model._meta.label}",
                )
