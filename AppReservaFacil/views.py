from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import *
from .models import *
from django.contrib.auth.forms import *
from datetime import datetime, timedelta


# Create your views here.

# Dirección URL de vistas de Clientes
def index(request):
    return render(request, "Clientes/index.html")

def inicio(request):
    return render(request, "Especialistas/inicio.html")

def inicioSesion(request):
    return render(request, "Clientes/inicioSesion.html")

# Dirección URL de vistas de Admin
# admin es el nombre de la carper donde se almacena los html

def home(request):
    return render(request, 'admin/home.html')  

def admin_Finanzas(request):
    return render(request, 'admin/admin_Finanzas.html')

def admin_RRHH(request):
    return render(request, 'admin/admin_RRHH.html')

def admin_Sesiones(request):
    return render(request, 'admin/admin_Sesiones.html')

def admin_Agregar(request):
    return render(request, 'admin/admin_Agregar.html')

def admin_crearUsuario(request):
    return render(request, 'admin/admin_crearUsuario.html')

def registrousuario(request):
    formulario1 = {
        'formRegistarUsuario': FormRegistrarUsuario()
    }

    if request.method=='POST':
        formulario=FormRegistrarUsuario(data=request.POST)
        print(formulario.errors)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Te has registrado con éxito")
            return render(request, 'clientes/registro.html', formulario1)
        else:
            #if #Si contraseña da aerroe print cambiar contraseña 
            formulario=FormRegistrarUsuario()
            messages.error(request, "Error al registrarte")

    return render(request, 'Clientes/registro.html', formulario1)


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

def cliente_Agendar_hora(request):
    if request.method == 'POST':
        if 'pedir_hora' in request.POST:        
            #Obtenemos la fecha actual Ej.27-03-2023 10:38:00
            DateTimeActual = datetime.today()
            #Obtenemos la fecha actual sin hora Ej.27-03-2023
            date = DateTimeActual.date()
            #Obtenemos año actual
            año = date.strftime("%Y")
            añocontext = {'año':año}
            #Obtenemos mes actual
            mes = date.strftime("%m")
            mescontext = {'mes':mes}
            #Obtenemos dia actual
            dia = date.strftime("%d")
            diacontext = {'dia':dia}
            hora =  list(range(8,21))
            horacontext = {'hora':hora}
            print(mes)
            print(año)
            print(dia)
            print(hora)
            print(type(hora))
            año = int(año)
            mes = int(mes)
            dia = int(dia)
            print(type(mes))
            print(diacontext)
            print(horacontext)
            creardate = datetime(año, mes, dia)
            #Cita.objects.create(ID_Cita = creardate)
            #Hola=Cita.objects.filter(ID_Cita = creardate)
            #print(Hola)
            #print(Hola)
            print(creardate)
            print("Pedir Hora Post")
            values = request.POST.get('pedir_hora')
            Especialistas = Especialista.objects.filter(ID_Especialista=values)
            contexto = {'especialista':Especialistas}
            ID_Especialista = Especialistas[0].ID_Especialista
            print("ID_Especialistas:\n")
            print(ID_Especialista)
            Usuario = User.objects.get(username=request.user.username)
            print("Usuario:\n")
            print(Usuario)
            return render(request, 'clientes/cliente_Seleccionar_Hora.html', {'año':añocontext, 'mes':mescontext, 'dia':diacontext, 'hora':horacontext})    
        print("Request method = POST")
        #Si pulsa el botón de seleccionar hora
        if 'hora_seleccionada' in request.POST:
            print("Hora Seleccionada")
            messages.success(request, "Hora creada con éxito")
            hora_seleccionada=request.POST.get('hora_seleccionada')
            print(type(hora_seleccionada))
            print(hora_seleccionada)
            return render(request, 'clientes/cliente_Hora_creada.html', {'hola':hora_seleccionada})
        #Cardiología filtro
        if 'cardiologia' in request.POST:
            valuebtn = 'Cardiología'
        #Nutricionista filtro
        if 'nutricionista' in request.POST:
            valuebtn = 'Nutricionista'
        if 'analisis' in request.POST:
            valuebtn = 'Análisis'
        if 'movimiento_humano' in request.POST:
            valuebtn = 'Movimiento Humano'
        if 'otorrinologo' in request.POST:
            valuebtn = 'Otorrinología'
        if 'radiologia' in request.POST:
            valuebtn = 'Radiología'
        values = request.POST.get('pedir_hora')
        print("Areas Medicas")
        Areas_Medicas = Area_Medica.objects.filter(Nombre_Area_Medica = valuebtn)
        print(Areas_Medicas)
        print("Especialidades")
        Especialidades = Especialidad.objects.filter(Area_Medica_F = Areas_Medicas[0])
        print(Especialidades)
        print("Especialistas")
        EspecialistasF = Especialista.objects.none()
        for x in Especialidades:
            print("EF Antes")
            print(EspecialistasF)
            print("Entrando a for")
            print("x")
            print(x)
            Especialistas = Especialista.objects.filter(Especialidad_P=x)
            EspecialistasF = EspecialistasF.union(Especialistas)
            print("Especialistas: ")
            print(Especialistas)
            print(EspecialistasF)
            contexto = {'especialista':EspecialistasF}
            print("Contexto: ")
            print(contexto)
        return render(request, 'clientes/listar_Especialistas.html', contexto)
        
        
    print('FINAL')
    return render(request, 'clientes/cliente_Agendar_Hora.html')

