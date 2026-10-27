"""
Descarga TODAS las imágenes del bucket de Supabase Storage a una carpeta local
(backup del storage). Se ejecuta desde una máquina con acceso a internet y con
las variables AWS_* configuradas (las mismas del .env de producción).

Uso:
    export AWS_STORAGE_BUCKET_NAME=media
    export AWS_ACCESS_KEY_ID=...            # de Render / Supabase
    export AWS_SECRET_ACCESS_KEY=...        # de Render / Supabase
    export AWS_S3_ENDPOINT_URL=https://aoolmrjrdwepoozqfjmy.storage.supabase.co/storage/v1/s3
    export AWS_S3_REGION_NAME=us-east-1
    python backup_storage.py

Resultado: carpeta ./media_backup/ con todos los archivos del bucket.
Requiere: pip install boto3   (ya está en el entorno del proyecto)
"""
import os
import boto3
from botocore.config import Config

BUCKET = os.environ.get("AWS_STORAGE_BUCKET_NAME", "media")
ENDPOINT = os.environ["AWS_S3_ENDPOINT_URL"]
REGION = os.environ.get("AWS_S3_REGION_NAME", "us-east-1")
OUT_DIR = "media_backup"

s3 = boto3.client(
    "s3",
    endpoint_url=ENDPOINT,
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    region_name=REGION,
    config=Config(s3={"addressing_style": "path"}),  # Supabase requiere path-style
)

paginator = s3.get_paginator("list_objects_v2")
count = 0
for page in paginator.paginate(Bucket=BUCKET):
    for obj in page.get("Contents", []):
        key = obj["Key"]
        dest = os.path.join(OUT_DIR, key)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        s3.download_file(BUCKET, key, dest)
        count += 1
        print("Descargado:", key)

print(f"\nListo: {count} archivo(s) respaldado(s) en ./{OUT_DIR}/")
