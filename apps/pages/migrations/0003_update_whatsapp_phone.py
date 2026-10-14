from django.db import migrations


NEW_PHONE = "+57 320 8825140"


def set_phone(apps, schema_editor):
    SiteConfig = apps.get_model("core", "SiteConfig")
    SiteConfig.objects.filter(pk=1).update(phone=NEW_PHONE)


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0002_update_homepage_content"),
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(set_phone, migrations.RunPython.noop),
    ]
