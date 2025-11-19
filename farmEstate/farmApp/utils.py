"""
Funciones utilitarias para el proyecto FarmEstate
"""
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from datetime import datetime, timedelta


def calcular_edad(fecha_nacimiento):
    """
    Calcula la edad en años a partir de una fecha de nacimiento.
    
    Args:
        fecha_nacimiento (date): Fecha de nacimiento
        
    Returns:
        int: Edad en años
    """
    hoy = timezone.now().date()
    edad = hoy.year - fecha_nacimiento.year
    
    # Ajustar si aún no ha cumplido años este año
    if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
        edad -= 1
    
    return edad


def calcular_edad_animal(fecha_nacimiento):
    """
    Calcula la edad de un animal en años y meses.
    
    Args:
        fecha_nacimiento (date): Fecha de nacimiento del animal
        
    Returns:
        dict: {'años': int, 'meses': int, 'total_meses': int}
    """
    hoy = timezone.now().date()
    
    años = hoy.year - fecha_nacimiento.year
    meses = hoy.month - fecha_nacimiento.month
    
    if meses < 0:
        años -= 1
        meses += 12
    
    total_meses = años * 12 + meses
    
    return {
        'años': años,
        'meses': meses,
        'total_meses': total_meses
    }


def obtener_produccion_periodo(fecha_inicio, fecha_fin, categoria=None):
    """
    Obtiene la producción total de un período.
    
    Args:
        fecha_inicio (date): Fecha inicial
        fecha_fin (date): Fecha final
        categoria (TablaDatos, optional): Filtrar por categoría
        
    Returns:
        float: Producción total en kg
    """
    from .models import Producciones
    
    query = Producciones.objects.filter(
        fecha_produccion__range=[fecha_inicio, fecha_fin]
    )
    
    if categoria:
        query = query.filter(categoria_p=categoria)
    
    resultado = query.aggregate(total=Sum('peso_cantidad'))
    return resultado['total'] or 0


def obtener_produccion_mes_actual():
    """
    Obtiene la producción del mes actual.
    
    Returns:
        float: Producción del mes en kg
    """
    hoy = timezone.now().date()
    primer_dia = hoy.replace(day=1)
    
    return obtener_produccion_periodo(primer_dia, hoy)


def obtener_produccion_hoy():
    """
    Obtiene la producción del día actual.
    
    Returns:
        float: Producción de hoy en kg
    """
    hoy = timezone.now().date()
    return obtener_produccion_periodo(hoy, hoy)


def estadisticas_generales():
    """
    Obtiene estadísticas generales de la finca.
    
    Returns:
        dict: Diccionario con estadísticas
    """
    from .models import Animales, Trabajadores, Huertos, Producciones
    
    # Conteos básicos
    total_animales = Animales.objects.count()
    total_trabajadores = Trabajadores.objects.count()
    total_huertos = Huertos.objects.count()
    
    # Hectáreas totales
    hectareas_totales = Huertos.objects.aggregate(
        total=Sum('hectareas')
    )['total'] or 0
    
    # Producción del mes
    produccion_mes = obtener_produccion_mes_actual()
    
    # Producción de hoy
    produccion_hoy = obtener_produccion_hoy()
    
    # Animales por categoría
    animales_por_categoria = Animales.objects.values(
        'categoria_a__nombre'
    ).annotate(
        cantidad=Count('id')
    ).order_by('-cantidad')
    
    # Promedio de edad de animales
    edades = []
    for animal in Animales.objects.all():
        edad = calcular_edad(animal.f_nacimiento)
        edades.append(edad)
    
    edad_promedio = sum(edades) / len(edades) if edades else 0
    
    return {
        'total_animales': total_animales,
        'total_trabajadores': total_trabajadores,
        'total_huertos': total_huertos,
        'hectareas_totales': round(hectareas_totales, 2),
        'produccion_mes': round(produccion_mes, 2),
        'produccion_hoy': round(produccion_hoy, 2),
        'animales_por_categoria': list(animales_por_categoria),
        'edad_promedio_animales': round(edad_promedio, 1)
    }


