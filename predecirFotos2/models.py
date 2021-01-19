from django.db import models

# Create your models here.
class Personajes(models.Model):
    nombre = models.CharField(max_length=128)
    nombre_real = models.CharField(max_length=128)
    imagen = models.ImageField()
    descripcion = models.TextField()