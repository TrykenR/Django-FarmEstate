from django.shortcuts import render, redirect
from .models import Trabajadores, Animales, Huertos, Producciones
from .forms import TrabajadoresForm, AnimalesForm, HuertosForm, ProduccionesForm

def home(request):
    return render(request, 'farmApp/home.html')

# --- CRUD básico de Trabajadores ---
def listar_trabajadores(request):
    trabajadores = Trabajadores.objects.all()
    return render(request, 'farmApp/trabajadores_list.html', {'trabajadores': trabajadores})

def crear_trabajador(request):
    if request.method == 'POST':
        form = TrabajadoresForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_trabajadores')
    else:
        form = TrabajadoresForm()
    return render(request, 'farmApp/trabajador_form.html', {'form': form})

# --- Ejemplo similar para Animales ---
def listar_animales(request):
    animales = Animales.objects.all()
    return render(request, 'farmApp/animales_list.html', {'animales': animales})

def crear_animal(request):
    if request.method == 'POST':
        form = AnimalesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_animales')
    else:
        form = AnimalesForm()
    return render(request, 'farmApp/animal_form.html', {'form': form})
