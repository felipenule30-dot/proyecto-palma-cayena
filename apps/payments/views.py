import json
import hashlib
import hmac
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from django.utils import timezone
from apps.orders.models import Order
from .models import Payment


@csrf_exempt
@require_POST
def wompi_webhook(request):
    """Webhook para recibir notificaciones de Wompi."""
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponse(status=400)

    # Verify signature (Wompi uses SHA256 HMAC)
    signature_header = request.headers.get('X-Event-Checksum', '')
    event_secret = settings.WOMPI_EVENTS_SECRET
    
    if event_secret:
        computed = hmac.new(
            event_secret.encode(), request.body, hashlib.sha256
        ).hexdigest()
        if not hmac.compare_digest(computed, signature_header):
            return HttpResponse(status=401)

    event_type = payload.get('event')
    data = payload.get('data', {})

    if event_type == 'transaction.updated':
        tx = data.get('transaction', {})
        reference = tx.get('reference', '')
        status = tx.get('status', '')
        tx_id = tx.get('id', '')

        try:
            order = Order.objects.get(order_number=reference)
            payment = order.payment
            payment.transaction_id = tx_id
            payment.gateway_response = tx
            if status == 'APPROVED':
                payment.status = 'approved'
                order.status = Order.STATUS_PAID
                order.paid_at = timezone.now()
                order.wompi_transaction_id = tx_id
            elif status in ('DECLINED', 'ERROR'):
                payment.status = 'declined'
            elif status == 'VOIDED':
                payment.status = 'voided'
            payment.save()
            order.save()
        except (Order.DoesNotExist, Payment.DoesNotExist):
            pass

    return HttpResponse(status=200)
