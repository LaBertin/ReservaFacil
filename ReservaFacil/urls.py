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
    path('inicioSesion/', views.iniciarsesionusuario, name='inicioSesion'),
    path('registro/', views.registrousuario),
    path('perfil/', views.perfil_cliente, name = 'perfil'),
    path('cerrarSesion/', views.cerrarsesionusuario),
    path('agendar_hora/', views.cliente_Agendar_hora),
    path('anular_hora/', views.Cliente_anular_hora),
    path('consultar_hora/', views.Cliente_consultar_hora),
    path('obtener_especialidades/<int:area_medica_id>/', views. obtener_especialidades, name='obtener_especialidades'),


    #Admin
    path('admin_Agregar_Especialista/', views.agregar_empleado, name='admin_Agregar_Especialista'),    
    path('admin_Eliminar_Especialista/', views.admin_Eliminar_Especialista, name='admin_Eliminar_Especialista'),
    path('admin_Agregar_Operador/', views.agregar_operador, name='admin_Agregar_Operador'),
    path('admin_Eliminar_Operador/', views.admin_Eliminar_Operador, name='admin_Eliminar_Operador'),
    path('admin_Agregar_Especialidad/', views.admin_Agregar_Especialidad, name='admin_Agregar_Especialidad'),
    path('admin_Eliminar_Especialidad/', views.admin_Eliminar_Especialidad, name='admin_Eliminar_Especialidad'),

    path('funciones_citas_operador/', views.operador_funciones, name='funciones_citas_operador'),

    #Consultar_Agenda
    path('agenda_citas/', views.operador_lista_agenda, name='agenda_citas'),

    path('agenda_citas_dos/', views.operador_lista_agenda_dos, name='agenda_citas_dos'),
    path('agenda_citas_medico/', views.operador_agenda_medica, name='agenda_citas_medico'),


    path('agendar_citas_paciente/', views.operador_agendar_cita, name='agendar_citas_paciente'),
    
    path('calendario_especialista/', views.operador_calendario_especialista, name='calendario_especialista'),
    path('operador_horas_esp/', views.operador_horas_especialista, name = 'operador_horas_esp'),

    #Especialista Fichas Médicas Pacientes

    path('pacientes_fichas_medicas/', views.pacientes_fichas_medicas, name = 'pacientes_fichas_medicas'),
    
    #Modificar_Cita
    path('modificar_cita/', views.operador_modificar_cita, name='modificar_cita'),
    path('modificar_lista/', views.operador_modificar_lista, name='modificar_lista'),
    path('modificar_cita_seleccionada/', views.operador_modificar_seleccion, name='modificar_cita_seleccionada'),
    path('modificar_fecha/', views.operador_modificar_fecha, name='modificar_fecha'),
    
    #Confirmar Cita Operador
    path('confirmacion/', views.operador_confirmacion, name='confirmacion'),
    path('confirmacion_citas/', views.operador_confirmacion_citas, name='confirmacion_citas'),

    #Pago
    path('pago/', views.operador_pago, name='pago'),
    path('cobros_paciente/', views.operador_pago_cobros, name='cobros_paciente'),
    path('boleta/', views.operador_boleta, name='boleta'),
    
    #Pago
    path('operador_pagar/', views.operador_pagar, name='operador_pagar'),

    path('select_Destinatario/', views.select_destinatario, name='select_Destinatario'),
    path('chat/', views.chatsito, name='chat'),
    path('ficha_medica/', views.list_ficha_medica, name='ficha_medica'),
    path('filtro_ficha_medica/', views.filtro_ficha_medica, name='filtro_ficha_medica'),
    path('crear_ficha_medica/', views.form_ficha_medica, name='crear_ficha_medica'),
    path('agregar_cita_medica/', views.agregar_cita_medica, name='agregar_cita_medica'),
    path('ver_cita_medica/', views.ver_cita_medica, name='ver_cita_medica'),
    path('ver_ficha_medica/', views.ver_ficha_medica, name='ver_ficha_medica'),

    #Receta medica
    path('receta_medica/', views.ver_receta_medica, name='receta_medica'),
    
    #Orden Examen
    path('orden_examen/', views.ver_orden_examen, name='orden_examen'),


    path('agenda_especialista/',views.especialista_Agenda, name='agenda_especialista'),
    path('agenda_dia/', views.especialista_list_citas, name='agenda_dia'),

    #API RUT
    # path('api/rut/activities/<str:rut>/', views.respuesta_api, name='resultado_api'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
