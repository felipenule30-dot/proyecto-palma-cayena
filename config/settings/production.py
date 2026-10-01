from .base import *

DEBUG = False

# --- HTTPS / proxy (Render, Heroku y similares terminan el SSL en un proxy) ---
# Sin esto, con SECURE_SSL_REDIRECT=True el sitio entra en bucle de redirección.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True

# --- HSTS: fuerza HTTPS en el navegador por 1 año ---
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# --- Cookies solo por HTTPS ---
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# --- Cabeceras de seguridad adicionales ---
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# --- Email real para confirmaciones de pedido ---
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
