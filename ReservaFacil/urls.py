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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('inicio/', views.inicio),
    path('inicioSesion/', views.iniciarsesionusuario),
    path('registro/', views.registrousuario),
    path('cerrarSesion/', views.cerrarsesionusuario),
    path('agendar_hora/', views.cliente_Agendar_hora),
    path('anular_hora/', views.Cliente_anular_hora),
    path('consultar_hora/', views.Cliente_consultar_hora),
    path('obtener_especialidades/<int:area_medica_id>/', views. obtener_especialidades, name='obtener_especialidades'),
    path('admin_Agregar_Especialista/', views.agregar_empleado),    
    path('admin_Agregar_Operador/', views.agregar_operador),
]
