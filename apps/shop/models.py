from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class Category(models.Model):
    name = models.CharField('Nombre', max_length=100)
    slug = models.SlugField('Slug', unique=True, blank=True)
    description = models.TextField('Descripción', blank=True)
    image = models.ImageField('Imagen', upload_to='categories/', blank=True, null=True)
    image_alt = models.CharField('Alt imagen', max_length=200, blank=True)
    meta_title = models.CharField('Meta title', max_length=160, blank=True)
    meta_description = models.TextField('Meta description', max_length=320, blank=True)
    is_active = models.BooleanField('Activa', default=True)
    order = models.PositiveSmallIntegerField('Orden', default=0)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:category', kwargs={'slug': self.slug})


class Collection(models.Model):
    name = models.CharField('Nombre', max_length=100)
    slug = models.SlugField('Slug', unique=True, blank=True)
    description = models.TextField('Descripción', blank=True)
    story = models.TextField('Historia de la colección', blank=True)
    image = models.ImageField('Imagen principal', upload_to='collections/', blank=True, null=True)
    image_alt = models.CharField('Alt imagen', max_length=200, blank=True)
    banner_image = models.ImageField('Banner', upload_to='collections/banners/', blank=True, null=True)
    is_active = models.BooleanField('Activa', default=True)
    is_featured = models.BooleanField('Destacada', default=False)
    launch_date = models.DateField('Fecha de lanzamiento', blank=True, null=True)
    meta_title = models.CharField('Meta title', max_length=160, blank=True)
    meta_description = models.TextField('Meta description', max_length=320, blank=True)
    order = models.PositiveSmallIntegerField('Orden', default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Colección'
        verbose_name_plural = 'Colecciones'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:collection', kwargs={'slug': self.slug})


class Color(models.Model):
    name = models.CharField('Nombre', max_length=50)
    hex_code = models.CharField('Código HEX', max_length=7, blank=True, help_text='Ej: #FF5733')
    order = models.PositiveSmallIntegerField('Orden', default=0)

    class Meta:
        verbose_name = 'Color'
        verbose_name_plural = 'Colores'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField('Talla', max_length=20)
    description = models.CharField('Descripción', max_length=100, blank=True)
    order = models.PositiveSmallIntegerField('Orden', default=0)

    class Meta:
        verbose_name = 'Talla'
        verbose_name_plural = 'Tallas'
        ordering = ['order']

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField('Etiqueta', max_length=50)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name = 'Etiqueta'
        verbose_name_plural = 'Etiquetas'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    STATUS_ACTIVE = 'active'
    STATUS_DRAFT = 'draft'
    STATUS_ARCHIVED = 'archived'
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Activo'),
        (STATUS_DRAFT, 'Borrador'),
        (STATUS_ARCHIVED, 'Archivado'),
    ]

    name = models.CharField('Nombre', max_length=200)
    slug = models.SlugField('Slug', unique=True, blank=True, max_length=250)
    sku = models.CharField('SKU base', max_length=50, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True,
                                  verbose_name='Categoría', related_name='products')
    collection = models.ForeignKey(Collection, on_delete=models.SET_NULL, null=True, blank=True,
                                    verbose_name='Colección', related_name='products')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='Etiquetas')
    colors = models.ManyToManyField(Color, blank=True, verbose_name='Colores disponibles')
    sizes = models.ManyToManyField(Size, blank=True, verbose_name='Tallas disponibles')

    short_description = models.TextField('Descripción corta', blank=True,
                                          help_text='Aparece en el listado y encabezado del producto')
    description = models.TextField('Descripción completa', blank=True)
    care_instructions = models.TextField('Instrucciones de cuidado', blank=True)
    composition = models.CharField('Composición / Materiales', max_length=300, blank=True)

    price = models.DecimalField('Precio (COP)', max_digits=12, decimal_places=2)
    compare_price = models.DecimalField('Precio comparado (COP)', max_digits=12, decimal_places=2,
                                         blank=True, null=True, help_text='Precio antes del descuento')

    status = models.CharField('Estado', max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    is_featured = models.BooleanField('Destacado', default=False)
    is_new = models.BooleanField('Nuevo', default=True)
    is_bestseller = models.BooleanField('Más vendido', default=False)

    meta_title = models.CharField('Meta title', max_length=160, blank=True)
    meta_description = models.TextField('Meta description', max_length=320, blank=True)
    og_image = models.ImageField('OG Image (redes sociales)', upload_to='products/og/', blank=True, null=True)

    weight = models.DecimalField('Peso (kg)', max_digits=6, decimal_places=3, blank=True, null=True)
    order = models.PositiveSmallIntegerField('Orden manual', default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.sku:
            import uuid
            self.sku = f'PC-{str(uuid.uuid4())[:8].upper()}'
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'slug': self.slug})

    @property
    def main_image(self):
        img = self.images.filter(is_main=True).first()
        if not img:
            img = self.images.first()
        return img

    @property
    def discount_percentage(self):
        if self.compare_price and self.compare_price > self.price:
            return int((1 - self.price / self.compare_price) * 100)
        return None

    @property
    def is_on_sale(self):
        return bool(self.compare_price and self.compare_price > self.price)

    @property
    def is_available(self):
        return self.status == self.STATUS_ACTIVE and self.variants.filter(stock__gt=0).exists()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images',
                                 verbose_name='Producto')
    image = models.ImageField('Imagen', upload_to='products/')
    alt_text = models.CharField('Texto alternativo', max_length=200, blank=True)
    is_main = models.BooleanField('Imagen principal', default=False)
    order = models.PositiveSmallIntegerField('Orden', default=0)

    class Meta:
        verbose_name = 'Imagen de producto'
        verbose_name_plural = 'Imágenes de producto'
        ordering = ['order']

    def __str__(self):
        return f'{self.product.name} — imagen {self.order}'

    def save(self, *args, **kwargs):
        if self.is_main:
            # Solo una imagen principal por producto
            ProductImage.objects.filter(product=self.product, is_main=True).update(is_main=False)
        super().save(*args, **kwargs)


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants',
                                 verbose_name='Producto')
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Talla')
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Color')
    sku = models.CharField('SKU variante', max_length=80, unique=True, blank=True)
    stock = models.PositiveIntegerField('Stock', default=0)
    price_override = models.DecimalField('Precio especial', max_digits=12, decimal_places=2,
                                          blank=True, null=True,
                                          help_text='Si se completa, reemplaza el precio del producto')
    is_active = models.BooleanField('Activa', default=True)

    class Meta:
        verbose_name = 'Variante'
        verbose_name_plural = 'Variantes'
        unique_together = [('product', 'size', 'color')]

    def __str__(self):
        parts = [self.product.name]
        if self.color:
            parts.append(self.color.name)
        if self.size:
            parts.append(self.size.name)
        return ' — '.join(parts)

    def save(self, *args, **kwargs):
        if not self.sku:
            import uuid
            self.sku = f'{self.product.sku}-{str(uuid.uuid4())[:6].upper()}'
        super().save(*args, **kwargs)

    @property
    def effective_price(self):
        return self.price_override if self.price_override else self.product.price

    @property
    def is_in_stock(self):
        return self.stock > 0
