from django.db import migrations


SLUG = "producto-prueba-2000"


def create_test_product(apps, schema_editor):
    Product = apps.get_model("shop", "Product")
    ProductVariant = apps.get_model("shop", "ProductVariant")
    Size = apps.get_model("shop", "Size")
    Color = apps.get_model("shop", "Color")
    Category = apps.get_model("shop", "Category")

    if Product.objects.filter(slug=SLUG).exists():
        return

    cat = Category.objects.order_by("order").first()
    size = Size.objects.filter(name__iexact="S").first() or Size.objects.order_by("order").first()
    color = Color.objects.order_by("order").first()

    p = Product.objects.create(
        name="Producto de prueba",
        slug=SLUG,
        sku="TEST-2000",
        category=cat,
        short_description="Producto temporal para probar el pago. Eliminar después.",
        price=2000,
        status="active",
        is_new=False,
        is_featured=False,
        order=999,
    )
    if color:
        p.colors.set([color])
    if size:
        p.sizes.set([size])
    ProductVariant.objects.get_or_create(
        product=p,
        size=size,
        color=color,
        defaults={"stock": 50, "is_active": True, "sku": "TEST-2000-S"},
    )


def remove_test_product(apps, schema_editor):
    Product = apps.get_model("shop", "Product")
    Product.objects.filter(slug=SLUG).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0004_remove_xl_size"),
    ]

    operations = [
        migrations.RunPython(create_test_product, remove_test_product),
    ]
