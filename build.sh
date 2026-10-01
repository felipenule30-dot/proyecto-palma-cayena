#!/usr/bin/env bash
# Script de build para Render. Se ejecuta en cada despliegue.
set -o errexit

pip install -r requirements.txt

# Archivos estáticos (CSS, JS, fuentes) servidos por WhiteNoise
python manage.py collectstatic --no-input

# Aplica migraciones a la base de datos (Supabase)
python manage.py migrate

# Carga los datos de ejemplo SOLO si la base está vacía (primer despliegue).
# IMPORTANTE: run_seed.py resetea el catálogo, así que se ejecuta una única vez.
# En despliegues posteriores se omite para no borrar los cambios reales de la tienda.
if python -c "import os, django; os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings.production'); django.setup(); import sys; from apps.shop.models import Product; sys.exit(0 if Product.objects.exists() else 1)"; then
  echo ">> La base ya tiene productos — se omite la carga de datos de ejemplo."
else
  echo ">> Base vacía — cargando datos iniciales (seed)..."
  python run_seed.py
fi
