from django.db import models
from django.utils.text import slugify


class StaticPage(models.Model):
    PAGE_CHOICES = [
        ('about', 'Nosotras'),
        ('shipping', 'Envíos'),
        ('returns', 'Cambios y devoluciones'),
        ('terms', 'Términos y condiciones'),
        ('privacy', 'Política de privacidad'),
        ('contact', 'Contacto'),
        ('custom', 'Personalizada'),
    ]
    page_type = models.CharField('Tipo', max_length=20, choices=PAGE_CHOICES, default='custom')
    title = models.CharField('Título', max_length=200)
    slug = models.SlugField('Slug', unique=True, blank=True)
    content = models.TextField('Contenido HTML')
    subtitle = models.CharField('Subtítulo', max_length=300, blank=True)
    hero_image = models.ImageField('Imagen hero', upload_to='pages/', blank=True, null=True)
    hero_image_alt = models.CharField('Alt imagen hero', max_length=200, blank=True)
    meta_title = models.CharField('Meta title', max_length=160, blank=True)
    meta_description = models.TextField('Meta description', max_length=320, blank=True)
    is_published = models.BooleanField('Publicada', default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Página'
        verbose_name_plural = 'Páginas'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        type_url_map = {
            'about': 'pages:about',
            'shipping': 'pages:shipping',
            'returns': 'pages:returns',
            'terms': 'pages:terms',
            'privacy': 'pages:privacy',
            'contact': 'pages:contact',
        }
        if self.page_type in type_url_map:
            return reverse(type_url_map[self.page_type])
        return reverse('pages:static_page', kwargs={'slug': self.slug})


class HeroSection(models.Model):
    title = models.CharField('Título', max_length=200)
    subtitle = models.CharField('Subtítulo', max_length=300, blank=True)
    cta_text = models.CharField('Texto del botón', max_length=80, default='Explorar colección')
    cta_url = models.CharField('URL del botón', max_length=200, default='/tienda/')
    image = models.ImageField('Imagen de fondo', upload_to='hero/', blank=True, null=True)
    image_alt = models.CharField('Alt imagen', max_length=200, blank=True)
    video_url = models.URLField('URL de video (mp4)', blank=True)
    text_color = models.CharField('Color del texto', max_length=7, default='#FFFFFF')
    overlay_opacity = models.DecimalField('Opacidad del overlay', max_digits=3, decimal_places=2,
                                           default=0.30)
    is_active = models.BooleanField('Activo', default=True)
    order = models.PositiveSmallIntegerField('Orden', default=0)

    class Meta:
        verbose_name = 'Hero section'
        verbose_name_plural = 'Hero sections'
        ordering = ['order']

    def __str__(self):
        return self.title


class HomepageBlock(models.Model):
    BLOCK_TYPE_CHOICES = [
        ('storytelling', 'Storytelling de marca'),
        ('benefits', 'Bloque de beneficios'),
        ('editorial', 'Editorial / Lookbook'),
        ('instagram', 'Bloque Instagram'),
        ('quote', 'Cita / Frase'),
        ('banner', 'Banner promocional'),
        ('custom', 'Bloque personalizado'),
    ]
    block_type = models.CharField('Tipo', max_length=30, choices=BLOCK_TYPE_CHOICES)
    title = models.CharField('Título', max_length=200, blank=True)
    subtitle = models.CharField('Subtítulo', max_length=400, blank=True)
    body_text = models.TextField('Texto principal', blank=True)
    cta_text = models.CharField('Texto CTA', max_length=80, blank=True)
    cta_url = models.CharField('URL CTA', max_length=200, blank=True)
    image = models.ImageField('Imagen', upload_to='homepage/', blank=True, null=True)
    image_secondary = models.ImageField('Imagen secundaria', upload_to='homepage/', blank=True, null=True)
    image_alt = models.CharField('Alt imagen', max_length=200, blank=True)
    bg_color = models.CharField('Color de fondo', max_length=7, blank=True, default='')
    is_active = models.BooleanField('Activo', default=True)
    order = models.PositiveSmallIntegerField('Orden', default=0)

    class Meta:
        verbose_name = 'Bloque homepage'
        verbose_name_plural = 'Bloques homepage'
        ordering = ['order']

    def __str__(self):
        return f'{self.get_block_type_display()} — {self.title or "(sin título)"}'


class BenefitItem(models.Model):
    ICON_CHOICES = [
        ('truck', 'Envío'),
        ('shield', 'Pago seguro'),
        ('refresh', 'Devoluciones'),
        ('heart', 'Calidad'),
        ('star', 'Exclusividad'),
        ('leaf', 'Sostenibilidad'),
    ]
    icon = models.CharField('Ícono', max_length=20, choices=ICON_CHOICES, default='star')
    title = models.CharField('Título', max_length=100)
    description = models.CharField('Descripción', max_length=200)
    is_active = models.BooleanField('Activo', default=True)
    order = models.PositiveSmallIntegerField('Orden', default=0)

    class Meta:
        verbose_name = 'Beneficio'
        verbose_name_plural = 'Beneficios'
        ordering = ['order']

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    name = models.CharField('Nombre', max_length=100)
    location = models.CharField('Ciudad', max_length=100, blank=True)
    text = models.TextField('Testimonio')
    rating = models.PositiveSmallIntegerField('Rating', default=5, choices=[(i, i) for i in range(1, 6)])
    photo = models.ImageField('Foto', upload_to='testimonials/', blank=True, null=True)
    is_active = models.BooleanField('Activo', default=True)
    order = models.PositiveSmallIntegerField('Orden', default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Testimonio'
        verbose_name_plural = 'Testimonios'
        ordering = ['order', '-created_at']

    def __str__(self):
        return f'{self.name} — {self.rating}★'


class FAQ(models.Model):
    CATEGORY_CHOICES = [
        ('shipping', 'Envíos'),
        ('returns', 'Cambios y devoluciones'),
        ('sizing', 'Tallas'),
        ('payments', 'Pagos'),
        ('products', 'Productos'),
        ('general', 'General'),
    ]
    category = models.CharField('Categoría', max_length=20, choices=CATEGORY_CHOICES, default='general')
    question = models.CharField('Pregunta', max_length=300)
    answer = models.TextField('Respuesta')
    is_active = models.BooleanField('Activa', default=True)
    order = models.PositiveSmallIntegerField('Orden', default=0)

    class Meta:
        verbose_name = 'Pregunta frecuente'
        verbose_name_plural = 'Preguntas frecuentes'
        ordering = ['category', 'order']

    def __str__(self):
        return self.question


class NewsletterSubscriber(models.Model):
    email = models.EmailField('Email', unique=True)
    name = models.CharField('Nombre', max_length=100, blank=True)
    is_active = models.BooleanField('Activo', default=True)
    source = models.CharField('Fuente', max_length=50, blank=True, default='homepage')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Suscriptor newsletter'
        verbose_name_plural = 'Suscriptores newsletter'
        ordering = ['-created_at']

    def __str__(self):
        return self.email


class ContactMessage(models.Model):
    name = models.CharField('Nombre', max_length=150)
    email = models.EmailField('Email')
    phone = models.CharField('Teléfono', max_length=20, blank=True)
    subject = models.CharField('Asunto', max_length=200)
    message = models.TextField('Mensaje')
    is_read = models.BooleanField('Leído', default=False)
    replied_at = models.DateTimeField('Respondido en', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Mensaje de contacto'
        verbose_name_plural = 'Mensajes de contacto'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.subject}'


class JournalPost(models.Model):
    title = models.CharField('Título', max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    excerpt = models.TextField('Extracto', blank=True)
    content = models.TextField('Contenido')
    cover_image = models.ImageField('Imagen portada', upload_to='journal/', blank=True, null=True)
    cover_image_alt = models.CharField('Alt imagen', max_length=200, blank=True)
    author = models.CharField('Autora', max_length=100, default='Palma Cayena')
    is_published = models.BooleanField('Publicado', default=False)
    meta_title = models.CharField('Meta title', max_length=160, blank=True)
    meta_description = models.TextField('Meta description', max_length=320, blank=True)
    published_at = models.DateTimeField('Fecha de publicación', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Post del journal'
        verbose_name_plural = 'Journal'
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('pages:journal_post', kwargs={'slug': self.slug})
