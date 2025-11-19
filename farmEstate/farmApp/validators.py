"""
Validadores personalizados para el proyecto FarmEstate
"""
from django.core.exceptions import ValidationError
from django.utils import timezone
import re


def validate_fecha_no_futura(value):
    """
    Valida que la fecha no sea futura.
    Útil para fechas de nacimiento y fechas de eventos pasados.
    """
    if value > timezone.now().date():
        raise ValidationError(
            'La fecha no puede ser futura',
            code='fecha_futura'
        )


def validate_fecha_razonable_animal(value):
    """
    Valida que la fecha de nacimiento de un animal sea razonable.
    No debe ser mayor a 30 años en el pasado.
    """
    hoy = timezone.now().date()
    edad_maxima_dias = 30 * 365  # 30 años
    
    if (hoy - value).days > edad_maxima_dias:
        raise ValidationError(
            'La fecha de nacimiento es demasiado antigua (más de 30 años)',
            code='fecha_muy_antigua'
        )
    
    if value > hoy:
        raise ValidationError(
            'La fecha de nacimiento no puede ser futura',
            code='fecha_futura'
        )


def validate_cedula_colombiana(value):
    """
    Valida el formato de una cédula de ciudadanía colombiana.
    Debe contener entre 6 y 10 dígitos numéricos.
    """
    # Remover espacios y guiones
    cedula_limpia = value.replace(' ', '').replace('-', '')
    
    if not cedula_limpia.isdigit():
        raise ValidationError(
            'La cédula solo debe contener números',
            code='cedula_no_numerica'
        )
    
    if len(cedula_limpia) < 6 or len(cedula_limpia) > 10:
        raise ValidationError(
            'La cédula debe tener entre 6 y 10 dígitos',
            code='cedula_longitud_invalida'
        )


def validate_telefono_colombia(value):
    """
    Valida el formato de un número de teléfono colombiano.
    Acepta formatos:
    - 3001234567
    - 300 123 4567
    - +57 300 1234567
    - +573001234567
    """
    # Remover espacios y guiones
    telefono_limpio = value.replace(' ', '').replace('-', '')
    
    # Patrón para teléfono colombiano
    # Acepta: 10 dígitos o +57 seguido de 10 dígitos
    patron = r'^(\+57)?[0-9]{10}$'
    
    if not re.match(patron, telefono_limpio):
        raise ValidationError(
            'Formato de teléfono inválido. Use formato: 3001234567 o +573001234567',
            code='telefono_formato_invalido'
        )
    
    # Validar que el número móvil empiece con 3 (después del código de país)
    if telefono_limpio.startswith('+57'):
        numero = telefono_limpio[3:]
    else:
        numero = telefono_limpio
    
    if not numero.startswith('3'):
        raise ValidationError(
            'Los números móviles en Colombia deben empezar con 3',
            code='telefono_no_movil'
        )


def validate_sueldo_positivo(value):
    """
    Valida que el sueldo sea un valor positivo y razonable.
    """
    if value <= 0:
        raise ValidationError(
            'El sueldo debe ser un valor positivo',
            code='sueldo_no_positivo'
        )
    
    # Validar contra el salario mínimo colombiano 2025 (aproximado)
    salario_minimo = 1300000
    
    if value < salario_minimo * 0.5:
        raise ValidationError(
            f'El sueldo parece demasiado bajo. Debe ser al menos ${salario_minimo * 0.5:,.0f}',
            code='sueldo_muy_bajo'
        )
    
    if value > 100000000:  # 100 millones
        raise ValidationError(
            'El sueldo parece demasiado alto. Verifique el valor',
            code='sueldo_muy_alto'
        )


def validate_hectareas_positivas(value):
    """
    Valida que las hectáreas sean un valor positivo.
    """
    if value <= 0:
        raise ValidationError(
            'Las hectáreas deben ser un valor positivo',
            code='hectareas_no_positivas'
        )
    
    if value > 10000:  # 10,000 hectáreas
        raise ValidationError(
            'El valor de hectáreas parece demasiado grande. Verifique el dato',
            code='hectareas_excesivas'
        )


def validate_peso_cantidad_positiva(value):
    """
    Valida que el peso o cantidad sea positivo.
    """
    if value <= 0:
        raise ValidationError(
            'El peso o cantidad debe ser un valor positivo',
            code='peso_no_positivo'
        )
    
    if value > 100000:  # 100 toneladas
        raise ValidationError(
            'El peso o cantidad parece demasiado grande. Verifique el dato',
            code='peso_excesivo'
        )


def validate_numero_partos(value):
    """
    Valida que el número de partos sea razonable.
    """
    if value < 0:
        raise ValidationError(
            'El número de partos no puede ser negativo',
            code='partos_negativo'
        )
    
    if value > 15:
        raise ValidationError(
            'El número de partos parece demasiado alto (máximo razonable: 15)',
            code='partos_excesivo'
        )


def validate_retorno_economico(value):
    """
    Valida que el retorno económico esté en un rango razonable.
    Puede ser negativo (pérdida) pero no excesivamente grande.
    """
    if value < -50000000:  # -50 millones
        raise ValidationError(
            'El retorno negativo parece demasiado grande. Verifique el dato',
            code='perdida_excesiva'
        )
    
    if value > 100000000:  # 100 millones
        raise ValidationError(
            'El retorno parece demasiado grande. Verifique el dato',
            code='ganancia_excesiva'
        )
    