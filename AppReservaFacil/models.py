from django.db import models
from django import forms
from django.contrib.auth.models import *
import os
from django.conf import settings
 
from multiselectfield import MultiSelectField

# Create your models here.

DIAS_CHOICES=[('lun','Lunes'),('mar','Martes'),('mie','Miercoles'),('jue','Jueves'),('vie','Viernes'),('sab','Sabado'),('dom','Domingo')]
MINUTOS_CHOICES=[(15,'15 Minutos'),(30,'30 Minutos'),(45,'45 Minutos'),(60,'60 Minutos')]
SEXO_CHOICES=[('Femenino','Femenino'), ('Masculino','Masculino')]
SISTEMA_SALUD=[('Ninguno','Ninguno'),('Seguro Complementario','Seguro Complementario'), ('ISAPRE','ISAPRE'), ('FONASA','FONASA'),('Fuerzas Armadas','Fuerzas Armadas')]
GRUPO_SANGUINEO=[('Ninguno','Ninguno'),('A+','A+'),('O+','O+'),('B+','B+'),('AB+','AB+'),('A-','A-'),('O-','O-'),('B-','B-'),('AB-','AB-')]
ESTADO_COBRO = [('Pagado','Pagado'),('Por pagar','Por pagar')]
METODO_PAGO = [('Efectivo','Efectivo'),('Debito','Debito'),('Credito','Credito')]
TIPO_ATENCION = [('Particular','Particular'),('Fonasa','Fonasa'),('Isapre','Isapre'),('Convenio','Convenio'),('Otros','Otros')]
EXAMENES=[('Glucosa','Glucosa'),('Nitrogeno_Ureico','Nitrogeno Ureico'),('Urea','Urea'),('Colesterol_total','Colesterol Total'),('Acido_Urico','Acido Urico'),('Proteinas_totales','Proteinas Totales')
          ,('Albuminca','Albúminca'),('Globulinas','Globulinas'),('Bilirrubina_total','Bilirrubina total'),('Transaminasa_GOT','Transaminasa GOT'),('Transaminada_GPT','Transaminada GPT'),
          ('Gammaglutamil_transferasa',' Gammaglutamil transferasa'),('Deshidrogenasa_lactica','Deshidrogenasa láctica'),('Fosfatasas_alcalinas','Fosfatasas alcalinas'),('Calcio_total','Calcio total'),('Fosforo','Fósforo')]

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

def foto_e_path(instance, filename):
    return os.path.join('AppReservaFacil/static/img', str(instance.ID_Especialista), filename)

