"""
Palma Cayena — Seed Data
Ejecutar con: python manage.py shell < seed_data.py
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.core.models import SiteConfig, SocialLink
from apps.shop.models import Category, Collection, Color, Size, Tag, Product, ProductVariant
from apps.pages.models import (HeroSection, HomepageBlock, BenefitItem,
                                Testimonial, FAQ, StaticPage)

print("🌴 Iniciando seed data de Palma Cayena...")

# ── SITE CONFIG ──────────────────────────────────────────────
config = SiteConfig.get()
config.site_name = "Palma Cayena"
config.site_tagline = "Nacida del Caribe. Diseñada para la mujer que lleva el mar adentro."
config.email = "hola@palmacayena.com"
config.phone = "+57 310 000 0000"
config.city = "Cartagena, Colombia"
config.default_meta_title = "Palma Cayena — Vestidos de baño del Caribe Colombiano"
config.default_meta_description = (
    "Vestidos de baño diseñados en el Caribe colombiano. "
    "Feminidad, sofisticación y el espíritu de Cartagena en cada pieza."
)
config.free_shipping_threshold = 250000
config.shipping_cost = 15000
config.save()
print("✓ SiteConfig guardado")

# ── SOCIAL LINKS ─────────────────────────────────────────────
SocialLink.objects.all().delete()
SocialLink.objects.create(platform='instagram', url='https://instagram.com/palmacayena', order=1)
SocialLink.objects.create(platform='tiktok',    url='https://tiktok.com/@palmacayena',  order=2)
print("✓ Redes sociales creadas")

# ── TALLAS ───────────────────────────────────────────────────
Size.objects.all().delete()
sizes = {}
for i, (name, desc) in enumerate([
    ('XS', 'Extra Small'),
    ('S',  'Small'),
    ('M',  'Medium'),
    ('L',  'Large'),
    ('XL', 'Extra Large'),
]):
    sizes[name] = Size.objects.create(name=name, description=desc, order=i)
print("✓ Tallas creadas")

# ── COLORES ──────────────────────────────────────────────────
Color.objects.all().delete()
colors = {}
for i, (name, hex_code) in enumerate([
    ('Arena',    '#E8D5B0'),
    ('Coral',    '#E07060'),
    ('Carmesí',  '#BC0E2C'),
    ('Orquídea', '#C855B8'),
    ('Espresso', '#3A2820'),
    ('Blanco',   '#F8F5F2'),
    ('Negro',    '#111111'),
    ('Turquesa', '#40B4C4'),
]):
    colors[name] = Color.objects.create(name=name, hex_code=hex_code, order=i)
print("✓ Colores creados")

# ── TAGS ─────────────────────────────────────────────────────
Tag.objects.all().delete()
tag_bikini     = Tag.objects.create(name='Bikini',      slug='bikini')
tag_onepiece   = Tag.objects.create(name='Una pieza',   slug='una-pieza')
tag_resort     = Tag.objects.create(name='Resort',      slug='resort')
tag_editorial  = Tag.objects.create(name='Editorial',   slug='editorial')
tag_bestseller = Tag.objects.create(name='Más vendido', slug='mas-vendido')
print("✓ Tags creados")

# ── CATEGORÍAS ───────────────────────────────────────────────
Category.objects.all().delete()
cat_bikinis   = Category.objects.create(
    name='Bikinis', slug='bikinis',
    description='Dos piezas diseñadas para la mujer que no pasa desapercibida.',
    meta_title='Bikinis — Palma Cayena',
    meta_description='Bikinis de diseño para la mujer del Caribe colombiano.',
    order=1
)
cat_onepiece  = Category.objects.create(
    name='Una pieza', slug='una-pieza',
    description='Trajes de baño enteros con la elegancia de una sola pieza.',
    meta_title='Trajes de baño una pieza — Palma Cayena',
    meta_description='Trajes de baño de una pieza elegantes y sofisticados.',
    order=2
)
cat_coverups  = Category.objects.create(
    name='Cover ups', slug='cover-ups',
    description='Para ir de la playa al restaurant sin perder el estilo.',
    meta_title='Cover ups — Palma Cayena',
    meta_description='Cover ups y salidas de baño de Palma Cayena.',
    order=3
)
print("✓ Categorías creadas")

# ── COLECCIONES ──────────────────────────────────────────────
Collection.objects.all().delete()
col_valentina = Collection.objects.create(
    name='Valentina',
    slug='valentina',
    description='Inspirada en la mujer cartagenera: fuerte, sensual y libre.',
    story=(
        'La colección Valentina nace del ritmo del mar Caribe al amanecer. '
        'Cada pieza es un poema visual que celebra la feminidad sin límites. '
        'Telas que abrazan el cuerpo como el agua, colores que recuerdan '
        'los atardeceres de Cartagena.'
    ),
    is_active=True,
    is_featured=True,
    order=1
)
col_caribe = Collection.objects.create(
    name='Caribe Noir',
    slug='caribe-noir',
    description='La elegancia del Caribe en su versión más oscura y misteriosa.',
    story=(
        'Caribe Noir es el lado nocturno del paraíso. Colores profundos, '
        'siluetas atrevidas y una actitud que dice: el lujo no necesita '
        'ser ruidoso.'
    ),
    is_active=True,
    is_featured=False,
    order=2
)
print("✓ Colecciones creadas")

# ── PRODUCTOS ────────────────────────────────────────────────
Product.objects.all().delete()

products_data = [
    {
        'name': 'Bikini Valeria',
        'sku': 'PC-BK-001',
        'category': cat_bikinis,
        'collection': col_valentina,
        'short_description': 'Bikini de dos piezas con escote en V y tiras ajustables. El favorito de la temporada.',
        'description': 'El Bikini Valeria es la pieza estrella de la colección Valentina. Su corte en V realza el escote mientras las tiras doradas ajustables le dan un toque editorial. Confeccionado en tejido de lycra de alta resistencia al cloro y al sol.',
        'composition': '82% Poliamida, 18% Elastano',
        'care_instructions': 'Lavar a mano con agua fría. No usar secadora. Enjuagar inmediatamente después del uso en mar o piscina.',
        'price': 280000,
        'compare_price': None,
        'is_featured': True,
        'is_new': True,
        'is_bestseller': True,
        'tags': [tag_bikini, tag_editorial, tag_bestseller],
        'colors_list': ['Carmesí', 'Orquídea', 'Arena'],
        'sizes_list': ['XS', 'S', 'M', 'L'],
        'meta_title': 'Bikini Valeria — Palma Cayena',
        'meta_description': 'Bikini de dos piezas con escote en V. Diseño editorial del Caribe colombiano.',
        'order': 1,
    },
    {
        'name': 'Bikini Luna',
        'sku': 'PC-BK-002',
        'category': cat_bikinis,
        'collection': col_valentina,
        'short_description': 'Bikini triangular minimalista con cola alta. Elegancia natural.',
        'description': 'El Bikini Luna es para la mujer que prefiere la belleza en su forma más pura. Triángulo minimalista arriba, cola alta abajo. Una combinación que estiliza y libera al mismo tiempo.',
        'composition': '80% Poliamida, 20% Elastano',
        'care_instructions': 'Lavar a mano con agua fría. No usar secadora.',
        'price': 260000,
        'compare_price': 320000,
        'is_featured': True,
        'is_new': True,
        'is_bestseller': False,
        'tags': [tag_bikini, tag_resort],
        'colors_list': ['Arena', 'Blanco', 'Turquesa'],
        'sizes_list': ['XS', 'S', 'M', 'L', 'XL'],
        'meta_title': 'Bikini Luna — Palma Cayena',
        'meta_description': 'Bikini triangular minimalista con cola alta de Palma Cayena.',
        'order': 2,
    },
    {
        'name': 'Bikini Cayena',
        'sku': 'PC-BK-003',
        'category': cat_bikinis,
        'collection': col_caribe,
        'short_description': 'Bikini bandeau con detalle de argolla central. Dramático y sofisticado.',
        'description': 'El Bikini Cayena lleva el nombre de la marca por una razón: es la pieza más icónica de la colección Caribe Noir. Bandeau estructurado con argolla dorada central y bottom de corte brasilero.',
        'composition': '85% Poliamida, 15% Elastano',
        'care_instructions': 'Lavar a mano con agua fría.',
        'price': 320000,
        'compare_price': None,
        'is_featured': True,
        'is_new': True,
        'is_bestseller': True,
        'tags': [tag_bikini, tag_editorial],
        'colors_list': ['Espresso', 'Negro', 'Carmesí'],
        'sizes_list': ['XS', 'S', 'M', 'L'],
        'meta_title': 'Bikini Cayena — Palma Cayena',
        'meta_description': 'Bikini bandeau con argolla dorada. La pieza icónica de Palma Cayena.',
        'order': 3,
    },
    {
        'name': 'Traje Una Pieza Palma',
        'sku': 'PC-OP-001',
        'category': cat_onepiece,
        'collection': col_valentina,
        'short_description': 'Traje de baño de una pieza con escote profundo en la espalda. Elegancia total.',
        'description': 'El Traje Palma redefine lo que significa elegancia en la playa. Su espalda completamente abierta lo convierte en una pieza editorial mientras la parte delantera ofrece el soporte perfecto.',
        'composition': '82% Poliamida, 18% Elastano',
        'care_instructions': 'Lavar a mano con agua fría. No usar secadora.',
        'price': 380000,
        'compare_price': 450000,
        'is_featured': True,
        'is_new': False,
        'is_bestseller': True,
        'tags': [tag_onepiece, tag_editorial, tag_bestseller],
        'colors_list': ['Coral', 'Arena', 'Espresso'],
        'sizes_list': ['XS', 'S', 'M', 'L'],
        'meta_title': 'Traje Una Pieza Palma — Palma Cayena',
        'meta_description': 'Traje de baño de una pieza con espalda descubierta. Palma Cayena.',
        'order': 4,
    },
    {
        'name': 'Traje Una Pieza Caribe',
        'sku': 'PC-OP-002',
        'category': cat_onepiece,
        'collection': col_caribe,
        'short_description': 'Traje entero con corte asimétrico y hombro único. Pura actitud.',
        'description': 'El Traje Caribe es para la mujer que no pasa desapercibida. Corte asimétrico, un solo hombro y líneas que abrazan la figura de manera espectacular. De la piscina al cóctel sin parar.',
        'composition': '80% Poliamida, 20% Elastano',
        'care_instructions': 'Lavar a mano con agua fría.',
        'price': 420000,
        'compare_price': None,
        'is_featured': False,
        'is_new': True,
        'is_bestseller': False,
        'tags': [tag_onepiece, tag_resort],
        'colors_list': ['Negro', 'Orquídea'],
        'sizes_list': ['S', 'M', 'L', 'XL'],
        'meta_title': 'Traje Una Pieza Caribe — Palma Cayena',
        'meta_description': 'Traje de baño asimétrico de un hombro. Palma Cayena Caribe Noir.',
        'order': 5,
    },
    {
        'name': 'Cover Up Brisa',
        'sku': 'PC-CU-001',
        'category': cat_coverups,
        'collection': col_valentina,
        'short_description': 'Pareo largo de gasa con estampado tropical. De la playa al restaurante.',
        'description': 'La Cover Up Brisa es la compañera perfecta para cualquier pieza de la colección. Gasa de alta calidad con caída fluida, estampado tropical exclusivo y amarre versátil.',
        'composition': '100% Viscosa',
        'care_instructions': 'Lavar a mano o en máquina en ciclo delicado.',
        'price': 180000,
        'compare_price': None,
        'is_featured': False,
        'is_new': True,
        'is_bestseller': False,
        'tags': [tag_resort],
        'colors_list': ['Arena', 'Blanco', 'Turquesa'],
        'sizes_list': ['S', 'M', 'L'],
        'meta_title': 'Cover Up Brisa — Palma Cayena',
        'meta_description': 'Pareo de gasa con estampado tropical. Cover up de Palma Cayena.',
        'order': 6,
    },
]

for data in products_data:
    colors_list = data.pop('colors_list')
    sizes_list  = data.pop('sizes_list')
    tags_list   = data.pop('tags')

    product = Product.objects.create(
        name=data['name'],
        slug=data['name'].lower().replace(' ', '-'),
        sku=data['sku'],
        category=data['category'],
        collection=data['collection'],
        short_description=data['short_description'],
        description=data['description'],
        composition=data['composition'],
        care_instructions=data['care_instructions'],
        price=data['price'],
        compare_price=data.get('compare_price'),
        is_featured=data['is_featured'],
        is_new=data['is_new'],
        is_bestseller=data['is_bestseller'],
        status='active',
        meta_title=data['meta_title'],
        meta_description=data['meta_description'],
        order=data['order'],
    )
    product.tags.set(tags_list)
    product.colors.set([colors[c] for c in colors_list if c in colors])
    product.sizes.set([sizes[s] for s in sizes_list if s in sizes])

    # Crear variantes
    for size_name in sizes_list:
        for color_name in colors_list:
            if size_name in sizes and color_name in colors:
                ProductVariant.objects.create(
                    product=product,
                    size=sizes[size_name],
                    color=colors[color_name],
                    stock=10,
                    is_active=True,
                )

print(f"✓ {len(products_data)} productos creados con variantes")

# ── HERO SECTION ─────────────────────────────────────────────
HeroSection.objects.all().delete()
HeroSection.objects.create(
    title="Naces del mar,\nvives en él.",
    subtitle="Vestidos de baño para la mujer que lleva el Caribe en la piel. Diseño editorial, artesanía colombiana.",
    cta_text="Explorar colección",
    cta_url="/tienda/",
    is_active=True,
    order=1,
)
print("✓ Hero section creado")

# ── HOMEPAGE BLOCKS ──────────────────────────────────────────
HomepageBlock.objects.all().delete()
HomepageBlock.objects.create(
    block_type='storytelling',
    title="Born from the idea that clothing is not just fabric",
    subtitle="Nuestra esencia",
    body_text=(
        "Palma Cayena nació de la idea de que un vestido de baño puede ser una obra de arte. "
        "Cada pieza está inspirada en los colores del Caribe colombiano, la fuerza del mar "
        "y la feminidad sin límites de la mujer de hoy. Diseñamos para la mujer que camina "
        "descalza sobre la arena con la misma seguridad con la que conquista el mundo."
    ),
    cta_text="Conocer nuestra historia",
    cta_url="/nosotras/",
    is_active=True,
    order=1,
)
print("✓ Homepage blocks creados")

# ── BENEFITS ─────────────────────────────────────────────────
BenefitItem.objects.all().delete()
benefits = [
    ('truck',   'Envío a todo Colombia',        'Gratis en compras mayores a $250.000 COP.'),
    ('shield',  'Pago 100% seguro',              'Procesamos tus pagos con Wompi, la plataforma más confiable de Colombia.'),
    ('refresh', 'Cambios sin complicaciones',    'Tienes 30 días para hacer un cambio o devolución.'),
    ('heart',   'Hecho con amor',                'Calidad artesanal que se siente desde la primera vez que lo usas.'),
]
for i, (icon, title, desc) in enumerate(benefits):
    BenefitItem.objects.create(icon=icon, title=title, description=desc, is_active=True, order=i)
print("✓ Benefits creados")

# ── TESTIMONIOS ──────────────────────────────────────────────
Testimonial.objects.all().delete()
testimonios = [
    ("Valeria M.",    "Cartagena",   "Llevo el Bikini Valeria a todas mis vacaciones. Es literalmente perfecto.", 5),
    ("Isabela R.",    "Bogotá",      "La calidad es increíble. Se nota que cada pieza está hecha con amor y detalle.", 5),
    ("Camila P.",     "Medellín",    "Finalmente una marca colombiana que se siente de lujo real. Palma Cayena es todo.", 5),
    ("Sofía G.",      "Barranquilla","El envío fue rapidísimo y el empaque demasiado lindo. Ya quiero comprar otro.", 5),
]
for i, (name, loc, text, rating) in enumerate(testimonios):
    Testimonial.objects.create(name=name, location=loc, text=text, rating=rating, is_active=True, order=i)
print("✓ Testimonios creados")

# ── FAQs ─────────────────────────────────────────────────────
FAQ.objects.all().delete()
faqs = [
    ('shipping', '¿Cuánto tarda el envío?',
     'Los pedidos se procesan en 1-2 días hábiles. El envío nacional tarda entre 3 y 7 días hábiles dependiendo de tu ciudad.'),
    ('shipping', '¿El envío es gratis?',
     'Sí, los envíos son gratis en compras mayores a $250.000 COP. Para pedidos menores, el costo de envío es de $15.000 COP.'),
    ('sizing', '¿Cómo sé qué talla elegir?',
     'Te recomendamos medir tu busto, cintura y cadera y comparar con nuestra guía de tallas. Si estás entre dos tallas, elige la mayor.'),
    ('sizing', '¿Las tallas son colombianas o internacionales?',
     'Usamos tallas internacionales: XS, S, M, L, XL. Cada producto tiene una guía de medidas específica.'),
    ('returns', '¿Puedo cambiar mi pedido?',
     'Tienes 30 días desde la fecha de recepción para solicitar un cambio, siempre que el producto esté en perfectas condiciones con su etiqueta original.'),
    ('returns', '¿Cómo inicio una devolución?',
     'Escríbenos a hola@palmacayena.com con tu número de pedido y el motivo del cambio. Te guiamos en el proceso.'),
    ('payments', '¿Qué métodos de pago aceptan?',
     'Aceptamos tarjetas de crédito y débito, PSE, Nequi y Daviplata a través de Wompi.'),
    ('payments', '¿Es seguro pagar en su web?',
     'Totalmente. Todos los pagos son procesados por Wompi con encriptación SSL. Nunca almacenamos datos de tus tarjetas.'),
    ('products', '¿Los colores son exactos a las fotos?',
     'Hacemos todo lo posible para que las fotos reflejen los colores reales, pero pueden variar ligeramente según la pantalla.'),
]
for i, (cat, q, a) in enumerate(faqs):
    FAQ.objects.create(category=cat, question=q, answer=a, is_active=True, order=i)
print("✓ FAQs creadas")

# ── PÁGINAS ESTÁTICAS ─────────────────────────────────────────
StaticPage.objects.all().delete()

StaticPage.objects.create(
    page_type='about',
    title='Nuestra historia',
    slug='nosotras',
    subtitle='Nacida del Caribe. Diseñada para la mujer que lleva el mar adentro.',
    content="""
