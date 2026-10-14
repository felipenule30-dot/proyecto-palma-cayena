import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = (
        'Restablece (o crea) el superusuario del panel usando variables de entorno. '
        'Pensado para hosting sin consola (Render Free). Define ADMIN_RESET_PASSWORD, '
        'redespliega, verifica el acceso y LUEGO borra esa variable.'
    )

    def handle(self, *args, **options):
        User = get_user_model()

        password = (os.environ.get('ADMIN_RESET_PASSWORD') or '').strip()
        if not password:
            self.stdout.write('ADMIN_RESET_PASSWORD no esta definida; no se cambia nada.')
            return

        username = (
            os.environ.get('ADMIN_RESET_USERNAME')
            or os.environ.get('DJANGO_SUPERUSER_USERNAME')
            or 'admin'
        )
        email = (
            os.environ.get('ADMIN_RESET_EMAIL')
            or os.environ.get('DJANGO_SUPERUSER_EMAIL')
            or ''
        )

        user, created = User.objects.get_or_create(
            username=username, defaults={'email': email}
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        if email:
            user.email = email
        user.save()

        accion = 'creado' if created else 'actualizado'
        # Nunca se imprime la contraseña.
        self.stdout.write(self.style.SUCCESS(
            f'>> Superusuario "{username}" {accion}: contrasena restablecida con exito.'
        ))
