from django.contrib import admin
from .models import TablaDatos, Trabajadores, Animales, Huertos, Producciones, ActividadesAnimales, ActividadesHuertos

@admin.register(TablaDatos)
class TablaDatosAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'jerarquia', 'padre', 'tipo_dato')
    list_filter = ('jerarquia',)
    search_fields = ('nombre',)
    ordering = ('jerarquia', 'nombre')
    
    def tipo_dato(self, obj):
        tipos = {
            1: '📁 Categoría Animal',
            2: '🐾 Raza',
            3: '⚧ Género',
            4: '🌱 Categoría Huerto',
            5: '📦 Categoría Producción'
        }
        return tipos.get(obj.jerarquia, 'Otro')
    tipo_dato.short_description = 'Tipo'
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'jerarquia')
        }),
        ('Relación', {
            'fields': ('padre',),
            'description': 'Opcional: Vincula este dato con otro (ej: una raza con una categoría)'
        }),
    )

@admin.register(Trabajadores)
class TrabajadoresAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cedula', 'telefono', 'sueldo', 'usuario')
    search_fields = ('nombre', 'cedula')
    list_filter = ('sueldo',)
    ordering = ('nombre',)
    
    fieldsets = (
        ('Datos Personales', {
            'fields': ('nombre', 'cedula', 'telefono')
        }),
        ('Información Laboral', {
            'fields': ('sueldo', 'usuario')
        }),
    )

@admin.register(Animales)
class AnimalesAdmin(admin.ModelAdmin):
    list_display = ('id', 'categoria_a', 'raza', 'genero', 'f_nacimiento', 'n_partos')
    list_filter = ('categoria_a', 'raza', 'genero')
    search_fields = ('categoria_a__nombre', 'raza__nombre')
    date_hierarchy = 'f_nacimiento'
    ordering = ('-f_nacimiento',)

@admin.register(Huertos)
class HuertosAdmin(admin.ModelAdmin):
    list_display = ('id', 'categoria_h', 'hectareas', 'fecha_p')
    list_filter = ('categoria_h',)
    date_hierarchy = 'fecha_p'
    ordering = ('-fecha_p',)

@admin.register(Producciones)
class ProduccionesAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria_p', 'id_trabajadores', 'fecha_produccion', 'peso_cantidad')
    list_filter = ('categoria_p', 'fecha_produccion')
    search_fields = ('nombre', 'id_trabajadores__nombre')
    date_hierarchy = 'fecha_produccion'
    ordering = ('-fecha_produccion',)

@admin.register(ActividadesAnimales)
class ActividadesAnimalesAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_animales', 'id_trabajadores', 'descripcion', 'fecha', 'retorno')
    list_filter = ('fecha', 'id_trabajadores')
    search_fields = ('descripcion',)
    date_hierarchy = 'fecha'
    ordering = ('-fecha',)

@admin.register(ActividadesHuertos)
class ActividadesHuertosAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_huerto', 'id_trabajadores', 'descripcion', 'fecha', 'retorno')
    list_filter = ('fecha', 'id_trabajadores')
    search_fields = ('descripcion',)
    date_hierarchy = 'fecha'
    ordering = ('-fecha',)