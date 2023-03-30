from django.contrib import admin
from .models import *

# llamo a AdminAgregar
from AppReservaFacil.models import AdminAgregar, NuevoUsuarios

# Register your models here.

admin.site.register(Especialista)

admin.site.register(Especialidad)

admin.site.register(Area_Medica)

admin.site.register(Cita)

# formulario de Admin Agregar.
admin.site.register(AdminAgregar)

# formulario de Admin Agregar.
admin.site.register(NuevoUsuarios)