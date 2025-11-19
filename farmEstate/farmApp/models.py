from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from .validators import (
    validate_fecha_razonable_animal,
    validate_cedula_colombiana,
    validate_telefono_colombia,
    validate_sueldo_positivo,
    validate_hectareas_positivas,
    validate_peso_cantidad_positiva,
    validate_numero_partos,
    validate_retorno_economico,
    validate_fecha_no_futura
)

class TablaDatos(models.Model):
    """
    Tabla maestra para categorías, razas, géneros y otros datos de referencia.
    Estructura jerárquica para organizar datos.
    """
    nombre = models.CharField(max_length=20)
    jerarquia = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    padre = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='hijos'
    )

    def __str__(self):
        return self.nombre
    
    @property
    def tiene_hijos(self):
        """Retorna True si este dato tiene elementos dependientes"""
        return self.hijos.exists()
    
    def get_jerarquia_completa(self):
        """Retorna la jerarquía completa como string"""
        if self.padre:
            return f"{self.padre.get_jerarquia_completa()} > {self.nombre}"
        return self.nombre

    class Meta:
        verbose_name = "Dato de Referencia"
        verbose_name_plural = "Datos de Referencia"
        ordering = ['jerarquia', 'nombre']
        unique_together = ['nombre', 'jerarquia']


class Trabajadores(models.Model):
    """
    Modelo para gestionar trabajadores de la finca.
    Vinculado con el sistema de usuarios de Django.
    """
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Usuario del sistema vinculado"
    )
    nombre = models.CharField(
        max_length=50,
        verbose_name="Nombre completo"
    )
    telefono = models.CharField(
        max_length=30,
        validators=[validate_telefono_colombia],
        verbose_name="Teléfono"
    )
    cedula = models.CharField(
        max_length=20,
        unique=True,
        validators=[validate_cedula_colombiana],
        verbose_name="Cédula"
    )
    sueldo = models.FloatField(
        validators=[validate_sueldo_positivo],
        verbose_name="Sueldo mensual"
    )
    fecha_ingreso = models.DateField(
        auto_now_add=True,
        verbose_name="Fecha de ingreso"
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )

    def __str__(self):
        return f"{self.nombre} ({self.cedula})"
    
    @property
    def actividades_totales(self):
        """Retorna el total de actividades realizadas"""
        return (
            self.actividadesanimales_set.count() +
            self.actividadeshuertos_set.count()
        )
    
    def actividades_mes_actual(self):
        """Retorna el número de actividades del mes actual"""
        from datetime import datetime
        from .utils import actividades_recientes
        hoy = datetime.now()
        
        actividades_animales = self.actividadesanimales_set.filter(
            fecha__year=hoy.year,
            fecha__month=hoy.month
        ).count()
        
        actividades_huertos = self.actividadeshuertos_set.filter(
            fecha__year=hoy.year,
            fecha__month=hoy.month
        ).count()
        
        return actividades_animales + actividades_huertos
    
    def retorno_total(self):
        """Calcula el retorno económico total generado"""
        from django.db.models import Sum
        
        retorno_animales = self.actividadesanimales_set.aggregate(
            total=Sum('retorno')
        )['total'] or 0
        
        retorno_huertos = self.actividadeshuertos_set.aggregate(
            total=Sum('retorno')
        )['total'] or 0
        
        return retorno_animales + retorno_huertos
    
    def produccion_total(self):
        """Retorna la producción total registrada por este trabajador"""
        from django.db.models import Sum
        return self.producciones_set.aggregate(
            total=Sum('peso_cantidad')
        )['total'] or 0

    class Meta:
        verbose_name = "Trabajador"
        verbose_name_plural = "Trabajadores"
        ordering = ['nombre']


class Animales(models.Model):
    """
    Modelo para gestionar animales de la finca.
    Incluye información de nacimiento, raza, género y reproducción.
    """
    f_nacimiento = models.DateField(
        validators=[validate_fecha_razonable_animal],
        verbose_name="Fecha de nacimiento"
    )
    categoria_a = models.ForeignKey(
        TablaDatos,
        on_delete=models.CASCADE,
        related_name='categoria_animales',
        verbose_name="Categoría"
    )
    raza = models.ForeignKey(
        TablaDatos,
        on_delete=models.CASCADE,
        related_name='raza_animales',
        verbose_name="Raza"
    )
    genero = models.ForeignKey(
        TablaDatos,
        on_delete=models.CASCADE,
        related_name='genero_animales',
        verbose_name="Género"
    )
    n_partos = models.IntegerField(
        null=True,
        blank=True,
        validators=[validate_numero_partos],
        verbose_name="Número de partos",
        help_text="Aplicable solo para hembras"
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Marcar como inactivo si el animal ya no está en la finca"
    )
    notas = models.TextField(
        blank=True,
        null=True,
        verbose_name="Notas adicionales"
    )

    @property
    def edad(self):
        """Retorna la edad del animal en años"""
        from .utils import calcular_edad
        return calcular_edad(self.f_nacimiento)
    
    @property
    def edad_detallada(self):
        """Retorna la edad del animal en años y meses"""
        from .utils import calcular_edad_animal
        return calcular_edad_animal(self.f_nacimiento)
    
    @property
    def es_productivo(self):
        """Determina si el animal está en edad productiva (2-10 años)"""
        return 2 <= self.edad <= 10
    
    @property
    def es_hembra(self):
        """Verifica si el animal es hembra"""
        return self.genero.nombre.lower() in ['hembra', 'femenino', 'f']
    
    @property
    def puede_reproducir(self):
        """Determina si el animal puede reproducirse"""
        return self.es_productivo and self.activo
    
    def total_actividades(self):
        """Retorna el número total de actividades registradas"""
        return self.actividadesanimales_set.count()
    
    def __str__(self):
        return f"{self.categoria_a} - {self.raza} ({self.edad} años)"

    class Meta:
        verbose_name = "Animal"
        verbose_name_plural = "Animales"
        ordering = ['-f_nacimiento']


