from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Especialista)

admin.site.register(Especialidad)

admin.site.register(Area_Medica)

admin.site.register(Cita)

admin.site.register(Operador)

admin.site.register(Paciente)

admin.site.register(Mensaje)

admin.site.register(CitaSinUsuario)

admin.site.register(Ficha_Medica)

admin.site.register(Ficha_Cita)

admin.site.register(CobrosEspecialistas)