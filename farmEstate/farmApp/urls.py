from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('trabajadores/', views.listar_trabajadores, name='listar_trabajadores'),
    path('trabajadores/nuevo/', views.crear_trabajador, name='crear_trabajador'),
    path('animales/', views.listar_animales, name='listar_animales'),
    path('animales/nuevo/', views.crear_animal, name='crear_animal'),
    path("login/", views.login_trabajador, name="login"),
    path("salir/", views.salir, name="salir"),
    path("panel/", views.dashboard, name="dashboard"),
]

