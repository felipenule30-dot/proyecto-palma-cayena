from django.db import migrations


def clear_discounts(apps, schema_editor):
    # Quita todos los descuentos activos: deja compare_price vacío en todos
    # los productos, así no se muestra precio tachado ni badge de -%.
    Product = apps.get_model("shop", "Product")
    Product.objects.all().update(compare_price=None)


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(clear_discounts, migrations.RunPython.noop),
    ]
