from django.db import models


class Customer(models.Model):
    first_name = models.CharField('Nombre', max_length=100)
    last_name = models.CharField('Apellido', max_length=100)
    email = models.EmailField('Email', unique=True)
    phone = models.CharField('Teléfono', max_length=20, blank=True)
    city = models.CharField('Ciudad', max_length=100, blank=True)
    country = models.CharField('País', max_length=100, default='Colombia')
    newsletter = models.BooleanField('Suscrito newsletter', default=False)
    notes = models.TextField('Notas internas', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.first_name} {self.last_name} <{self.email}>'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