class Especialista(models.Model):
    ID_Especialista = models.IntegerField(primary_key=True, unique=True)
    Nombre_completo_E = models.CharField(max_length=256)
    Rut = models.CharField(max_length=9, null=True)
    Sexo = models.CharField(choices = ([('Femenino','Femenino'), ('Masculino','Masculino')]),max_length=9, null=True)
    Fecha_de_nacimiento_E = models.DateField(null=True)
    Direccion_E = models.CharField(max_length=256, null=True)
    Telefono_E = models.CharField(max_length=9, null=True)
    ini_con_especialista = models.DateField(null=True)
    fin_con_especialista = models.DateField(null=True)
    Foto_E = models.ImageField(upload_to='Paciente',null=True)
    Especialidad_P = models.ForeignKey(Especialidad,null=True, on_delete=models.RESTRICT,related_name="Especialidad_P")
    Especialidad_S = models.ForeignKey(Especialidad,null=True, on_delete=models.RESTRICT,related_name="Especialidad_S")
    Dia_Esp_P = MultiSelectField(choices=DIAS_CHOICES)
    Dia_Esp_S = MultiSelectField(choices=DIAS_CHOICES)
    Minutes_Esp_P_Lun = models.IntegerField(null = True, choices=MINUTOS_CHOICES)
    Minutes_Esp_P_Mar = models.IntegerField(null = True, choices=MINUTOS_CHOICES)
    Minutes_Esp_P_Mie = models.IntegerField(null = True, choices=MINUTOS_CHOICES)
    Minutes_Esp_P_Jue = models.IntegerField(null = True, choices=MINUTOS_CHOICES)
    Minutes_Esp_P_Vie = models.IntegerField(null = True, choices=MINUTOS_CHOICES)
    Minutes_Esp_P_Sab = models.IntegerField(null = True, choices=MINUTOS_CHOICES)
    Minutes_Esp_P_Dom = models.IntegerField(null = True, choices=MINUTOS_CHOICES)
    Minutes_Esp_S_Lun = models.IntegerField(null = True, choices=MINUTOS_CHOICES)
    Minutes_Esp_S_Mar = models.IntegerField(null = True, choices=MINUTOS_CHOICES)
    Minutes_Esp_S_Mie = models.IntegerField(null = True, choices=MINUTOS_CHOICES)
    Minutes_Esp_S_Jue = models.IntegerField(null = True, choices=MINUTOS_CHOICES)
    Minutes_Esp_S_Vie = models.IntegerField(null = True, choices=MINUTOS_CHOICES)
    Minutes_Esp_S_Sab = models.IntegerField(null = True, choices=MINUTOS_CHOICES)
    Minutes_Esp_S_Dom = models.IntegerField(null = True, choices=MINUTOS_CHOICES)
    Usuario_E = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.Nombre_completo_E}'
    
class Operador(models.Model):
    ID_Operador = models.IntegerField(primary_key=True, unique=True)
    Nombre_completo_O = models.CharField(max_length=256)
    Rut = models.CharField(max_length=9, null=True)
    Sexo = models.CharField(choices = SEXO_CHOICES, max_length=9, null=True)
    Fecha_de_nacimiento_O = models.DateField(null=True)
    Direccion_O = models.CharField(max_length=256, null=True)
    Telefono_O = models.CharField(max_length=9, null=True)
    Foto_O = models.ImageField(upload_to='Operador', null=True)
    Fecha_de_contrato_O = models.DateField(null=True)
    Fecha_fin_de_contrato_O = models.DateField(null=True)
    Usuario_O = models.ForeignKey(User, null=True, on_delete=models.RESTRICT)

    def __str__(self):
        ID_Operador = str(self.ID_Operador)
        return f'{self.Nombre_completo_O} {ID_Operador}'
    class Meta:
        verbose_name='Operador'
        verbose_name_plural='Operadores'

class Paciente(models.Model):
    ID_Paciente = models.IntegerField(primary_key=True, unique=True)
    Nombre_Paciente = models.CharField(max_length = 256)
    Rut = models.CharField(max_length=9, null = True)
    Sexo = models.CharField(SEXO_CHOICES, max_length=9, null = True)
    Fecha_de_nacimiento_P = models.DateField(null = True)
    Direccion_P = models.CharField(max_length=256, null = True)
    Telefono_P = models.CharField(max_length=9, null = True)
    Usuario_P = models.ForeignKey(User, null=True, on_delete=models.RESTRICT)
    Primer_Login = models.BooleanField(default=True)

    def __str__(self):
        ID_Paciente = str(self.ID_Paciente)
        return f'{self.Nombre_Paciente} {ID_Paciente}'
    
    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'

class Cita(models.Model):
    ID_Cita = models.DateTimeField(primary_key=True, unique=True)
    Fecha_Cita = models.CharField(max_length=20, null=True)
    Hora_Cita = models.CharField(max_length=20, null=True)
    Confirmacion_Cita = models.BooleanField(default=False)
    Confirmacion_Cita_Operador = models.BooleanField(default=False)
    ID_Cliente = models.ForeignKey(User,null=True, on_delete=models.RESTRICT)
    ID_Especialista = models.ForeignKey(Especialista,null=True, on_delete=models.RESTRICT)

    def __datetime__ (self):
        return f'{self.ID_Cita} {self.Fecha_Cita} {self.Hora_Cita}'  

