from django import forms
from .models import TablaDatos, Trabajadores, Animales, Huertos, Producciones, ActividadesAnimales, ActividadesHuertos

class TablaDatosForm(forms.ModelForm):
    class Meta:
        model = TablaDatos
        fields = ['nombre', 'jerarquia', 'padre']
        widgets = {
            'jerarquia': forms.Select(choices=[
                ('', '---------'),
                (1, 'Categoría Animal'),
                (2, 'Raza'),
                (3, 'Género'),
                (4, 'Categoría Huerto'),
                (5, 'Categoría Producción'),
            ])
        }

class TrabajadoresForm(forms.ModelForm):
    class Meta:
        model = Trabajadores
        fields = ['nombre', 'telefono', 'cedula', 'sueldo']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre completo'}),
            'telefono': forms.TextInput(attrs={'placeholder': '3001234567'}),
            'cedula': forms.TextInput(attrs={'placeholder': 'Número de cédula'}),
            'sueldo': forms.NumberInput(attrs={'placeholder': '0.00', 'step': '0.01'}),
        }

class AnimalesForm(forms.ModelForm):
    class Meta:
        model = Animales
        fields = ['f_nacimiento', 'categoria_a', 'raza', 'genero', 'n_partos']
        widgets = {
            'f_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'n_partos': forms.NumberInput(attrs={'min': '0', 'placeholder': 'Opcional'}),
        }
        labels = {
            'f_nacimiento': 'Fecha de Nacimiento',
            'categoria_a': 'Categoría',
            'raza': 'Raza',
            'genero': 'Género',
            'n_partos': 'Número de Partos',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar las opciones según jerarquía
        self.fields['categoria_a'].queryset = TablaDatos.objects.filter(jerarquia=1).order_by('nombre')
        self.fields['raza'].queryset = TablaDatos.objects.filter(jerarquia=2).order_by('nombre')
        self.fields['genero'].queryset = TablaDatos.objects.filter(jerarquia=3).order_by('nombre')
        
        # Hacer n_partos opcional
        self.fields['n_partos'].required = False
        
        # Añadir texto de ayuda
        self.fields['n_partos'].help_text = 'Dejar vacío si no aplica (machos o animales sin partos)'

class HuertosForm(forms.ModelForm):
    class Meta:
        model = Huertos
        fields = ['categoria_h', 'hectareas', 'fecha_p']
        widgets = {
            'fecha_p': forms.DateInput(attrs={'type': 'date'}),
            'hectareas': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }
        labels = {
            'categoria_h': 'Categoría de Huerto',
            'hectareas': 'Hectáreas',
            'fecha_p': 'Fecha de Plantación',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria_h'].queryset = TablaDatos.objects.filter(jerarquia=4).order_by('nombre')

class ProduccionesForm(forms.ModelForm):
    class Meta:
        model = Producciones
        fields = ['categoria_p', 'id_trabajadores', 'fecha_produccion', 'nombre', 'peso_cantidad']
        widgets = {
            'fecha_produccion': forms.DateInput(attrs={'type': 'date'}),
            'peso_cantidad': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Descripción del producto'}),
        }
        labels = {
            'categoria_p': 'Categoría de Producción',
            'id_trabajadores': 'Trabajador Responsable',
            'fecha_produccion': 'Fecha de Producción',
            'nombre': 'Nombre/Descripción',
            'peso_cantidad': 'Peso/Cantidad (kg)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria_p'].queryset = TablaDatos.objects.filter(jerarquia=5).order_by('nombre')

class ActividadesAnimalesForm(forms.ModelForm):
    class Meta:
        model = ActividadesAnimales
        fields = ['id_animales', 'id_trabajadores', 'descripcion', 'fecha', 'retorno']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe la actividad...'}),
            'retorno': forms.NumberInput(attrs={'min': '0'}),
        }
        labels = {
            'id_animales': 'Animal',
            'id_trabajadores': 'Trabajador',
            'descripcion': 'Descripción',
            'fecha': 'Fecha',
            'retorno': 'Retorno/Costo',
        }

class ActividadesHuertosForm(forms.ModelForm):
    class Meta:
        model = ActividadesHuertos
        fields = ['id_huerto', 'id_trabajadores', 'descripcion', 'fecha', 'retorno']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe la actividad...'}),
            'retorno': forms.NumberInput(attrs={'min': '0'}),
        }
        labels = {
            'id_huerto': 'Huerto',
            'id_trabajadores': 'Trabajador',
            'descripcion': 'Descripción',
            'fecha': 'Fecha',
            'retorno': 'Retorno/Costo',
        }