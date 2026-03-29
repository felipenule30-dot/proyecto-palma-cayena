import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_PAID = 'paid'
    STATUS_PROCESSING = 'processing'
    STATUS_SHIPPED = 'shipped'
    STATUS_DELIVERED = 'delivered'
    STATUS_CANCELLED = 'cancelled'
    STATUS_REFUNDED = 'refunded'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pendiente'),
        (STATUS_PAID, 'Pagado'),
        (STATUS_PROCESSING, 'En preparación'),
        (STATUS_SHIPPED, 'Enviado'),
        (STATUS_DELIVERED, 'Entregado'),
        (STATUS_CANCELLED, 'Cancelado'),
        (STATUS_REFUNDED, 'Reembolsado'),
    ]

    PAYMENT_CHOICES = [
        ('wompi', 'Wompi'),
        ('transfer', 'Transferencia'),
        ('cash', 'Efectivo'),
        ('other', 'Otro'),
    ]

    order_number = models.CharField('Número de pedido', max_length=20, unique=True, blank=True)

    # Customer info
    first_name = models.CharField('Nombre', max_length=100)
    last_name = models.CharField('Apellido', max_length=100)
    email = models.EmailField('Email')
    phone = models.CharField('Teléfono', max_length=20, blank=True)

    # Shipping
    country = models.CharField('País', max_length=100, default='Colombia')
    city = models.CharField('Ciudad', max_length=100)
    department = models.CharField('Departamento', max_length=100, blank=True)
    address = models.TextField('Dirección completa')
    postal_code = models.CharField('Código postal', max_length=20, blank=True)
    notes = models.TextField('Notas del pedido', blank=True)

    # Pricing
    subtotal = models.DecimalField('Subtotal', max_digits=12, decimal_places=2, default=0)
    shipping_cost = models.DecimalField('Costo de envío', max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField('Descuento', max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField('Total', max_digits=12, decimal_places=2, default=0)

    # Status
    status = models.CharField('Estado', max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    payment_method = models.CharField('Método de pago', max_length=20, choices=PAYMENT_CHOICES, default='wompi')
    payment_status = models.CharField('Estado del pago', max_length=50, blank=True)
    wompi_transaction_id = models.CharField('ID transacción Wompi', max_length=100, blank=True)

    # Tracking
    tracking_number = models.CharField('Número de guía', max_length=100, blank=True)
    carrier = models.CharField('Transportadora', max_length=100, blank=True)

    # Internal
    admin_notes = models.TextField('Notas internas', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField('Pagado en', null=True, blank=True)
    shipped_at = models.DateTimeField('Enviado en', null=True, blank=True)

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-created_at']

    def __str__(self):
        return f'Pedido #{self.order_number}'

    def save(self, *args, **kwargs):
        if not self.order_number:
            import random, string
            self.order_number = 'PC-' + ''.join(random.choices(string.digits, k=6))
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def item_count(self):
        return sum(item.quantity for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Pedido')
    product_name = models.CharField('Nombre del producto', max_length=200)
    product_slug = models.CharField('Slug del producto', max_length=250, blank=True)
    variant_info = models.CharField('Variante (talla / color)', max_length=100, blank=True)
    sku = models.CharField('SKU', max_length=80, blank=True)
    quantity = models.PositiveIntegerField('Cantidad', default=1)
    unit_price = models.DecimalField('Precio unitario', max_digits=12, decimal_places=2)
    total_price = models.DecimalField('Total línea', max_digits=12, decimal_places=2)
    image_url = models.URLField('URL imagen', blank=True)

    class Meta:
        verbose_name = 'Línea de pedido'
        verbose_name_plural = 'Líneas de pedido'

    def __str__(self):
        return f'{self.quantity}x {self.product_name}'

    def save(self, *args, **kwargs):
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)
