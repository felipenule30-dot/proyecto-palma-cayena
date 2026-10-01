from django.shortcuts import render, redirect
from django.conf import settings
from .forms import CheckoutForm
from apps.cart.cart import Cart
from apps.orders.models import Order, OrderItem
from apps.payments.models import Payment
import hashlib


def checkout(request):
    cart = Cart(request)
    if not cart:
        return redirect('cart:detail')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            order = Order.objects.create(
                first_name=d['first_name'],
                last_name=d['last_name'],
                email=d['email'],
                phone=d['phone'],
                country=d['country'],
                department=d.get('department', ''),
                city=d['city'],
                address=d['address'],
                postal_code=d.get('postal_code', ''),
                notes=d.get('notes', ''),
                subtotal=cart.get_subtotal(),
                shipping_cost=cart.get_shipping_cost(),
                total=cart.get_total(),
            )
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product_name=item['product_name'],
                    product_slug=item['product_slug'],
                    variant_info=item['variant_info'],
                    sku=item['sku'],
                    quantity=item['quantity'],
                    unit_price=item['price'],
                    image_url=item.get('image_url', ''),
                )
            
            payment = Payment.objects.create(
                order=order,
                amount=order.total,
                reference=order.order_number,
            )
            
            request.session['pending_order_id'] = order.id
            cart.clear()
            return redirect('checkout:payment', order_number=order.order_number)
    else:
        form = CheckoutForm()

    context = {
        'form': form,
        'cart': cart,
        'meta_title': 'Checkout — Palma Cayena',
    }
    return render(request, 'checkout/checkout.html', context)


def payment_page(request, order_number):
    try:
        order = Order.objects.get(order_number=order_number)
    except Order.DoesNotExist:
        return redirect('pages:home')

    wompi_public_key = settings.WOMPI_PUBLIC_KEY
    # Amount in cents for Wompi
    amount_in_cents = int(order.total * 100)
    currency = 'COP'

    # Firma de integridad exigida por el Widget/Checkout de Wompi:
    # SHA256(reference + amountInCents + currency + integritySecret)
    integrity_signature = ''
    if settings.WOMPI_INTEGRITY_SECRET:
        signature_string = f'{order.order_number}{amount_in_cents}{currency}{settings.WOMPI_INTEGRITY_SECRET}'
        integrity_signature = hashlib.sha256(signature_string.encode('utf-8')).hexdigest()

    context = {
        'order': order,
        'wompi_public_key': wompi_public_key,
        'wompi_sandbox': settings.WOMPI_SANDBOX,
        'amount_in_cents': amount_in_cents,
        'currency': currency,
        'integrity_signature': integrity_signature,
        'meta_title': f'Pago pedido #{order.order_number} — Palma Cayena',
    }
    return render(request, 'checkout/payment.html', context)


def order_confirmation(request, order_number):
    try:
        order = Order.objects.prefetch_related('items').get(order_number=order_number)
    except Order.DoesNotExist:
        return redirect('pages:home')
    return render(request, 'checkout/confirmation.html', {
        'order': order,
        'meta_title': f'¡Pedido confirmado! #{order.order_number} — Palma Cayena',
    })
