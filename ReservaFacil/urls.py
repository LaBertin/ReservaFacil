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
    path('home/', views.home, name="home"),
    path('admin_Finanzas/', views.admin_Finanzas, name="admin_Finanzas"),
    path('admin_RRHH/', views.admin_RRHH, name="admin_RRHH"),
    path('admin_Sesiones/', views.admin_Sesiones, name="admin_Sesiones"),
    path('admin_Agregar/', views.admin_Agregar, name="admin_admin_Agregar"),
    path('admin_crearUsuario/', views.admin_crearUsuario, name="admin_crearUsuario"), 
    
    
]