class CitaSinUsuario(models.Model):
    ID_Cita = models.DateTimeField(primary_key=True, unique=True)
    Fecha_Cita = models.CharField(max_length=20, null=True)
    Hora_Cita = models.CharField(max_length=20, null=True)
    Confirmacion_Cita = models.BooleanField(default=False)
    Confirmacion_Cita_Operador = models.BooleanField(default=False)
    Rut_Paciente = models.CharField(max_length=9, null=False)
    Email_Contacto = models.EmailField(null=True)
    Telefono_Contacto = models.IntegerField(null=True)
    ID_Especialista = models.ForeignKey(Especialista, on_delete=models.RESTRICT)
    
    def __datetime__ (self):
        return f'{self.ID_Cita} {self.Fecha_Cita} {self.Hora_Cita}'

class Mensaje(models.Model):
    Nombre_Remitente = models.CharField(max_length=100, editable=False)
    Nombre_Destinatario = models.CharField(max_length=100, editable=False)
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Remitente: {self.Nombre_Remitente}, Destinatario: {self.Nombre_Destinatario}"
    
    class Meta:
        verbose_name = 'Mensaje'
        verbose_name_plural = 'Mensajes'

class Ficha_Medica(models.Model):
    ID_Ficha_Medica = models.IntegerField(primary_key=True, unique=True)
    RUT_Pac = models.CharField(max_length=9)
    Nombre_Com_Pac = models.CharField(max_length = 256)
    Direccion_Pac = models.CharField(max_length=256, null = True)
    Telefono_Pac = models.CharField(max_length=9, null = True)
    Sis_Sal_Pac = models.CharField(choices = SISTEMA_SALUD, max_length=21, null=True)
    Grupo_Sanguineo = models.CharField(choices=GRUPO_SANGUINEO, max_length=7, null=True)

    Al_Antibioticos = models.BooleanField(null=True)
    Antibioticos_TI = models.CharField(max_length = 256, null=True)

    Al_Medicamentos = models.BooleanField(null=True)
    Medicamentos_TI = models.CharField(max_length = 256, null=True)

    Al_Alimentos = models.BooleanField(null=True)
    Alimentos_TI = models.CharField(max_length = 256, null=True)

    Al_Ani_Ins = models.BooleanField(null=True)
    Ani_Ins_TI = models.CharField(max_length = 256, null=True)

    Enf_Cronic = models.BooleanField(null=True)
    Enf_Cronic_TI = models.CharField(max_length = 256, null=True)

    Observaciones_Ficha = models.TextField(max_length=1000, null=True)

    def __str__(self):
        ID_Ficha_Medica = str(self.ID_Ficha_Medica)
        return f'{ID_Ficha_Medica}'
    
    class Meta:
        verbose_name = 'Ficha Médica'
        verbose_name_plural = 'Fichas Médicas'
    
class Receta (models.Model):
    Numero_receta = models.IntegerField()
    Especialista_receta = models.ForeignKey(Especialista, on_delete=models.RESTRICT,null=True)
    Rut_esp_receta = models.CharField(max_length = 9,null=True)
    Especialidad_receta = models.ForeignKey(Especialidad,null=True, on_delete=models.RESTRICT)
    Nompre_paciente_receta = models.CharField(max_length = 256,null=True)
    Rut_pac_receta = models.CharField(max_length = 9,null=True)
    Edad_pac_receta = models.IntegerField(null=True)
    Direccion_pac_receta = models.CharField(max_length=256, null=True)
    Diagnostico_rec = models.CharField(max_length=80, null=True)
    Descripcion_receta = models.TextField(max_length=256, null=True)

    def __str__(self):
        return f'{self.Numero_receta}'
    
