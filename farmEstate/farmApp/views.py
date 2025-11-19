from django.shortcuts import render, redirect, get_object_or_404
from .models import Trabajadores, Animales, Huertos, Producciones, ActividadesAnimales, ActividadesHuertos
from .forms import TrabajadoresForm, AnimalesForm, HuertosForm, ProduccionesForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# ========================================
# VISTAS PÚBLICAS (sin autenticación)
# ========================================

def home(request):
    """Página de inicio - Accesible para todos"""
    return render(request, 'farmApp/home.html')


def login_trabajador(request):
    """Vista de login - Accesible para todos"""
    # Si ya está autenticado, redirigir al dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            # Vinculamos trabajador
            trabajador = Trabajadores.objects.filter(usuario=user).first()
            request.session["trabajador_id"] = trabajador.id if trabajador else None

            messages.success(request, f'¡Bienvenido {user.username}!')
            return redirect("dashboard")
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
            return render(request, "farmApp/login.html", {
                "error": "Usuario o contraseña incorrectos"
            })

    return render(request, "farmApp/login.html")


# ========================================
# VISTAS PROTEGIDAS - DASHBOARD
# ========================================

@login_required(login_url='login')
def dashboard(request):
    """Dashboard principal - Requiere autenticación"""
    trabajador = Trabajadores.objects.filter(usuario=request.user).first()
    
    # Si el usuario no tiene trabajador asociado
    if not trabajador:
        messages.warning(request, 'Tu usuario no está asociado a un trabajador. Contacta al administrador.')
        logout(request)
        return redirect('login')
    
    total_animales = Animales.objects.filter(activo=True).count()
    total_huertos = Huertos.objects.filter(activo=True).count()
    total_trabajadores = Trabajadores.objects.filter(activo=True).count()
    
    # Usar las funciones de utils
    from .utils import obtener_produccion_hoy, actividades_recientes
    produccion_hoy = obtener_produccion_hoy()
    actividades = actividades_recientes(trabajador=trabajador, limite=5)

    context = {
        "trabajador": trabajador,
        "total_animales": total_animales,
        "total_huertos": total_huertos,
        "total_trabajadores": total_trabajadores,
        "produccion_hoy": produccion_hoy,
        "actividades": actividades,
    }
    return render(request, "farmApp/dashboard.html", context)


@login_required(login_url='login')
def salir(request):
    """Cerrar sesión"""
    messages.info(request, 'Has cerrado sesión exitosamente')
    logout(request)
    return redirect("login")


# ========================================
# VISTAS PROTEGIDAS - TRABAJADORES
# ========================================

@login_required(login_url='login')
def listar_trabajadores(request):
    """Listar trabajadores - Requiere autenticación"""
    trabajadores = Trabajadores.objects.filter(activo=True).order_by('nombre')
    return render(request, 'farmApp/trabajadores_list.html', {
        'trabajadores': trabajadores
    })


@login_required(login_url='login')
def crear_trabajador(request):
    """Crear trabajador - Requiere autenticación"""
    if request.method == 'POST':
        form = TrabajadoresForm(request.POST)
        if form.is_valid():
            trabajador = form.save()
            messages.success(request, f'✅ Trabajador {trabajador.nombre} registrado exitosamente')
            return redirect('listar_trabajadores')
        else:
            messages.error(request, '❌ Por favor corrige los errores en el formulario')
    else:
        form = TrabajadoresForm()
    
    return render(request, 'farmApp/trabajador_form.html', {
        'form': form,
        'titulo': 'Registrar Trabajador'
    })


@login_required(login_url='login')
def editar_trabajador(request, pk):
    """Editar trabajador - Requiere autenticación"""
    trabajador = get_object_or_404(Trabajadores, pk=pk)
    
    if request.method == 'POST':
        form = TrabajadoresForm(request.POST, instance=trabajador)
        if form.is_valid():
            form.save()
            messages.success(request, f'✅ Trabajador {trabajador.nombre} actualizado exitosamente')
            return redirect('listar_trabajadores')
        else:
            messages.error(request, '❌ Por favor corrige los errores en el formulario')
    else:
        form = TrabajadoresForm(instance=trabajador)
    
    return render(request, 'farmApp/trabajador_form.html', {
        'form': form,
        'titulo': f'Editar: {trabajador.nombre}',
        'editando': True
    })


@login_required(login_url='login')
def eliminar_trabajador(request, pk):
    """Eliminar trabajador (desactivar) - Requiere autenticación"""
    trabajador = get_object_or_404(Trabajadores, pk=pk)
    
    if request.method == 'POST':
        # No eliminamos realmente, solo desactivamos
        trabajador.activo = False
        trabajador.save()
        messages.warning(request, f'🗑️ Trabajador {trabajador.nombre} desactivado')
        return redirect('listar_trabajadores')
    
    return render(request, 'farmApp/confirmar_eliminar.html', {
        'objeto': trabajador,
        'tipo': 'trabajador',
        'url_cancelar': 'listar_trabajadores'
    })


# ========================================
# VISTAS PROTEGIDAS - ANIMALES
# ========================================

@login_required(login_url='login')
def listar_animales(request):
    """Listar animales - Requiere autenticación"""
    animales = Animales.objects.filter(activo=True).select_related(
        'categoria_a', 'raza', 'genero'
    ).order_by('-f_nacimiento')
    
    return render(request, 'farmApp/animales_list.html', {
        'animales': animales
    })


