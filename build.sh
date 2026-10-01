#!/usr/bin/env bash
# Script de build para Render. Se ejecuta en cada despliegue.
set -o errexit

pip install -r requirements.txt

# Archivos estáticos (CSS, JS, fuentes) servidos por WhiteNoise
python manage.py collectstatic --no-input

# Aplica migraciones a la base de datos (Supabase)
python manage.py migrate
