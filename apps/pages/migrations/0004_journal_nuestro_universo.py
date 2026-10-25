# -*- coding: utf-8 -*-
from django.db import migrations
from django.utils import timezone


TITLE = "Un vistazo a nuestro universo"
SLUG = "un-vistazo-a-nuestro-universo"
EXCERPT = (
    "Hemos pasado meses guardando imágenes, texturas, colores y pequeñas ideas "
    "que, sin saberlo, terminaron conectándose entre sí. Hoy compartimos una "
    "parte de ese universo."
)

# (archivo de imagen, texto alternativo)
_GALLERY = [
    ("01", "Moldes y pepas artesanales sobre el patronaje"),
    ("03", "Pepas en tono rosa, tejidas a mano"),
    ("04", "Piezas listas, empacadas una a una"),
    ("05", "Pepas clasificadas por color y cantidad"),
    ("06", "Textura de las pepas en rosa y rojo"),
    ("07", "Mood board: inspiración del Caribe"),
    ("08", "Telas y pepas sobre el tablero de inspiración"),
    ("09", "Pepas sobre el molde de la pieza"),
    ("10", "Pepas en rojo, listas para bordar"),
    ("11", "Referencias: fauna, mar y sol"),
    ("12", "Carta de colores en lino"),
]


def _build_content():
    p = []
    p.append(
        "<p>Hemos pasado meses guardando imágenes, texturas, colores y pequeñas "
        "ideas que, sin saberlo, terminaron conectándose entre sí. Hoy comparto "
        "una parte de ese universo.</p>"
    )
    p.append(
        "<p>Todo lo que estamos creando nace de un proceso artesanal, de la "
        "intención puesta en cada detalle y de la convicción de que las cosas "
        "más especiales toman tiempo.</p>"
    )
    p.append(
        '<img src="/static/images/journal/journal-02.jpg" '
        'alt="Vestido de baño en rojo con terminaciones artesanales — Palma Cayena" '
        'loading="eager" style="width:100%;border-radius:14px;margin:2.5rem 0;display:block;">'
    )
    p.append(
        '<p style="font-style:italic;color:var(--color-pink);text-align:center;'
        'margin:0 0 2rem;">El amor y el mar, hilo a hilo.</p>'
    )
    p.append(
        '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));'
        'gap:1rem;margin:2rem 0;">'
    )
    for num, alt in _GALLERY:
        p.append(
            f'<img src="/static/images/journal/journal-{num}.jpg" alt="{alt} — Palma Cayena" '
            'loading="lazy" style="width:100%;height:340px;object-fit:cover;'
            'border-radius:10px;display:block;">'
        )
    p.append("</div>")
    p.append(
        "<p>Cada pieza es un pequeño universo hecho a mano. Esto es apenas el comienzo.</p>"
    )
    return "\n".join(p)


CONTENT = _build_content()


def create_post(apps, schema_editor):
    JournalPost = apps.get_model("pages", "JournalPost")
    JournalPost.objects.update_or_create(
        slug=SLUG,
        defaults=dict(
            title=TITLE,
            excerpt=EXCERPT,
            content=CONTENT,
            author="Palma Cayena",
            is_published=True,
            published_at=timezone.now(),
        ),
    )


def remove_post(apps, schema_editor):
    JournalPost = apps.get_model("pages", "JournalPost")
    JournalPost.objects.filter(slug=SLUG).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0003_update_whatsapp_phone"),
    ]

    operations = [
        migrations.RunPython(create_post, remove_post),
    ]
