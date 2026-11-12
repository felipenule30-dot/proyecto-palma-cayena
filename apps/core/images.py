import logging
from urllib.parse import quote, unquote

MARKER = "/storage/v1/object/public/media/"
WIDTHS = (640, 1280)
logger = logging.getLogger(__name__)

# Per-process cache so we don't HEAD S3 on every image of every request.
_opt_status = {}


def resized_url(url, width):
    """Public URL of the WebP copy, or the original if that copy is missing."""
    if not url:
        return url
    url = str(url)
    if MARKER not in url:
        return url
    try:
        width = int(width)
    except (TypeError, ValueError):
        return url
    base, path = url.split(MARKER, 1)
    path = unquote(path.split("?", 1)[0])
    if path.startswith("opt/"):
        return url
    stem = path.rsplit(".", 1)[0]
    opt_key = f"opt/w{width}/{stem}.webp"
    if not _variant_exists(opt_key):
        return url
    encoded = "/".join(quote(part) for part in opt_key.split("/"))
    return f"{base}{MARKER}{encoded}"


def _variant_exists(key):
    cached = _opt_status.get(key)
    if cached is not None:
        return cached
    try:
        from django.core.files.storage import default_storage
        exists = default_storage.exists(key)
    except Exception:
        exists = False
    _opt_status[key] = exists
    return exists


def mark_variant_present(key):
    _opt_status[key] = True


def write_variants_for_name(name):
    """Create opt/w640 and opt/w1280 WebP copies for a stored media path."""
    import io
    import os

    from PIL import Image, ImageOps

    if not name or str(name).startswith("opt/"):
        return

    name = str(name)
    stem = name.rsplit(".", 1)[0]
    bucket = os.environ.get("AWS_STORAGE_BUCKET_NAME", "")
    if not bucket:
        return

    from django.core.files.storage import default_storage

    with default_storage.open(name, "rb") as handle:
        raw = handle.read()
    image = ImageOps.exif_transpose(Image.open(io.BytesIO(raw)))
    if image.mode in ("RGBA", "LA") or (image.mode == "P" and "transparency" in image.info):
        image = image.convert("RGBA")
    else:
        image = image.convert("RGB")

    import boto3
    from botocore.config import Config

    client = boto3.client(
        "s3",
        endpoint_url=os.environ.get("AWS_S3_ENDPOINT_URL") or None,
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_S3_REGION_NAME", "us-east-1"),
        config=Config(s3={"addressing_style": os.environ.get("AWS_S3_ADDRESSING_STYLE", "path")}),
    )

    for width in WIDTHS:
        variant = image.copy()
        variant.thumbnail((width, 20000), Image.Resampling.LANCZOS)
        buffer = io.BytesIO()
        variant.save(buffer, format="WEBP", quality=72, method=4)
        key = f"opt/w{width}/{stem}.webp"
        client.put_object(
            Bucket=bucket,
            Key=key,
            Body=buffer.getvalue(),
            ContentType="image/webp",
            CacheControl="public, max-age=31536000, immutable",
        )
        mark_variant_present(key)


def ensure_variants(instance):
    """Create the small WebP copies when a photo is saved."""
    from django.db.models import ImageField

    for field in instance._meta.fields:
        if not isinstance(field, ImageField):
            continue
        uploaded = getattr(instance, field.name, None)
        name = getattr(uploaded, "name", "") or ""
        if not name or name.startswith("opt/"):
            continue
        try:
            write_variants_for_name(name)
        except Exception:
            logger.exception("No se pudo generar WebP para %s", name)
