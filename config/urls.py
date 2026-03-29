from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from apps.shop.sitemaps import ProductSitemap, CategorySitemap
from apps.pages.sitemaps import PageSitemap

admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.site_title = settings.ADMIN_SITE_TITLE
admin.site.index_title = settings.ADMIN_INDEX_TITLE

sitemaps = {
    'products': ProductSitemap,
    'categories': CategorySitemap,
    'pages': PageSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    # Rutas con prefijo específico — deben ir ANTES del catch-all de pages
    path('tienda/', include('apps.shop.urls')),
    path('carrito/', include('apps.cart.urls')),
    path('checkout/', include('apps.checkout.urls')),
    path('pedidos/', include('apps.orders.urls')),
    path('pagos/', include('apps.payments.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    # Pages al final porque contiene <slug:slug>/ que captura cualquier ruta
    path('', include('apps.pages.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
