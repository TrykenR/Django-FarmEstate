from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('trabajadores/', views.listar_trabajadores, name='listar_trabajadores'),
    path('trabajadores/nuevo/', views.crear_trabajador, name='crear_trabajador'),
    path('animales/', views.listar_animales, name='listar_animales'),
    path('animales/nuevo/', views.crear_animal, name='crear_animal'),
]

