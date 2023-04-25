"""ReservaFacil URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from AppReservaFacil import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('inicio/', views.inicio),
    path('inicioSesion/', views.iniciarsesionusuario, name='inicioSesion'),
    path('registro/', views.registrousuario),
    path('perfil/', views.perfil_cliente, name = 'perfil'),
    path('cerrarSesion/', views.cerrarsesionusuario),
    path('agendar_hora/', views.cliente_Agendar_hora),
    path('anular_hora/', views.Cliente_anular_hora),
    path('consultar_hora/', views.Cliente_consultar_hora),
    path('obtener_especialidades/<int:area_medica_id>/', views. obtener_especialidades, name='obtener_especialidades'),

    path('admin_Agregar_Especialista/', views.agregar_empleado),    
    path('admin_Agregar_Operador/', views.agregar_operador),

    path('funciones_citas_operador/', views.operador_funciones, name='funciones_citas_operador'),
    #Consultar_Agenda
    path('agenda_citas/', views.operador_lista_agenda, name='agenda_citas'),
    path('agendar_citas_paciente/', views.operador_agendar_cita, name='agendar_citas_paciente'),
    path('confirmacion/', views.operador_confirmacion, name='confirmacion'),
    path('calendario_especialista/', views.operador_calendario_especialista, name='calendario_especialista'),
    path('operador_horas_esp/', views.operador_horas_especialista, name = 'operador_horas_esp'),
    
    #Modificar_Cita
    path('modificar_cita/', views.operador_modificar_cita, name='modificar_cita'),
    path('modificar_lista/', views.operador_modificar_lista, name='modificar_lista'),

    path('pago/', views.operador_pago, name='pago'),

    path('select_Destinatario/', views.select_destinatario, name='select_Destinatario'),
    path('chat/', views.chatsito, name='chat'),

    path('agenda_especialista/',views.especialista_Agenda, name='agenda_especialista'),
    path('agenda_dia/', views.especialista_list_citas, name='agenda_dia')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
