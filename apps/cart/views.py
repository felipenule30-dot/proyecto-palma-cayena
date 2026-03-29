from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .cart import Cart
from apps.shop.models import ProductVariant


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart.html', {'cart': cart})


@require_POST
def cart_add(request):
    cart = Cart(request)
    variant_id = request.POST.get('variant_id')
    quantity = int(request.POST.get('quantity', 1))
    if not variant_id:
        return JsonResponse({'error': 'Variante requerida'}, status=400)
    cart.add(int(variant_id), quantity=quantity)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': cart.get_item_count(),
            'subtotal': str(cart.get_subtotal()),
        })
    return redirect('cart:detail')


@require_POST
def cart_remove(request):
    cart = Cart(request)
    variant_id = request.POST.get('variant_id')
    if variant_id:
        cart.remove(int(variant_id))
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'cart_count': cart.get_item_count()})
    return redirect('cart:detail')


@require_POST
def cart_update(request):
    cart = Cart(request)
    variant_id = request.POST.get('variant_id')
    quantity = int(request.POST.get('quantity', 1))
    if variant_id:
        cart.update_quantity(int(variant_id), quantity)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': cart.get_item_count(),
            'subtotal': str(cart.get_subtotal()),
        })
    return redirect('cart:detail')
