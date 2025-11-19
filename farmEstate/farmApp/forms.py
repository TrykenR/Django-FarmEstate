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
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del dato'
            }),
            'jerarquia': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nivel de jerarquía'
            }),
            'padre': forms.Select(attrs={'class': 'form-control'}),
        }

class TrabajadoresForm(forms.ModelForm):
    class Meta:
        model = Trabajadores
        fields = [
            'nombre',
            'telefono',
            'cedula',
            'sueldo'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+57 300 123 4567'
            }),
            'cedula': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de cédula'
            }),
            'sueldo': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sueldo mensual',
                'step': '0.01'
            }),
        }
        labels = {
            'nombre': 'Nombre completo',
            'telefono': 'Teléfono',
            'cedula': 'Cédula de ciudadanía',
            'sueldo': 'Sueldo mensual (COP)'
        }

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
        widgets = {
            'f_nacimiento': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'categoria_a': forms.Select(attrs={'class': 'form-control'}),
            'raza': forms.Select(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'n_partos': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de partos',
                'min': '0'
            }),
        }
        labels = {
            'f_nacimiento': 'Fecha de nacimiento',
            'categoria_a': 'Categoría',
            'raza': 'Raza',
            'genero': 'Género',
            'n_partos': 'Número de partos'
        }
        help_texts = {
            'n_partos': 'Dejar vacío si no aplica',
        }

class HuertosForm(forms.ModelForm):
    class Meta:
        model = Huertos
        fields = [
            'categoria_h',
            'hectareas',
            'fecha_p'
        ]
        widgets = {
            'categoria_h': forms.Select(attrs={'class': 'form-control'}),
            'hectareas': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Hectáreas',
                'step': '0.01',
                'min': '0'
            }),
            'fecha_p': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        }
        labels = {
            'categoria_h': 'Categoría del huerto',
            'hectareas': 'Hectáreas',
            'fecha_p': 'Fecha de plantación'
        }

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
        widgets = {
            'categoria_p': forms.Select(attrs={'class': 'form-control'}),
            'id_trabajadores': forms.Select(attrs={'class': 'form-control'}),
            'fecha_produccion': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del producto'
            }),
            'peso_cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Peso o cantidad',
                'step': '0.01',
                'min': '0'
            }),
        }
        labels = {
            'categoria_p': 'Categoría de producción',
            'id_trabajadores': 'Trabajador responsable',
            'fecha_produccion': 'Fecha de producción',
            'nombre': 'Nombre del producto',
            'peso_cantidad': 'Peso/Cantidad (kg)'
        }

class ActividadesAnimalesForm(forms.ModelForm):
    class Meta:  # ✅ CORREGIDO: Ahora tiene class Meta
        model = ActividadesAnimales
        fields = [
            'id_animales',
            'id_trabajadores',
            'descripcion',
            'fecha',
            'retorno'
        ]
        widgets = {
            'id_animales': forms.Select(attrs={'class': 'form-control'}),
            'id_trabajadores': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción de la actividad'
            }),
            'fecha': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'retorno': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Retorno económico',
                'step': '0.01'
            }),
        }
        labels = {
            'id_animales': 'Animal',
            'id_trabajadores': 'Trabajador responsable',
            'descripcion': 'Descripción',
            'fecha': 'Fecha de la actividad',
            'retorno': 'Retorno (COP)'
        }

class ActividadesHuertosForm(forms.ModelForm):
    class Meta:  # ✅ CORREGIDO: Ahora tiene class Meta
        model = ActividadesHuertos
        fields = [
            'id_huerto',
            'id_trabajadores',
            'descripcion',
            'fecha',
            'retorno'
        ]
        widgets = {
            'id_huerto': forms.Select(attrs={'class': 'form-control'}),
            'id_trabajadores': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción de la actividad'
            }),
            'fecha': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'retorno': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Retorno económico',
                'step': '0.01'
            }),
        }
        labels = {
            'id_huerto': 'Huerto',
            'id_trabajadores': 'Trabajador responsable',
            'descripcion': 'Descripción',
            'fecha': 'Fecha de la actividad',
            'retorno': 'Retorno (COP)'
        }
        