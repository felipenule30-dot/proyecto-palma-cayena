# Despliegue de Palma Cayena en un servidor propio (VPS)

Guía para montar la tienda en un servidor Linux (Ubuntu/Debian) con Nginx + Gunicorn.

> La **base de datos (Supabase)** y las **imágenes (Supabase Storage)** son externas:
> el servidor solo se conecta a ellas. **No se migran datos** — los pedidos, productos
> y fotos siguen viviendo en Supabase. Solo se mueve la aplicación (el código).

## 1. Requisitos del servidor
- Python **3.12**
- Nginx (como proxy inverso + HTTPS)
- Un dominio apuntando al servidor (el dueño mueve el DNS)
- Git

## 2. Clonar y preparar el entorno
```bash
git clone https://github.com/felipenule30-dot/proyecto-palma-cayena.git
cd proyecto-palma-cayena
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 3. Variables de entorno (.env)
Crear un archivo `.env` en la raíz con TODAS estas variables.
**Los valores reales los entrega el dueño por un canal seguro** (no están en el repo):

```bash
DJANGO_SETTINGS_MODULE=config.settings.production
SECRET_KEY=              # provisto por el dueño
ALLOWED_HOSTS=palmacayena.com,www.palmacayena.com
CSRF_TRUSTED_ORIGINS=https://palmacayena.com,https://www.palmacayena.com
ADMIN_URL=               # ruta secreta del panel (provista por el dueño)
SITE_URL=https://palmacayena.com

# Base de datos (Supabase — Session pooler)
DB_NAME=postgres
DB_USER=                 # provisto por el dueño
DB_PASSWORD=             # provisto por el dueño
DB_HOST=                 # provisto por el dueño
DB_PORT=5432

# Wompi
WOMPI_PUBLIC_KEY=        # provisto por el dueño
WOMPI_PRIVATE_KEY=       # provisto por el dueño
WOMPI_EVENTS_SECRET=     # provisto por el dueño
WOMPI_INTEGRITY_SECRET=  # provisto por el dueño
WOMPI_SANDBOX=True

# Almacenamiento de imágenes (Supabase Storage, S3)
AWS_STORAGE_BUCKET_NAME=media
AWS_ACCESS_KEY_ID=       # provisto por el dueño
AWS_SECRET_ACCESS_KEY=   # provisto por el dueño
AWS_S3_ENDPOINT_URL=     # provisto por el dueño
AWS_S3_REGION_NAME=us-east-1
AWS_S3_CUSTOM_DOMAIN=    # provisto por el dueño

# Superusuario (opcional, solo para crear/restablecer admin al arrancar)
DJANGO_SUPERUSER_USERNAME=   # provisto por el dueño
DJANGO_SUPERUSER_EMAIL=      # provisto por el dueño
DJANGO_SUPERUSER_PASSWORD=   # provisto por el dueño
```

> Ajustar `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` y `SITE_URL` si se usa un dominio o
> IP distinta durante las pruebas.

## 4. Build (estáticos + migraciones)
```bash
export $(grep -v '^#' .env | xargs)   # cargar variables (o usar un gestor)
bash build.sh
```
`build.sh` hace: `collectstatic`, `migrate`, carga el seed solo si la BD está vacía
(no aplica aquí porque Supabase ya tiene datos), y crea el superusuario si se definieron
las variables `DJANGO_SUPERUSER_*`.

## 5. Servir con Gunicorn (ejemplo con systemd)
`/etc/systemd/system/palmacayena.service`:
```ini
[Unit]
Description=Palma Cayena (gunicorn)
After=network.target

[Service]
User=www-data
WorkingDirectory=/ruta/a/proyecto-palma-cayena
EnvironmentFile=/ruta/a/proyecto-palma-cayena/.env
ExecStart=/ruta/a/proyecto-palma-cayena/venv/bin/gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 3
Restart=always

[Install]
WantedBy=multi-user.target
```
```bash
sudo systemctl enable --now palmacayena
```

## 6. Nginx (proxy inverso) + HTTPS
La app **obliga HTTPS** (redirección + HSTS) y confía en el header `X-Forwarded-Proto`,
así que Nginx debe terminar el SSL y pasar ese header.

`/etc/nginx/sites-available/palmacayena`:
```nginx
server {
    server_name palmacayena.com www.palmacayena.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
```bash
sudo ln -s /etc/nginx/sites-available/palmacayena /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
# HTTPS gratis con Let's Encrypt:
sudo certbot --nginx -d palmacayena.com -d www.palmacayena.com
```

## 7. Notas
- WhiteNoise sirve los estáticos (CSS/JS/fuentes), no hace falta configurarlos en Nginx.
- Las imágenes subidas van a Supabase Storage (no al disco del servidor).
- El webhook de Wompi sigue siendo `https://palmacayena.com/pagos/webhook/wompi/`
  (no cambia si el dominio sigue igual).
- Para actualizar: `git pull`, `bash build.sh`, `sudo systemctl restart palmacayena`.
