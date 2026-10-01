from django.db import migrations


HERO_TITLE = "For slow mornings, salty skin & golden afternoons."
HERO_SUBTITLE = "Crafted by Colombian hands."

TESTIMONIALS = [
    (
        "Saso - Cata",
        "Me encantan los enterizos: la tela es gruesa y de una horma espectacular, "
        "así que estilizan el cuerpo y quedan tan bien que los uso también como body "
        "con jeans. Se sienten firmes y se ven impecables dentro y fuera del agua.",
    ),
    (
        "Male",
        "La calidad de la tela es lo que más me conquistó. Se siente suave pero "
        "resistente, no se transparenta ni pierde la forma, y después de varios usos "
        "sigue como nueva.",
    ),
    (
        "Isa",
        "Me enamoré de lo colorido y a la vez elegante de cada diseño. Son piezas "
        "alegres y sofisticadas al mismo tiempo, perfectas para sentirme segura y "
        "femenina en la playa.",
    ),
]

SITE_PHONE = "+57 301 7122411"
SITE_EMAIL = "palmacayena@gmail.com"


def apply_changes(apps, schema_editor):
    HeroSection = apps.get_model("pages", "HeroSection")
    Testimonial = apps.get_model("pages", "Testimonial")
    SiteConfig = apps.get_model("core", "SiteConfig")

    # Hero: nuevo título y subtítulo
    HeroSection.objects.all().update(title=HERO_TITLE, subtitle=HERO_SUBTITLE)

    # Reseñas: reemplazar por las nuevas
    Testimonial.objects.all().delete()
    for i, (name, text) in enumerate(TESTIMONIALS):
        Testimonial.objects.create(
            name=name, text=text, rating=5, is_active=True, order=i
        )

    # Contacto (footer): teléfono y email
    SiteConfig.objects.filter(pk=1).update(phone=SITE_PHONE, email=SITE_EMAIL)


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0001_initial"),
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(apply_changes, migrations.RunPython.noop),
    ]