class Huertos(models.Model):
    """
    Modelo para gestionar huertos y cultivos de la finca.
    """
    categoria_h = models.ForeignKey(
        TablaDatos,
        on_delete=models.CASCADE,
        related_name='categoria_huertos',
        verbose_name="Categoría"
    )
    hectareas = models.FloatField(
        validators=[validate_hectareas_positivas],
        verbose_name="Hectáreas"
    )
    fecha_p = models.DateField(
        validators=[validate_fecha_no_futura],
        verbose_name="Fecha de plantación"
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )
    ubicacion = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Ubicación"
    )
    notas = models.TextField(
        blank=True,
        null=True,
        verbose_name="Notas adicionales"
    )

    @property
    def edad_cultivo(self):
        """Retorna la edad del cultivo en días"""
        from django.utils import timezone
        delta = timezone.now().date() - self.fecha_p
        return delta.days
    
    @property
    def meses_plantado(self):
        """Retorna los meses desde la plantación"""
        return self.edad_cultivo // 30
    
    def total_actividades(self):
        """Retorna el número total de actividades registradas"""
        return self.actividadeshuertos_set.count()
    
    def __str__(self):
        return f"{self.categoria_h} - {self.hectareas} ha"

    class Meta:
        verbose_name = "Huerto"
        verbose_name_plural = "Huertos"
        ordering = ['-fecha_p']


class Producciones(models.Model):
    """
    Modelo para registrar la producción de la finca.
    """
    categoria_p = models.ForeignKey(
        TablaDatos,
        on_delete=models.CASCADE,
        related_name='categoria_producciones',
        verbose_name="Categoría"
    )
    id_trabajadores = models.ForeignKey(
        Trabajadores,
        on_delete=models.CASCADE,
        verbose_name="Trabajador responsable"
    )
    fecha_produccion = models.DateField(
        validators=[validate_fecha_no_futura],
        verbose_name="Fecha de producción"
    )
    nombre = models.CharField(
        max_length=10,
        verbose_name="Nombre del producto"
    )
    peso_cantidad = models.FloatField(
        validators=[validate_peso_cantidad_positiva],
        verbose_name="Peso/Cantidad (kg)"
    )

    def __str__(self):
        return f"{self.nombre} - {self.peso_cantidad} kg"
    
    @property
    def valor_formateado(self):
        """Retorna el peso formateado"""
        return f"{self.peso_cantidad:,.2f} kg"

    class Meta:
        verbose_name = "Producción"
        verbose_name_plural = "Producciones"
        ordering = ['-fecha_produccion']


class ActividadesAnimales(models.Model):
    """
    Modelo para registrar actividades relacionadas con animales.
    """
    id_animales = models.ForeignKey(
        Animales,
        on_delete=models.CASCADE,
        verbose_name="Animal"
    )
    id_trabajadores = models.ForeignKey(
        Trabajadores,
        on_delete=models.CASCADE,
        verbose_name="Trabajador"
    )
    descripcion = models.CharField(
        max_length=100,
        verbose_name="Descripción"
    )
    fecha = models.DateField(
        validators=[validate_fecha_no_futura],
        verbose_name="Fecha"
    )
    retorno = models.IntegerField(
        validators=[validate_retorno_economico],
        verbose_name="Retorno económico",
        help_text="Puede ser negativo en caso de gastos"
    )

    def __str__(self):
        return f"{self.descripcion} - {self.fecha}"
    
    @property
    def es_ganancia(self):
        """Retorna True si el retorno es positivo"""
        return self.retorno > 0

    class Meta:
        verbose_name = "Actividad Animal"
        verbose_name_plural = "Actividades Animales"
        ordering = ['-fecha']


class ActividadesHuertos(models.Model):
    """
    Modelo para registrar actividades relacionadas con huertos.
    """
    id_huerto = models.ForeignKey(
        Huertos,
        on_delete=models.CASCADE,
        verbose_name="Huerto"
    )
    id_trabajadores = models.ForeignKey(
        Trabajadores,
        on_delete=models.CASCADE,
        verbose_name="Trabajador"
    )
    descripcion = models.CharField(
        max_length=100,
        verbose_name="Descripción"
    )
    fecha = models.DateField(
        validators=[validate_fecha_no_futura],
        verbose_name="Fecha"
    )
    retorno = models.IntegerField(
        validators=[validate_retorno_economico],
        verbose_name="Retorno económico",
        help_text="Puede ser negativo en caso de gastos"
    )

    def __str__(self):
        return f"{self.descripcion} - {self.fecha}"
    
    @property
    def es_ganancia(self):
        """Retorna True si el retorno es positivo"""
        return self.retorno > 0

    class Meta:
        verbose_name = "Actividad Huerto"
        verbose_name_plural = "Actividades Huertos"
        ordering = ['-fecha']
        