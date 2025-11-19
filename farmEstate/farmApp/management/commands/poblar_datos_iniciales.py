from django.core.management.base import BaseCommand
from farmApp.models import TablaDatos

class Command(BaseCommand):
    help = 'Pobla la tabla TablaDatos con opciones iniciales para el sistema'

    def handle(self, *args, **kwargs):
        self.stdout.write('Poblando datos iniciales...\n')
        
        # Datos a crear: (nombre, jerarquia, padre_nombre)
        datos_iniciales = [
            # JERARQUÍA 1: Categorías de Animales
            ('Ganado Bovino', 1, None),
            ('Ganado Porcino', 1, None),
            ('Aves de Corral', 1, None),
            ('Ganado Ovino', 1, None),
            ('Ganado Caprino', 1, None),
            
            # JERARQUÍA 2: Razas
            ('Holstein', 2, 'Ganado Bovino'),
            ('Jersey', 2, 'Ganado Bovino'),
            ('Brahman', 2, 'Ganado Bovino'),
            ('Angus', 2, 'Ganado Bovino'),
            ('Normando', 2, 'Ganado Bovino'),
            ('Landrace', 2, 'Ganado Porcino'),
            ('Yorkshire', 2, 'Ganado Porcino'),
            ('Duroc', 2, 'Ganado Porcino'),
            ('Gallina Ponedora', 2, 'Aves de Corral'),
            ('Pollo de Engorde', 2, 'Aves de Corral'),
            ('Pato', 2, 'Aves de Corral'),
            ('Merino', 2, 'Ganado Ovino'),
            ('Suffolk', 2, 'Ganado Ovino'),
            ('Alpina', 2, 'Ganado Caprino'),
            ('Saanen', 2, 'Ganado Caprino'),
            
            # JERARQUÍA 3: Géneros
            ('Macho', 3, None),
            ('Hembra', 3, None),
            
            # JERARQUÍA 4: Categorías de Huertos
            ('Hortalizas', 4, None),
            ('Frutales', 4, None),
            ('Granos', 4, None),
            ('Forraje', 4, None),
            ('Tubérculos', 4, None),
            
            # JERARQUÍA 5: Categorías de Producción
            ('Leche', 5, None),
            ('Carne', 5, None),
            ('Huevos', 5, None),
            ('Frutas', 5, None),
            ('Verduras', 5, None),
            ('Granos', 5, None),
            ('Forraje', 5, None),
        ]
        
        creados = 0
        existentes = 0
        
        for nombre, jerarquia, padre_nombre in datos_iniciales:
            # Buscar el padre si existe
            padre = None
            if padre_nombre:
                padre = TablaDatos.objects.filter(nombre=padre_nombre).first()
            
            # Crear o recuperar el dato
            dato, created = TablaDatos.objects.get_or_create(
                nombre=nombre,
                jerarquia=jerarquia,
                defaults={'padre': padre}
            )
            
            if created:
                creados += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Creado: {nombre} (Jerarquía {jerarquia})')
                )
            else:
                existentes += 1
                self.stdout.write(
                    self.style.WARNING(f'⚠ Ya existe: {nombre}')
                )
        
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS(f'Proceso completado:'))
        self.stdout.write(f'  ✓ Registros creados: {creados}')
        self.stdout.write(f'  ⚠ Registros existentes: {existentes}')
        self.stdout.write(f'  📊 Total en BD: {TablaDatos.objects.count()}')
        self.stdout.write('='*60)
        
        # Mostrar resumen por jerarquía
        self.stdout.write('\n📋 Resumen por tipo:')
        self.stdout.write(f'  Categorías de Animales: {TablaDatos.objects.filter(jerarquia=1).count()}')
        self.stdout.write(f'  Razas: {TablaDatos.objects.filter(jerarquia=2).count()}')
        self.stdout.write(f'  Géneros: {TablaDatos.objects.filter(jerarquia=3).count()}')
        self.stdout.write(f'  Categorías de Huertos: {TablaDatos.objects.filter(jerarquia=4).count()}')
        self.stdout.write(f'  Categorías de Producción: {TablaDatos.objects.filter(jerarquia=5).count()}')
