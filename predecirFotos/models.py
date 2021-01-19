from django.db import models

# Create your models here.

class Clientes(models.Model):
    nombre=models.CharField(max_length=30)
    direccion=models.CharField(max_length=50)
    email=models.EmailField(blank=True, null=True)
    telefono=models.CharField(max_length=8)

class Equipos(models.Model):
    nombre=models.CharField(max_length=30)
    descripción=models.CharField(max_length=50)

class Articulos(models.Model):
    nombre=models.CharField(max_length=30)
    seccion=models.CharField(max_length=20)
    precio=models.IntegerField()


class ImagenesBuscadas(models.Model):
    fecha=models.DateTimeField(null=True)
    imagen = models.ImageField(null=True, blank=True)

class Book(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()

class EquiposPuertoColoso(models.Model):
    nombre = models.CharField(max_length=50)
    bomba_funcionando = models.IntegerField()
    presion_agua_sello = models.IntegerField()
    flujo_agua_sello =  models.IntegerField()
    velocidad = models.IntegerField()
    flujo_transmisor = models.IntegerField()
    densimetro_nuclear = models.IntegerField()




# MODELO OFICIAL 
class EQUIPOSCOLOSO(models.Model):
    Codigo_e = models.AutoField(primary_key=True)
    Nombre_equipo = models.CharField(max_length=500)
    Descripcion = models.CharField(max_length=1000)
    Tipo_equipo = models.CharField(max_length=500)

    def __str__(self):
        return self.Nombre_equipo


# DATOS EXCEL
class Sensores_excel(models.Model):
    Fecha = models.DateTimeField(primary_key=True, blank=True, default=None)
    Equipo1 = models.ForeignKey(EQUIPOSCOLOSO, on_delete= models.SET_NULL,
                                    null=True, blank=False)
    Funcionando = models.IntegerField()
    Presion_agua_sello = models.FloatField()
    Flujo_agua_sello = models.FloatField()
    Velocidad = models.FloatField()
    Flujo_transmisor = models.FloatField()
    Densimetro_nuclear = models.FloatField()
    Temperatura = models.FloatField()
    Aceleracion = models.FloatField()
    Velocidad_vibracion = models.FloatField()

class FALLAS(models.Model):
    Codigo_f = models.AutoField(primary_key=True)
    Nombre_falla = models.CharField(max_length=500)

    def __str__(self):
        return self.Nombre_falla

class SENSORES(models.Model):
    Fecha = models.DateTimeField(primary_key=True, blank=True, default=None)
    Equipo = models.ForeignKey(EQUIPOSCOLOSO, on_delete=models.CASCADE,
                                    null=False, blank=False)
    Falla = models.ManyToManyField(FALLAS, through='SENSORESFALLAS')
    Presion_agua_sello = models.FloatField()
    Flujo_agua_sello = models.FloatField()
    Velocidad = models.FloatField()
    Flujo_transmisor = models.FloatField()
    Densimetro_nuclear = models.FloatField()
    Temperatura = models.FloatField()
    Aceleracion = models.FloatField()
    Velocidad_vibracion = models.FloatField()
    Ingreso = models.CharField(max_length=10)

    def __str__(self):
        return self.Equipo.Nombre_equipo

class SENSORESFALLAS(models.Model):
    Sensores = models.ForeignKey(SENSORES, on_delete=models.CASCADE)
    Fallas = models.ForeignKey(FALLAS, on_delete=models.CASCADE)
    Porc_falla = models.FloatField()

    def __str__(self):
        return self.Fallas.Nombre_falla

