from django.db import migrations


# Orden deseado de las tallas en los filtros de la tienda.
SIZE_ORDER = {"XS": 0, "S": 1, "M": 2, "L": 3, "XL": 4}


def reorder_sizes(apps, schema_editor):
    Size = apps.get_model("shop", "Size")
    for name, order in SIZE_ORDER.items():
        Size.objects.filter(name__iexact=name).update(order=order)


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0002_clear_discounts"),
    ]

    operations = [
        migrations.RunPython(reorder_sizes, migrations.RunPython.noop),
    ]