def actividades_recientes(trabajador=None, limite=10):
    """
    Obtiene las actividades más recientes.
    
    Args:
        trabajador (Trabajadores, optional): Filtrar por trabajador
        limite (int): Número máximo de actividades a retornar
        
    Returns:
        list: Lista de actividades combinadas
    """
    from .models import ActividadesAnimales, ActividadesHuertos
    
    # Actividades de animales
    query_animales = ActividadesAnimales.objects.select_related(
        'id_trabajadores', 'id_animales'
    )
    
    # Actividades de huertos
    query_huertos = ActividadesHuertos.objects.select_related(
        'id_trabajadores', 'id_huerto'
    )
    
    # Filtrar por trabajador si se especifica
    if trabajador:
        query_animales = query_animales.filter(id_trabajadores=trabajador)
        query_huertos = query_huertos.filter(id_trabajadores=trabajador)
    
    # Obtener y combinar
    actividades_animales = list(query_animales.order_by('-fecha')[:limite])
    actividades_huertos = list(query_huertos.order_by('-fecha')[:limite])
    
    # Combinar y ordenar por fecha
    todas_actividades = actividades_animales + actividades_huertos
    todas_actividades.sort(key=lambda x: x.fecha, reverse=True)
    
    return todas_actividades[:limite]


def calcular_retorno_trabajador(trabajador, fecha_inicio=None, fecha_fin=None):
    """
    Calcula el retorno económico generado por un trabajador.
    
    Args:
        trabajador (Trabajadores): El trabajador
        fecha_inicio (date, optional): Fecha inicial del período
        fecha_fin (date, optional): Fecha final del período
        
    Returns:
        dict: {'total': float, 'animales': float, 'huertos': float}
    """
    from .models import ActividadesAnimales, ActividadesHuertos
    
    # Si no se especifican fechas, usar el mes actual
    if not fecha_inicio or not fecha_fin:
        hoy = timezone.now().date()
        fecha_inicio = hoy.replace(day=1)
        fecha_fin = hoy
    
    # Retorno de actividades con animales
    retorno_animales = ActividadesAnimales.objects.filter(
        id_trabajadores=trabajador,
        fecha__range=[fecha_inicio, fecha_fin]
    ).aggregate(total=Sum('retorno'))['total'] or 0
    
    # Retorno de actividades con huertos
    retorno_huertos = ActividadesHuertos.objects.filter(
        id_trabajadores=trabajador,
        fecha__range=[fecha_inicio, fecha_fin]
    ).aggregate(total=Sum('retorno'))['total'] or 0
    
    return {
        'total': retorno_animales + retorno_huertos,
        'animales': retorno_animales,
        'huertos': retorno_huertos
    }


def obtener_animales_productivos():
    """
    Obtiene los animales en edad productiva (entre 2 y 10 años).
    
    Returns:
        QuerySet: Animales productivos
    """
    from .models import Animales
    
    hoy = timezone.now().date()
    fecha_max = hoy.replace(year=hoy.year - 2)  # 2 años
    fecha_min = hoy.replace(year=hoy.year - 10)  # 10 años
    
    return Animales.objects.filter(
        f_nacimiento__range=[fecha_min, fecha_max]
    )


def obtener_huertos_activos():
    """
    Obtiene los huertos plantados en los últimos 2 años.
    
    Returns:
        QuerySet: Huertos activos
    """
    from .models import Huertos
    
    hace_dos_años = timezone.now().date() - timedelta(days=730)
    
    return Huertos.objects.filter(
        fecha_p__gte=hace_dos_años
    )


def formatear_moneda(valor):
    """
    Formatea un valor como moneda colombiana (COP).
    
    Args:
        valor (float): Valor a formatear
        
    Returns:
        str: Valor formateado como $1,234,567
    """
    return f"${valor:,.0f}".replace(",", ".")


def formatear_peso(valor):
    """
    Formatea un valor de peso en kg.
    
    Args:
        valor (float): Peso en kg
        
    Returns:
        str: Valor formateado como "123.45 kg"
    """
    return f"{valor:,.2f} kg"


def validar_permisos_trabajador(usuario, nivel_requerido='trabajador'):
    """
    Valida si un usuario tiene los permisos necesarios.
    
    Args:
        usuario (User): Usuario a validar
        nivel_requerido (str): Nivel requerido ('trabajador', 'supervisor', 'admin')
        
    Returns:
        bool: True si tiene permisos, False en caso contrario
    """
    try:
        trabajador = usuario.trabajadores
        
        niveles = {
            'trabajador': 1,
            'supervisor': 2,
            'admin': 3
        }
        
        # Por ahora, todos los trabajadores tienen acceso
        # En el futuro, implementar sistema de roles
        return True
        
    except:
        return False


def resumen_finca():
    """
    Genera un resumen completo de la finca para el dashboard.
    
    Returns:
        dict: Resumen completo con todas las estadísticas
    """
    stats = estadisticas_generales()
    
    return {
        **stats,
        'animales_productivos': obtener_animales_productivos().count(),
        'huertos_activos': obtener_huertos_activos().count(),
    }