<p>Palma Cayena nació en Cartagena, donde el Caribe enseña que la belleza no necesita explicación.
Somos una marca de vestidos de baño que cree en el diseño con propósito, en la artesanía colombiana
y en la mujer que sabe exactamente quién es.</p>

<p>Cada pieza de Palma Cayena es una conversación entre el mar, el sol y la feminidad contemporánea.
Diseñamos para la mujer que camina descalza sobre la arena con la misma seguridad con la que
conquista el mundo.</p>

<h3>Nuestra filosofía</h3>
<p>Clothing is not just fabric. Creemos que lo que vistes es una extensión de quién eres.
Por eso cada vestido de baño está pensado como una pieza editorial: con historia, con alma,
con identidad propia.</p>

<h3>Hecho en Colombia</h3>
<p>Orgullosamente colombianas. Desde el diseño hasta la confección, todo nace aquí.
Trabajamos con artesanos locales y materiales de alta calidad para garantizar que cada
pieza sea perfecta.</p>
""",
    is_published=True,
    meta_title='Nuestra historia — Palma Cayena',
    meta_description='Conoce la historia de Palma Cayena, marca de vestidos de baño del Caribe colombiano.',
)

StaticPage.objects.create(
    page_type='shipping',
    title='Envíos',
    slug='envios',
    content="""
