from django.db import migrations


def remove_xl(apps, schema_editor):
    # Quita la talla XL del catálogo (y por tanto de los filtros de la tienda).
    # ProductVariant.size es SET_NULL, así que no se elimina ninguna variante.
    Size = apps.get_model("shop", "Size")
    Size.objects.filter(name__iexact="XL").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0003_reorder_sizes"),
    ]

    operations = [
        migrations.RunPython(remove_xl, migrations.RunPython.noop),
    ]
