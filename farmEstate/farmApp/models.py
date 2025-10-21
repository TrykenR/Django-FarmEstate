from django.db import models

from django.db import models


class TablaDatos(models.Model):
    nombre = models.CharField(max_length=20)
    jerarquia = models.IntegerField()
    padre = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nombre


class Trabajadores(models.Model):
    nombre = models.CharField(max_length=50)
    telefono = models.CharField(max_length=30)
    cedula = models.CharField(max_length=20)
    sueldo = models.FloatField()

    def __str__(self):
        return self.nombre


class Animales(models.Model):
    f_nacimiento = models.DateField()
    categoria_a = models.ForeignKey(TablaDatos, on_delete=models.CASCADE, related_name='categoria_animales')
    raza = models.ForeignKey(TablaDatos, on_delete=models.CASCADE, related_name='raza_animales')
    genero = models.ForeignKey(TablaDatos, on_delete=models.CASCADE, related_name='genero_animales')
    n_partos = models.IntegerField()

    def __str__(self):
        return f"Animal {self.id}"


class Huertos(models.Model):
    categoria_h = models.ForeignKey(TablaDatos, on_delete=models.CASCADE, related_name='categoria_huertos')
    hectareas = models.FloatField()
    fecha_p = models.DateField()

    def __str__(self):
        return f"Huerto {self.id}"


class Producciones(models.Model):
    categoria_p = models.ForeignKey(TablaDatos, on_delete=models.CASCADE, related_name='categoria_producciones')
    id_trabajadores = models.ForeignKey(Trabajadores, on_delete=models.CASCADE)
    fecha_produccion = models.DateField()
    nombre = models.CharField(max_length=10)
    peso_cantidad = models.FloatField()

    def __str__(self):
        return self.nombre


class ActividadesAnimales(models.Model):
    id_animales = models.ForeignKey(Animales, on_delete=models.CASCADE)
    id_trabajadores = models.ForeignKey(Trabajadores, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=100)
    fecha = models.DateField()
    retorno = models.IntegerField()

    def __str__(self):
        return f"Actividad Animal {self.id}"


class ActividadesHuertos(models.Model):
    id_huerto = models.ForeignKey(Huertos, on_delete=models.CASCADE)
    id_trabajadores = models.ForeignKey(Trabajadores, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=100)
    fecha = models.DateField()
    retorno = models.IntegerField()

    def __str__(self):
        return f"Actividad Huerto {self.id}"
