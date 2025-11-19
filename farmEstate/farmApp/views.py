from django.shortcuts import render, redirect
from .models import Trabajadores, Animales, Huertos, Producciones, ActividadesAnimales, ActividadesHuertos
from .forms import TrabajadoresForm, AnimalesForm, HuertosForm, ProduccionesForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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

def login_trabajador(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            # Vinculamos trabajador
            trabajador = Trabajadores.objects.filter(usuario=user).first()

            request.session["trabajador_id"] = trabajador.id if trabajador else None

            return redirect("dashboard")

        else:
            return render(request, "farmApp/login.html", {
                "error": "Usuario o contraseña incorrectos"
            })

    return render(request, "farmApp/login.html")

@login_required
def dashboard(request):
    trabajador = Trabajadores.objects.filter(usuario=request.user).first()
    total_animales = Animales.objects.count()
    total_huertos = Huertos.objects.count()
    total_trabajadores = Trabajadores.objects.count()
    produccion_hoy = 0  # placeholder
    actividades = ActividadesAnimales.objects.filter(
        id_trabajadores=trabajador
    ).order_by('-fecha')[:5]

    context = {
        "trabajador": trabajador,
        "total_animales": total_animales,
        "total_huertos": total_huertos,
        "total_trabajadores": total_trabajadores,
        "produccion_hoy": produccion_hoy,
        "actividades": actividades,
    }
    return render(request, "farmApp/dashboard.html", context)

def salir(request):
    logout(request)
    return redirect("login")
