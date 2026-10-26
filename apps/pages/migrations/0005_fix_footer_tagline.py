# -*- coding: utf-8 -*-
from django.db import migrations


NEW_TAGLINE = "Nacida del Caribe. Diseñada para la mujer que lleva el mar adentro."


def set_tagline(apps, schema_editor):
    SiteConfig = apps.get_model("core", "SiteConfig")
    SiteConfig.objects.filter(pk=1).update(site_tagline=NEW_TAGLINE)


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0004_journal_nuestro_universo"),
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(set_tagline, migrations.RunPython.noop),
    ]
