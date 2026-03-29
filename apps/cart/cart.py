from decimal import Decimal
from apps.shop.models import ProductVariant, Product
from apps.core.models import SiteConfig


class Cart:
    """Carrito de compras basado en sesión."""

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, variant_id, quantity=1, override_qty=False):
        key = str(variant_id)
        if key not in self.cart:
            try:
                variant = ProductVariant.objects.select_related('product', 'size', 'color').get(id=variant_id)
                self.cart[key] = {
                    'variant_id': variant_id,
                    'product_id': variant.product.id,
                    'product_name': variant.product.name,
                    'product_slug': variant.product.slug,
                    'variant_info': str(variant),
                    'size': variant.size.name if variant.size else '',
                    'color': variant.color.name if variant.color else '',
                    'sku': variant.sku,
                    'price': str(variant.effective_price),
                    'quantity': 0,
                    'image_url': variant.product.main_image.image.url if variant.product.main_image else '',
                }
            except ProductVariant.DoesNotExist:
                return
        if override_qty:
            self.cart[key]['quantity'] = quantity
        else:
            self.cart[key]['quantity'] += quantity
        self.save()

    def remove(self, variant_id):
        key = str(variant_id)
        if key in self.cart:
            del self.cart[key]
            self.save()

    def update_quantity(self, variant_id, quantity):
        key = str(variant_id)
        if key in self.cart:
            if quantity <= 0:
                self.remove(variant_id)
            else:
                self.cart[key]['quantity'] = quantity
                self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session['cart']
        self.session.modified = True

    def __iter__(self):
        for item in self.cart.values():
            item = dict(item)
            item['price'] = Decimal(item['price'])
            item['total'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_subtotal(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def get_shipping_cost(self):
        config = SiteConfig.get()
        subtotal = self.get_subtotal()
        if subtotal >= config.free_shipping_threshold:
            return Decimal('0')
        return config.shipping_cost

    def get_total(self):
        return self.get_subtotal() + self.get_shipping_cost()

    def get_item_count(self):
        return sum(item['quantity'] for item in self.cart.values())
