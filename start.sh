#!/usr/bin/env bash
# Arranque en Railway. Las migraciones van aquí (no en el build) porque
# la red privada de Postgres solo está disponible cuando el servicio ya corre.
set -o errexit

python manage.py collectstatic --no-input
python manage.py migrate

if python -c "import os, django; os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings.production'); django.setup(); import sys; from apps.shop.models import Product; sys.exit(0 if Product.objects.exists() else 1)"; then
  echo ">> La base ya tiene productos — se omite la carga de datos de ejemplo."
else
  echo ">> Base vacía — cargando datos iniciales (seed)..."
  python run_seed.py
fi

python manage.py createsuperuser --noinput 2>/dev/null && echo ">> Superusuario creado." || echo ">> Superusuario ya existe o faltan variables DJANGO_SUPERUSER_* (ok)."

if [ -n "${ADMIN_RESET_PASSWORD:-}" ]; then
  echo ">> ADMIN_RESET_PASSWORD detectada — restableciendo contraseña del admin..."
  python manage.py reset_admin
fi

exec gunicorn config.wsgi:application --bind "0.0.0.0:${PORT:-8000}"
