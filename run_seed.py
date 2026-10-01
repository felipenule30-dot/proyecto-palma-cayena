import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
import django; django.setup()

from apps.core.models import SiteConfig, SocialLink
from apps.shop.models import Category, Collection, Color, Size, Tag, Product, ProductVariant
from apps.pages.models import HeroSection, HomepageBlock, BenefitItem, Testimonial, FAQ, StaticPage

# Site config
c = SiteConfig.get()
c.site_name = 'Palma Cayena'
c.site_tagline = 'Nacida del Caribe. Disenada para la mujer que lleva el mar adentro.'
c.email = 'palmacayena@gmail.com'
c.phone = '+57 301 7122411'
c.city = 'Cartagena, Colombia'
c.default_meta_title = 'Palma Cayena - Vestidos de bano del Caribe Colombiano'
c.default_meta_description = 'Vestidos de bano disenados en el Caribe colombiano. Feminidad, sofisticacion y el espiritu de Cartagena.'
c.free_shipping_threshold = 250000
c.shipping_cost = 15000
c.save()
print('SiteConfig OK')

SocialLink.objects.all().delete()
SocialLink.objects.create(platform='instagram', url='https://instagram.com/palmacayena', order=1)
SocialLink.objects.create(platform='tiktok', url='https://tiktok.com/@palmacayena', order=2)
print('SocialLinks OK')

Size.objects.all().delete()
sizes = {}
for i, (n, d) in enumerate([('XS','Extra Small'),('S','Small'),('M','Medium'),('L','Large'),('XL','Extra Large')]):
    sizes[n] = Size.objects.create(name=n, description=d, order=i)
print('Sizes OK')

Color.objects.all().delete()
colors = {}
for i, (n, h) in enumerate([
    ('Arena','#E8D5B0'),('Coral','#E07060'),('Carmesi','#BC0E2C'),
    ('Orquidea','#C855B8'),('Espresso','#3A2820'),('Blanco','#F8F5F2'),
    ('Negro','#111111'),('Turquesa','#40B4C4')
]):
    colors[n] = Color.objects.create(name=n, hex_code=h, order=i)
print('Colors OK')

Tag.objects.all().delete()
t_bk = Tag.objects.create(name='Bikini', slug='bikini')
t_op = Tag.objects.create(name='Una pieza', slug='una-pieza')
t_rs = Tag.objects.create(name='Resort', slug='resort')
t_ed = Tag.objects.create(name='Editorial', slug='editorial')
print('Tags OK')

Category.objects.all().delete()
cat_bk = Category.objects.create(name='Bikinis', slug='bikinis', meta_title='Bikinis - Palma Cayena', order=1)
cat_op = Category.objects.create(name='Una pieza', slug='una-pieza', meta_title='Una pieza - Palma Cayena', order=2)
cat_cu = Category.objects.create(name='Cover ups', slug='cover-ups', meta_title='Cover ups - Palma Cayena', order=3)
print('Categories OK')

Collection.objects.all().delete()
col_v = Collection.objects.create(name='Valentina', slug='valentina', description='Inspirada en la mujer cartagenera: fuerte, sensual y libre.', is_active=True, is_featured=True, order=1)
col_c = Collection.objects.create(name='Caribe Noir', slug='caribe-noir', description='La elegancia del Caribe en su version mas oscura.', is_active=True, order=2)
print('Collections OK')

Product.objects.all().delete()
prods = [
    ('Bikini Valeria','PC-BK-001',cat_bk,col_v,'Bikini de dos piezas con escote en V.',280000,None,True,True,[t_bk,t_ed],['Carmesi','Orquidea','Arena'],['XS','S','M','L'],1),
    ('Bikini Luna','PC-BK-002',cat_bk,col_v,'Bikini triangular minimalista con cola alta.',260000,320000,True,True,[t_bk,t_rs],['Arena','Blanco','Turquesa'],['XS','S','M','L','XL'],2),
    ('Bikini Cayena','PC-BK-003',cat_bk,col_c,'Bikini bandeau con argolla central.',320000,None,True,True,[t_bk,t_ed],['Espresso','Negro','Carmesi'],['XS','S','M','L'],3),
    ('Traje Una Pieza Palma','PC-OP-001',cat_op,col_v,'Traje de bano de una pieza con espalda descubierta.',380000,450000,True,False,[t_op,t_ed],['Coral','Arena','Espresso'],['XS','S','M','L'],4),
    ('Traje Una Pieza Caribe','PC-OP-002',cat_op,col_c,'Traje entero con corte asimetrico.',420000,None,False,True,[t_op,t_rs],['Negro','Orquidea'],['S','M','L','XL'],5),
    ('Cover Up Brisa','PC-CU-001',cat_cu,col_v,'Pareo largo de gasa con estampado tropical.',180000,None,False,True,[t_rs],['Arena','Blanco','Turquesa'],['S','M','L'],6),
]

