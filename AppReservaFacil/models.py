from django.db import models
from django.contrib.auth.models import *

# Create your models here.

MINUTOS_CHOICES=[(15,'15 Minutos'),(30,'30 Minutos'),(45,'45 Minutos'),(60,'60 Minutos')]
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
    Rut = models.CharField(max_length=9, null=True)
    Sexo = models.CharField(choices = ([('Femenino','Femenino'), ('Masculino','Masculino')]),max_length=9, null=True)
    Fecha_de_nacimiento_E = models.DateField(null=True)
    Direccion_E = models.CharField(max_length=256, null=True)
    Telefono_E = models.IntegerField(null=True)
    Foto_E = models.ImageField(null=True)
    Especialidad_P = models.ForeignKey(Especialidad,null=True, on_delete=models.RESTRICT,related_name="Especialidad_P")
    Especialidad_S = models.ForeignKey(Especialidad,null=True, on_delete=models.RESTRICT,related_name="Especialidad_S")
    Especialidad_T = models.ForeignKey(Especialidad,null=True, on_delete=models.RESTRICT,related_name="Especialidad_T")
    Especialidad_C = models.ForeignKey(Especialidad,null=True, on_delete=models.RESTRICT,related_name="Especialidad_C")
    Dia_Esp_P = models.CharField(null=True, max_length=15)
    Dia_Esp_S = models.CharField(null=True, max_length=15)
    Dia_Esp_T = models.CharField(null=True, max_length=15)
    Dia_Esp_C = models.CharField(null=True, max_length=15)
    Minutes_Esp_P = models.IntegerField(null = True, choices=MINUTOS_CHOICES)
    Minutes_Esp_S = models.IntegerField(null = True, choices=MINUTOS_CHOICES)
    Minutes_Esp_T = models.IntegerField(null = True, choices=MINUTOS_CHOICES)
    Minutes_Esp_C = models.IntegerField(null = True, choices=MINUTOS_CHOICES)
    Usuario_E = models.ForeignKey(User, null=True, on_delete=models.RESTRICT )

    def __str__(self):
        ID_Especialista = str(self.ID_Especialista)
        return f'{self.Nombre_completo_E} {ID_Especialista}'
    
class Cita(models.Model):
    ID_Cita = models.DateTimeField(primary_key=True, unique=True)
    Fecha_Cita = models.CharField(max_length=20, null=True)
    Hora_Cita = models.CharField(max_length=20, null=True)
    Confirmacion_Cita = models.BooleanField(default=False)
    ID_Cliente = models.ForeignKey(User,null=True, on_delete=models.RESTRICT)
    ID_Especialista = models.ForeignKey(Especialista,null=True, on_delete=models.RESTRICT)

    def __datetime__ (self):
        return f'{self.ID_Cita} {self.Fecha_Cita} {self.Hora_Cita}'
    
    
    