<h3>Tiempos de envío</h3>
<p>Los pedidos se procesan en <strong>1 a 2 días hábiles</strong>. Una vez despachado, el tiempo
de entrega depende de tu ciudad:</p>
<ul style="padding-left:1.5rem;margin:1rem 0;">
  <li style="margin-bottom:.5rem;"><strong>Ciudades principales</strong> (Bogotá, Medellín, Cali, Barranquilla, Cartagena): 2 a 4 días hábiles</li>
  <li style="margin-bottom:.5rem;"><strong>Otras ciudades:</strong> 4 a 7 días hábiles</li>
</ul>

<h3>Costos de envío</h3>
<p>El envío es <strong>gratis</strong> en compras mayores a <strong>$250.000 COP</strong>.
Para pedidos menores, el costo de envío estándar es de <strong>$15.000 COP</strong>.</p>

<h3>Seguimiento de pedido</h3>
<p>Una vez despachado tu pedido, te enviaremos un email con el número de guía para que
puedas rastrear tu envío en tiempo real.</p>
""",
    is_published=True,
    meta_title='Envíos — Palma Cayena',
    meta_description='Información sobre envíos, tiempos de entrega y costos de Palma Cayena.',
)

StaticPage.objects.create(
    page_type='returns',
    title='Cambios y devoluciones',
    slug='cambios-y-devoluciones',
    content="""
