from django.contrib import admin
from .models import TablaDatos, Trabajadores, Animales, Huertos, Producciones, ActividadesAnimales, ActividadesHuertos

admin.site.register(TablaDatos)
admin.site.register(Trabajadores)
admin.site.register(Animales)
admin.site.register(Huertos)
admin.site.register(Producciones)
admin.site.register(ActividadesAnimales)
admin.site.register(ActividadesHuertos)
