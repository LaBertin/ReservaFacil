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
        if 'seleccionar_hora' in request.POST:
            global Fecha
            Fecha = DateForm(request.POST)
            print('Fecha:', Fecha)
            Fecha = Fecha.cleaned_data
            Fecha = Fecha['date']
            print('Fecha obtenida')
            Fecha= datetime.date(Fecha)
            print(Fecha)
            print(type(Fecha))
            hora =  list(range(8,21))
            horacontext = {'hora':hora}
            print(hora)
            print(type(hora))
            print(horacontext)
            print("Pedir Hora Post")
            return render(request, 'clientes/cliente_Seleccionar_Hora.html', {'hora':horacontext})
        if 'pedir_cita' in request.POST:      
            data = {
                'formDate': DateForm()
            }  
            global Especialistas
            values = request.POST.get('pedir_cita')
            Especialistas = Especialista.objects.filter(ID_Especialista=values)
            print(Especialistas)
            contexto = {'especialista':Especialistas}  
            ID_Especialista = Especialistas[0].ID_Especialista
            print("ID_Especialistas:\n")
            print(ID_Especialista)
            return render(request, 'clientes/cliente_Seleccionar_Fecha.html', data)    
        print("Request method = POST")
        #Si pulsa el botón de seleccionar hora
        if 'hora_seleccionada' in request.POST:
            print("Hora Seleccionada")
            Usuario = User.objects.get(username=request.user.username)
            print("Usuario:\n")
            print(Usuario)
            hora_seleccionada = request.POST.get('hora_seleccionada')
            hora_seleccionada = hora_seleccionada+':00'
            print(Fecha)
            hora_seleccionada = str(Fecha)+str(' '+hora_seleccionada)
            print(hora_seleccionada)
            print("ID_Especialistas:\n")
            print(Especialistas[0])
            print("AAAAAAAAAAA")
            print(datetime.date(datetime(hora_seleccionada)))
            Citas_Usuario = Cita.objects.filter(ID_Cliente=Usuario)
            print("Deberia entrar al for")
            print(Citas_Usuario)
            count_c=0
            for c in Citas_Usuario:
                count_c = count_c+1
                print("C:\n")   
                print(c)
            #Cita.objects.create(ID_Cita=hora_seleccionada, ID_Cliente=Usuario, ID_Especialista=Especialistas[0])
            messages.success(request, "Hora creada con éxito")
            return render(request, 'clientes/cliente_Hora_creada.html', {'hora_seleccionada':hora_seleccionada})
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
    return render(request, 'clientes/cliente_Agendar_Hora.html')

def Cliente_anular_hora(request):
    if 'anular_hora' in request.POST:
        print("Pulsaste Anular Hora")
        Anular_Hora_Principal = request.POST.get('anular_hora')
        Anular_Hora = Anular_Hora_Principal.replace('de','')
        Anular_Hora = Anular_Hora.replace('a las','')
        Anular_Hora = Anular_Hora.replace('  ',' ')
        print(Anular_Hora)
        if 'Enero' in Anular_Hora:
            Anular_Hora = Anular_Hora.replace('Enero','January')
        elif 'Febrero' in Anular_Hora:
            Anular_Hora = Anular_Hora.replace('Febrero','February')
        elif 'Marzo' in Anular_Hora:
            Anular_Hora = Anular_Hora.replace('Marzo','March')
        elif 'Abril' in Anular_Hora:
            Anular_Hora = Anular_Hora.replace('Abril','April')
        elif 'Mayo' in Anular_Hora:
            Anular_Hora = Anular_Hora.replace('Mayo','May')
        elif 'Junio' in Anular_Hora:    
            Anular_Hora = Anular_Hora.replace('Junio','June')
        elif 'Julio' in Anular_Hora:
            Anular_Hora = Anular_Hora.replace('Julio','July')
        elif 'Agosto' in Anular_Hora:
            Anular_Hora = Anular_Hora.replace('Agosto','August')
        elif 'Septiembre' in Anular_Hora:
            Anular_Hora = Anular_Hora.replace('Septiembre','September')
        elif 'Octubre' in Anular_Hora:
            Anular_Hora = Anular_Hora.replace('Octubre','October')
        elif 'Noviembre' in Anular_Hora:
            Anular_Hora = Anular_Hora.replace('Noviembre','November')
        elif 'Diciembre' in Anular_Hora:
            Anular_Hora = Anular_Hora.replace('Diciembre','December')
        Anular_Hora = datetime.strptime(Anular_Hora, '%d %B %Y %H:%M')
        print(Anular_Hora)
        Cita.objects.filter(ID_Cita=Anular_Hora).delete()
        messages.success(request, "Cita anulada con éxito")
        return render(request, 'clientes/cliente_Hora_anulada.html', {'hora_principal':Anular_Hora_Principal})
    if request.user.is_authenticated:
        Usuario = User.objects.get(username=request.user.username)
        citas_cliente = Cita.objects.filter(ID_Cliente=Usuario)
        
        return render(request, 'clientes/cliente_Anular_Hora.html', {'citas_cliente':citas_cliente})
    else:
        return render(request, 'clientes/cliente_Anular_Hora.html')