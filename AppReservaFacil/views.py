from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import *
from django.contrib.auth.forms import *

# Create your views here.

def index(request):
    return render(request, "Clientes/index.html")

def inicio(request):
    return render(request, "Especialistas/inicio.html")

def registrousuario(request):
    formulario = {
        'formRegistarUsuario': FormRegistrarUsuario()
    }

    if request.method=='POST':
        formulario=FormRegistrarUsuario(data=request.POST)
        print(formulario.errors)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Te has registrado con éxito")
            return render(request, 'Clientes/iniciosSesion.html', {'form': formulario})
        else:
            #if #Si contraseña da aerroe print cambiar contraseña 
            formulario=FormRegistrarUsuario()
            messages.error(request, "Error al registrarte")

    return render(request, 'Clientes/registro.html', formulario)

def iniciarsesionusuario(request):
    data = {
        'formIniciarSesionUsuario': LoginUsuario()
    }
    if request.method=='POST':
        print(0)
        formulario=LoginUsuario(data=request.POST)
        print(1)
        print(formulario.is_valid())
        print(formulario.errors)
        if formulario.is_valid():
            print(2)
            usuario = authenticate(username=formulario.cleaned_data['username'], password=formulario.cleaned_data['password'])
            print(usuario)
            print(3)
            login(request,usuario)
            messages.success(request, "Has iniciado sesión con éxito")
            return redirect(to='../')
        else:
            messages.error(request, "Error al iniciar sesión")

    return render(request, 'Clientes/inicioSesion.html', data)

def cerrarsesionusuario(request):
    logout(request)
    messages.success(request, "Has cerrado sesión con éxito")
    return render(request,  'Clientes/cerrarSesion.html')