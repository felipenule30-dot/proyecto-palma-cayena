from urllib.parse import quote, unquote

MARKER = "/storage/v1/object/public/media/"
WIDTHS = (640, 1280)


def resized_url(url, width):
    """Public URL of the pre-generated WebP for this photo."""
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
    new_path = f"opt/w{width}/{stem}.webp"
    encoded = "/".join(quote(part) for part in new_path.split("/"))
    return f"{base}{MARKER}{encoded}"


def write_variants_for_name(name):
    """Create opt/w640 and opt/w1280 WebP copies for a stored media path."""
    import io

    from django.core.files.base import ContentFile
    from django.core.files.storage import default_storage
    from PIL import Image, ImageOps

    if not name or name.startswith("opt/"):
        return
    stem = name.rsplit(".", 1)[0]
    missing = [w for w in WIDTHS if not default_storage.exists(f"opt/w{w}/{stem}.webp")]
    if not missing:
        return

    with default_storage.open(name, "rb") as handle:
        image = ImageOps.exif_transpose(Image.open(io.BytesIO(handle.read())))
    if image.mode in ("RGBA", "LA") or (image.mode == "P" and "transparency" in image.info):
        image = image.convert("RGBA")
    else:
        image = image.convert("RGB")

    for width in missing:
        variant = image.copy()
        variant.thumbnail((width, 20000), Image.Resampling.LANCZOS)
        buffer = io.BytesIO()
        variant.save(buffer, format="WEBP", quality=72, method=4)
        key = f"opt/w{width}/{stem}.webp"
        # Bypass get_available_name so the key matches what resized_url() expects.
        default_storage._save(key, ContentFile(buffer.getvalue()))


def ensure_variants(instance):
    """Create the small WebP copies when a photo is saved."""
    from django.db import transaction
    from django.db.models import ImageField

    names = []
    for field in instance._meta.fields:
        if not isinstance(field, ImageField):
            continue
        uploaded = getattr(instance, field.name, None)
        name = getattr(uploaded, "name", "") or ""
        if name and not name.startswith("opt/"):
            names.append(name)

    if not names:
        return

    def _run():
        for name in names:
            write_variants_for_name(name)

    transaction.on_commit(_run)