for name, sku, cat, col, desc, price, cp, feat, new, tags, colorl, sizel, order in prods:
    slug = name.lower().replace(' ', '-')
    p = Product.objects.create(
        name=name, slug=slug, sku=sku, category=cat, collection=col,
        short_description=desc, price=price, compare_price=cp,
        is_featured=feat, is_new=new, status='active', order=order
    )
    p.tags.set(tags)
    p.colors.set([colors[c] for c in colorl if c in colors])
    p.sizes.set([sizes[s] for s in sizel if s in sizes])
    for sn in sizel:
        for cn in colorl:
            if sn in sizes and cn in colors:
                ProductVariant.objects.get_or_create(
                    product=p, size=sizes[sn], color=colors[cn],
                    defaults={'stock': 10, 'is_active': True}
                )
print('Products + Variants OK')

HeroSection.objects.all().delete()
HeroSection.objects.create(
    title='For slow mornings, salty skin & golden afternoons.',
    subtitle='Crafted by Colombian hands.',
    cta_text='Explorar coleccion', cta_url='/tienda/', is_active=True, order=1
)
print('Hero OK')

HomepageBlock.objects.all().delete()
HomepageBlock.objects.create(
    block_type='storytelling',
    title='Born from the idea that clothing is not just fabric',
    subtitle='Nuestra esencia',
    body_text='Palma Cayena nacio de la idea de que un vestido de bano puede ser una obra de arte. Cada pieza esta inspirada en los colores del Caribe colombiano, la fuerza del mar y la feminidad sin limites de la mujer de hoy.',
    cta_text='Conocer nuestra historia', cta_url='/nosotras/', is_active=True, order=1
)
print('Blocks OK')

BenefitItem.objects.all().delete()
for i, (icon, title, desc) in enumerate([
    ('truck', 'Envio a todo Colombia', 'Gratis en compras mayores a $250.000 COP.'),
    ('shield', 'Pago 100% seguro', 'Procesamos tus pagos con Wompi.'),
    ('refresh', 'Cambios sin complicaciones', '30 dias para cambios y devoluciones.'),
    ('heart', 'Hecho con amor', 'Calidad artesanal desde la primera vez.'),
]):
    BenefitItem.objects.create(icon=icon, title=title, description=desc, is_active=True, order=i)
print('Benefits OK')

Testimonial.objects.all().delete()
for i, (n, l, t) in enumerate([
    ('Saso - Cata', '', 'Me encantan los enterizos: la tela es gruesa y de una horma espectacular, asi que estilizan el cuerpo y quedan tan bien que los uso tambien como body con jeans. Se sienten firmes y se ven impecables dentro y fuera del agua.'),
    ('Male', '', 'La calidad de la tela es lo que mas me conquisto. Se siente suave pero resistente, no se transparenta ni pierde la forma, y despues de varios usos sigue como nueva.'),
    ('Isa', '', 'Me enamore de lo colorido y a la vez elegante de cada diseno. Son piezas alegres y sofisticadas al mismo tiempo, perfectas para sentirme segura y femenina en la playa.'),
]):
    Testimonial.objects.create(name=n, location=l, text=t, rating=5, is_active=True, order=i)
print('Testimonials OK')

FAQ.objects.all().delete()
for i, (cat, q, a) in enumerate([
    ('shipping', 'Cuando tarda el envio?', '3 a 7 dias habiles dependiendo de tu ciudad.'),
    ('shipping', 'El envio es gratis?', 'Gratis en compras mayores a $250.000 COP.'),
    ('sizing', 'Como se cual talla elegir?', 'Mide tu busto, cintura y cadera y compara con nuestra guia de tallas.'),
    ('returns', 'Puedo cambiar mi pedido?', 'Tienes 30 dias desde la recepcion para solicitar un cambio.'),
    ('payments', 'Que metodos de pago aceptan?', 'Tarjetas, PSE, Nequi y Daviplata a traves de Wompi.'),
]):
    FAQ.objects.create(category=cat, question=q, answer=a, is_active=True, order=i)
print('FAQs OK')

StaticPage.objects.all().delete()
StaticPage.objects.create(page_type='about', title='Nuestra historia', slug='nosotras',
    subtitle='Nacida del Caribe.',
    content='<p>Palma Cayena nacio en Cartagena, donde el Caribe ensena que la belleza no necesita explicacion. Disenamos para la mujer que lleva el mar adentro.</p>',
    is_published=True)
StaticPage.objects.create(page_type='shipping', title='Envios', slug='envios',
    content='<p>Envios a todo Colombia. Gratis en compras mayores a $250.000 COP. Tiempo de entrega: 3-7 dias habiles.</p>',
    is_published=True)
StaticPage.objects.create(page_type='returns', title='Cambios y devoluciones', slug='cambios-y-devoluciones',
    content='<p>Tienes 30 dias desde la recepcion para solicitar un cambio. Escribenos a hola@palmacayena.com.</p>',
    is_published=True)
StaticPage.objects.create(page_type='terms', title='Terminos y condiciones', slug='terminos',
    content='<p>Al realizar una compra aceptas nuestros terminos y condiciones.</p>',
    is_published=True)
StaticPage.objects.create(page_type='privacy', title='Politica de privacidad', slug='privacidad',
    content='<p>No vendemos ni compartimos tus datos con terceros.</p>',
    is_published=True)
print('Pages OK')

print('\nSeed data completado exitosamente!')
print('Ahora corre: python manage.py createsuperuser')
print('Y luego: python manage.py runserver')