<h3>Política de cambios</h3>
<p>En Palma Cayena queremos que estés 100% satisfecha con tu compra. Por eso tienes
<strong>30 días</strong> desde la fecha de recepción para solicitar un cambio o devolución.</p>

<h3>Condiciones</h3>
<ul style="padding-left:1.5rem;margin:1rem 0;">
  <li style="margin-bottom:.5rem;">El producto debe estar en perfectas condiciones, sin uso.</li>
  <li style="margin-bottom:.5rem;">Debe conservar su etiqueta original.</li>
  <li style="margin-bottom:.5rem;">Debe estar en su empaque original.</li>
</ul>

<h3>¿Cómo solicitar un cambio?</h3>
<p>Escríbenos a <a href="mailto:hola@palmacayena.com" style="color:var(--color-pink);">hola@palmacayena.com</a>
con tu número de pedido y el motivo del cambio. Te responderemos en máximo 24 horas hábiles.</p>
""",
    is_published=True,
    meta_title='Cambios y devoluciones — Palma Cayena',
    meta_description='Política de cambios y devoluciones de Palma Cayena.',
)

StaticPage.objects.create(
    page_type='terms',
    title='Términos y condiciones',
    slug='terminos',
    content="<p>Al realizar una compra en palmacayena.com aceptas nuestros términos y condiciones. Palma Cayena se reserva el derecho de modificar precios, productos y políticas sin previo aviso. Toda la información personal es tratada conforme a nuestra política de privacidad.</p>",
    is_published=True,
    meta_title='Términos y condiciones — Palma Cayena',
    meta_description='Términos y condiciones de uso de Palma Cayena.',
)

StaticPage.objects.create(
    page_type='privacy',
    title='Política de privacidad',
    slug='privacidad',
    content="<p>Palma Cayena recopila únicamente la información necesaria para procesar tus pedidos y mejorar tu experiencia de compra. No vendemos ni compartimos tus datos con terceros. Puedes solicitar la eliminación de tus datos en cualquier momento escribiéndonos a hola@palmacayena.com.</p>",
    is_published=True,
    meta_title='Política de privacidad — Palma Cayena',
    meta_description='Política de privacidad y tratamiento de datos de Palma Cayena.',
)

print("✓ Páginas estáticas creadas")
print("\n🌴 ¡Seed data completado! El proyecto está listo.")
print("   Corre: python manage.py runserver")
