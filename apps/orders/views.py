from django.shortcuts import render, get_object_or_404
from .models import Order


def order_tracking(request):
    order = None
    error = None
    if request.method == 'POST':
        order_number = request.POST.get('order_number', '').strip()
        email = request.POST.get('email', '').strip()
        try:
            order = Order.objects.prefetch_related('items').get(
                order_number=order_number, email__iexact=email
            )
        except Order.DoesNotExist:
            error = 'No encontramos un pedido con esos datos. Revisa el número y el email.'
    return render(request, 'orders/tracking.html', {
        'order': order,
        'error': error,
        'meta_title': 'Seguimiento de pedido — Palma Cayena',
    })
