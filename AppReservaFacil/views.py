from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import *

# Create your views here.

def index(request):
    return render(request, "Clientes/index.html")

def inicio(request):
    return render(request, "Especialistas/inicio.html")

def inicioSesion(request):
    return render(request, "Clientes/inicioSesion.html")

def registrousuario(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method=='POST':
        formulario=CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user= authenticate(username=formulario.cleaned_data['username'], password=formulario.cleaned_data['password1'])
            login(request,user)
            print("Antes success")
            messages.success(request, "Te has registrado correctamente")
            print("Despues success")
            return redirect(to='../inicioSesion')

    return render(request, 'Clientes/registro.html', data)