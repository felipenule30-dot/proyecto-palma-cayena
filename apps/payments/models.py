from django.db import models
from apps.orders.models import Order


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('approved', 'Aprobado'),
        ('declined', 'Rechazado'),
        ('voided', 'Anulado'),
        ('error', 'Error'),
    ]
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment', verbose_name='Pedido')
    gateway = models.CharField('Pasarela', max_length=30, default='wompi')
    transaction_id = models.CharField('ID transacción', max_length=150, blank=True)
    reference = models.CharField('Referencia', max_length=150, blank=True, unique=True)
    amount = models.DecimalField('Monto', max_digits=12, decimal_places=2)
    currency = models.CharField('Moneda', max_length=10, default='COP')
    status = models.CharField('Estado', max_length=20, choices=STATUS_CHOICES, default='pending')
    gateway_response = models.JSONField('Respuesta de pasarela', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        ordering = ['-created_at']

    def __str__(self):
        return f'Pago {self.reference} — {self.get_status_display()}'
