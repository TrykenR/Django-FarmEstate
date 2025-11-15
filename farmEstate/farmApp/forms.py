from django import forms
from .models import TablaDatos, Trabajadores, Animales, Huertos, Producciones, ActividadesAnimales, ActividadesHuertos

class TablaDatosForm(forms.ModelForm):
    class Meta:
        model = TablaDatos
        fields = [
            'nombre', 
            'jerarquia', 
            'padre'
        ]

class TrabajadoresForm(forms.ModelForm):
    class Meta:
        model = Trabajadores
        fields = [
            'nombre',
            'telefono',
            'cedula',
            'sueldo'
        ]

class AnimalesForm(forms.ModelForm):
    class Meta:
        model = Animales
        fields = [
            'f_nacimiento', 
            'categoria_a', 
            'raza', 
            'genero', 
            'n_partos'
        ]

class HuertosForm(forms.ModelForm):
    class Meta:
        model = Huertos
        fields = [
            'categoria_h',
            'hectareas',
            'fecha_p'
        ]

class ProduccionesForm(forms.ModelForm):
    class Meta:
        model = Producciones
        fields = [
            'categoria_p',
            'id_trabajadores',
            'fecha_produccion',
            'nombre',
            'peso_cantidad'
        ]

class ActividadesAnimalesForm(forms.ModelForm):
    model = ActividadesAnimales
    fields = [
        'id_animales',
        'id_trabajadores',
        'descripcion',
        'fecha',
        'retorno'
    ]

class ActividadesHuertosForm(forms.ModelForm):
    model = ActividadesHuertos
    fields = [
        'id_huertos',
        'id_trabajadores',
        'descripcion',
        'fecha',
        'retorno'
    ]