class Examene (models.Model):
    Numero_orden_examen = models.IntegerField()
    Nombre_pac_orden = models.CharField(max_length=256, null=True)
    Rut_pac_orden = models.CharField(max_length = 9,null=True)
    Edad_pac_orden = models.IntegerField(null=True)
    Fecha_nac_pac_orden = models.DateField(null=True)
    Prevision_pac_orden = models.CharField(choices=TIPO_ATENCION, max_length=15, null = True)
    Servicio_pac_orden = models.CharField(max_length=80, null=True)
    Diagnostico_orden = models.CharField(max_length=80, null=True)
    Nombre_Medico_orden = models.CharField(max_length=256, null=True)
    Rut_Medico_orden = models.CharField(max_length = 9,null=True)
    Examenes = MultiSelectField(choices=EXAMENES,null=True)
    
    def __str__(self):
        return f'{self.Numero_orden_examen}'
    

#TODO REALIZAR EL MIGRATE PARA PROBARLO
class Ficha_Cita(models.Model):
    ID_Ficha_Cita = models.IntegerField(primary_key=True, unique=True)
    Fecha_Cita = models.DateField(null=False)
    Ficha_Medica_Pac = models.ForeignKey(Ficha_Medica,null=False, on_delete=models.RESTRICT)
    RUT_Pac = models.CharField(max_length=9)
    Nombre_Com_Pac = models.ForeignKey(Paciente,null=False, on_delete=models.RESTRICT)
    Nombre_Com_Esp = models.ForeignKey(Especialista,null=False, on_delete=models.RESTRICT)
    Diagnostico_Cita = models.TextField(max_length=256, null=True)
    Receta = models.ForeignKey(Receta,null=True, on_delete=models.RESTRICT)
    Examene = models.ForeignKey(Examene,null=True, on_delete=models.RESTRICT)

    def __str__(self):
        ID_Ficha_Cita = str(self.ID_Ficha_Cita)
        return f'{ID_Ficha_Cita}'
    
    class Meta:
        verbose_name = 'Ficha Cita'
        verbose_name_plural = 'Fichas Citas'

class CobrosEspecialistas(models.Model):

    Monto_Esp_P = models.IntegerField(null=True)
    Monto_Esp_S = models.IntegerField(null=True)
    # Nombre_completo_E = models.CharField(max_length=256, null = True)
    ID_Especialista = models.ForeignKey(Especialista, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.ID_Especialista}'
    
class Cobro (models.Model):
    ID_Cobro = models.IntegerField()
    Rut_Pac_Cobro = models.CharField(max_length=9, null = True)
    Especialista_Cobro = models.ForeignKey(Especialista, on_delete=models.RESTRICT)
    Especialidad_Cobro = models.ForeignKey(Especialidad,null=True, on_delete=models.RESTRICT)
    Monto = models.IntegerField()
    Estado_cobro = models.CharField(choices = ESTADO_COBRO, max_length=10, null=True)

    def __str__(self):
        return f'{self.ID_Cobro} {self.Rut_Pac_Cobro}'
    
class Boleta (models.Model):
    ID_Boleta = models.IntegerField()
    Rut_Pac_Boleta = models.CharField(max_length=9, null = True)
    Especialista_Boleta = models.ForeignKey(Especialista, on_delete=models.RESTRICT)
    Especialidad_Boleta = models.ForeignKey(Especialidad,null=True, on_delete=models.RESTRICT)
    Monto_Boleta = models.IntegerField()
    Fecha_Emision = models.DateField(null = False)
    Metodo_Pago = models.CharField(choices=METODO_PAGO, max_length=15)
    Efectivo = models.IntegerField(null = True)
    Vuelto = models.IntegerField(null = True)
    Tipo_atencion = models.CharField(choices=TIPO_ATENCION, max_length=15, null = True)
    Arancel = models.DecimalField(max_digits=3, decimal_places=2,default=0.0,null = True)
    Num_Documento =  models.IntegerField(null = True)
    def __str__(self):
        return f'{self.ID_Boleta} {self.Rut_Pac_Boleta}'