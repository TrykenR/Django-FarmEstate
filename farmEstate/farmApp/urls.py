from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("login/", views.login_trabajador, name="login"),
    
    path("salir/", views.salir, name="salir"),
    path("panel/", views.dashboard, name="dashboard"),
    
    path('trabajadores/', views.listar_trabajadores, name='listar_trabajadores'),
    path('trabajadores/nuevo/', views.crear_trabajador, name='crear_trabajador'),
    path('trabajadores/<int:pk>/editar/', views.editar_trabajador, name='editar_trabajador'),
    path('trabajadores/<int:pk>/eliminar/', views.eliminar_trabajador, name='eliminar_trabajador'),
    
    path('animales/', views.listar_animales, name='listar_animales'),
    path('animales/nuevo/', views.crear_animal, name='crear_animal'),
    path('animales/<int:pk>/editar/', views.editar_animal, name='editar_animal'),
    path('animales/<int:pk>/eliminar/', views.eliminar_animal, name='eliminar_animal'),
    
    path('huertos/', views.listar_huertos, name='listar_huertos'),
    path('huertos/nuevo/', views.crear_huerto, name='crear_huerto'),
    path('huertos/<int:pk>/editar/', views.editar_huerto, name='editar_huerto'),
    path('huertos/<int:pk>/eliminar/', views.eliminar_huerto, name='eliminar_huerto'),
    
    path('producciones/', views.listar_producciones, name='listar_producciones'),
    path('producciones/nuevo/', views.crear_produccion, name='crear_produccion'),
]