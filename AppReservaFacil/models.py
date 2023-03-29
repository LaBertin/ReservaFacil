from django.db import models
from django.contrib.auth.models import *

# Create your models here.

class Area_Medica(models.Model):
    ID_Area_Medica = models.IntegerField(primary_key=True, unique=True)
    Nombre_Area_Medica = models.CharField(max_length=256)

    def __str__(self):
        return self.Nombre_Area_Medica
    
    class Meta:
        verbose_name='Área Médica'
        verbose_name_plural='Áreas Médicas'

class Especialidad(models.Model):
    Codigo_especialidad = models.IntegerField(primary_key=True, unique=True)
    Nombre_especialidad = models.CharField(max_length=256)
    Icono_especialidad = models.ImageField()
    Color_especialidad = models.CharField(max_length=64)
    Area_Medica_F = models.ForeignKey(Area_Medica,null=True, on_delete=models.RESTRICT)

    def __str__(self):
        return self.Nombre_especialidad
    
    class Meta:
        verbose_name='Especialidad'
        verbose_name_plural='Especialidades'

class Especialista(models.Model):
    ID_Especialista = models.IntegerField(primary_key=True, unique=True)
    Nombre_completo_E = models.CharField(max_length=256)
    Fecha_de_nacimiento_E = models.DateField()
    Direccion_E = models.CharField(max_length=256)
    Telefono_E = models.IntegerField()
    Foto_E = models.ImageField()
    Especialidad_P = models.ForeignKey(Especialidad,null=True, on_delete=models.RESTRICT)

    def __str__(self):
        ID_Especialista = str(self.ID_Especialista)
        return f'{self.Nombre_completo_E} {ID_Especialista}'
    
class Cita(models.Model):
    ID_Cita = models.DateTimeField(primary_key=True, unique=True)
    ID_Cliente = models.ForeignKey(User,null=True, on_delete=models.RESTRICT)
    ID_Especialista = models.ForeignKey(Especialista,null=True, on_delete=models.RESTRICT)

    def __datetime__ (self):
        return self.ID_Cita
    