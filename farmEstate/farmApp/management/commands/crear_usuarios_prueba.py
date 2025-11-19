from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from farmApp.models import Trabajadores

class Command(BaseCommand):
    help = 'Crea usuarios de prueba y los vincula con trabajadores'

    def handle(self, *args, **kwargs):
        # Datos de usuarios de prueba
        usuarios_prueba = [
            {
                'username': 'jperez',
                'password': 'granja123',
                'trabajador': {
                    'nombre': 'Juan Pérez',
                    'telefono': '3001234567',
                    'cedula': '1234567890',
                    'sueldo': 1500000.0
                }
            },
            {
                'username': 'mgomez',
                'password': 'granja123',
                'trabajador': {
                    'nombre': 'María Gómez',
                    'telefono': '3009876543',
                    'cedula': '0987654321',
                    'sueldo': 1800000.0
                }
            },
            {
                'username': 'admin',
                'password': 'admin123',
                'trabajador': {
                    'nombre': 'Administrador',
                    'telefono': '3005555555',
                    'cedula': '1111111111',
                    'sueldo': 3000000.0
                }
            }
        ]

        for dato in usuarios_prueba:
            # Crear usuario si no existe
            user, created = User.objects.get_or_create(
                username=dato['username'],
                defaults={'is_staff': False, 'is_superuser': False}
            )
            
            if created:
                user.set_password(dato['password'])
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Usuario creado: {dato["username"]}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠ Usuario ya existe: {dato["username"]}')
                )
            
            # Crear o actualizar trabajador
            trabajador, t_created = Trabajadores.objects.get_or_create(
                cedula=dato['trabajador']['cedula'],
                defaults={
                    'usuario': user,
                    'nombre': dato['trabajador']['nombre'],
                    'telefono': dato['trabajador']['telefono'],
                    'sueldo': dato['trabajador']['sueldo']
                }
            )
            
            if t_created:
                self.stdout.write(
                    self.style.SUCCESS(f'  ✓ Trabajador creado: {trabajador.nombre}')
                )
            else:
                # Si el trabajador ya existe, vincularlo con el usuario
                if not trabajador.usuario:
                    trabajador.usuario = user
                    trabajador.save()
                    self.stdout.write(
                        self.style.SUCCESS(f'  ✓ Trabajador vinculado: {trabajador.nombre}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'  ⚠ Trabajador ya vinculado: {trabajador.nombre}')
                    )

        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('CREDENCIALES DE ACCESO:'))
        self.stdout.write('='*50)
        for dato in usuarios_prueba:
            self.stdout.write(f"Usuario: {dato['username']}")
            self.stdout.write(f"Contraseña: {dato['password']}")
            self.stdout.write('-'*50)
            