@login_required(login_url='login')
def crear_animal(request):
    """Crear animal - Requiere autenticación"""
    if request.method == 'POST':
        form = AnimalesForm(request.POST)
        if form.is_valid():
            animal = form.save()
            messages.success(request, f'✅ Animal registrado exitosamente')
            return redirect('listar_animales')
        else:
            messages.error(request, '❌ Por favor corrige los errores en el formulario')
    else:
        form = AnimalesForm()
    
    return render(request, 'farmApp/animal_form.html', {
        'form': form,
        'titulo': 'Registrar Animal'
    })


@login_required(login_url='login')
def editar_animal(request, pk):
    """Editar animal - Requiere autenticación"""
    animal = get_object_or_404(Animales, pk=pk)
    
    if request.method == 'POST':
        form = AnimalesForm(request.POST, instance=animal)
        if form.is_valid():
            form.save()
            messages.success(request, f'✅ Animal actualizado exitosamente')
            return redirect('listar_animales')
        else:
            messages.error(request, '❌ Por favor corrige los errores en el formulario')
    else:
        form = AnimalesForm(instance=animal)
    
    return render(request, 'farmApp/animal_form.html', {
        'form': form,
        'titulo': 'Editar Animal',
        'editando': True
    })


@login_required(login_url='login')
def eliminar_animal(request, pk):
    """Eliminar animal (desactivar) - Requiere autenticación"""
    animal = get_object_or_404(Animales, pk=pk)
    
    if request.method == 'POST':
        # No eliminamos realmente, solo desactivamos
        animal.activo = False
        animal.save()
        messages.warning(request, f'🗑️ Animal desactivado')
        return redirect('listar_animales')
    
    return render(request, 'farmApp/confirmar_eliminar.html', {
        'objeto': animal,
        'tipo': 'animal',
        'url_cancelar': 'listar_animales'
    })


# ========================================
# VISTAS PROTEGIDAS - HUERTOS
# ========================================

@login_required(login_url='login')
def listar_huertos(request):
    """Listar huertos - Requiere autenticación"""
    huertos = Huertos.objects.filter(activo=True).select_related(
        'categoria_h'
    ).order_by('-fecha_p')
    
    return render(request, 'farmApp/huertos_list.html', {
        'huertos': huertos
    })


@login_required(login_url='login')
def crear_huerto(request):
    """Crear huerto - Requiere autenticación"""
    if request.method == 'POST':
        form = HuertosForm(request.POST)
        if form.is_valid():
            huerto = form.save()
            messages.success(request, f'✅ Huerto registrado exitosamente')
            return redirect('listar_huertos')
        else:
            messages.error(request, '❌ Por favor corrige los errores en el formulario')
    else:
        form = HuertosForm()
    
    return render(request, 'farmApp/huerto_form.html', {
        'form': form,
        'titulo': 'Registrar Huerto'
    })


@login_required(login_url='login')
def editar_huerto(request, pk):
    """Editar huerto - Requiere autenticación"""
    huerto = get_object_or_404(Huertos, pk=pk)
    
    if request.method == 'POST':
        form = HuertosForm(request.POST, instance=huerto)
        if form.is_valid():
            form.save()
            messages.success(request, f'✅ Huerto actualizado exitosamente')
            return redirect('listar_huertos')
        else:
            messages.error(request, '❌ Por favor corrige los errores en el formulario')
    else:
        form = HuertosForm(instance=huerto)
    
    return render(request, 'farmApp/huerto_form.html', {
        'form': form,
        'titulo': 'Editar Huerto',
        'editando': True
    })


@login_required(login_url='login')
def eliminar_huerto(request, pk):
    """Eliminar huerto (desactivar) - Requiere autenticación"""
    huerto = get_object_or_404(Huertos, pk=pk)
    
    if request.method == 'POST':
        # No eliminamos realmente, solo desactivamos
        huerto.activo = False
        huerto.save()
        messages.warning(request, f'🗑️ Huerto desactivado')
        return redirect('listar_huertos')
    
    return render(request, 'farmApp/confirmar_eliminar.html', {
        'objeto': huerto,
        'tipo': 'huerto',
        'url_cancelar': 'listar_huertos'
    })


# ========================================
# VISTAS PROTEGIDAS - PRODUCCIONES
# ========================================

@login_required(login_url='login')
def listar_producciones(request):
    """Listar producciones - Requiere autenticación"""
    producciones = Producciones.objects.select_related(
        'categoria_p', 'id_trabajadores'
    ).order_by('-fecha_produccion')
    
    return render(request, 'farmApp/producciones_list.html', {
        'producciones': producciones
    })


@login_required(login_url='login')
def crear_produccion(request):
    """Crear producción - Requiere autenticación"""
    if request.method == 'POST':
        form = ProduccionesForm(request.POST)
        if form.is_valid():
            produccion = form.save()
            messages.success(request, f'✅ Producción registrada exitosamente')
            return redirect('listar_producciones')
        else:
            messages.error(request, '❌ Por favor corrige los errores en el formulario')
    else:
        form = ProduccionesForm()
    
    return render(request, 'farmApp/produccion_form.html', {
        'form': form,
        'titulo': 'Registrar Producción'
    })
