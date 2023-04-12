from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import *
from .models import *
from django.contrib.auth.forms import *
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
from django import template

from AppReservaFacil.models import AdminAgregar, NuevoUsuarios

from AppReservaFacil.models import AdminAgregar, NuevoUsuarios

# Create your views here.



#Def necesario para cambiar header dependiendo del rol
register = template.Library() 

@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists() 


# Dirección URL de vistas de Clientes
def index(request):
    nombre_Usuario = User.objects.get(username=request.user.username)
    Bool_Grupo = nombre_Usuario.groups.filter(name__in=['Especialistas']).exists()
    if Bool_Grupo == True:
        print(nombre_Usuario)
        nombre_Especialista = Especialista.objects.filter(Usuario_E=nombre_Usuario)[0].Nombre_completo_E
        img_Especialista = Especialista.objects.filter(Usuario_E=nombre_Usuario)[0].Foto_E
        nombre_Especialista = nombre_Especialista.split(' ')
        nombre_Especialista = nombre_Especialista[0]+' '+nombre_Especialista[3]
        print(nombre_Especialista)
        print(img_Especialista)
        return render(request, "Clientes/index.html", {'Nombre_E':nombre_Especialista,'Foto_E':img_Especialista})

    else:
        print("Otro")
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

#Definiciones del 

def registrousuario(request):
    formulario1 = {
        'formRegistarUsuario': FormRegistrarUsuario()
    }

    if request.method=='POST':
        formulario=FormRegistrarUsuario(data=request.POST)
        print(formulario.errors)
        if formulario.is_valid():
            usuario = request.POST.get('username')
            print(usuario)
            formulario.save()
            user = User.objects.get(username = usuario)
            grupo_Pacientes = Group.objects.get(name='Pacientes') 
            user.groups.add(grupo_Pacientes)
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
        formulario=LoginUsuario(data=request.POST)
        print(formulario.is_valid())
        print(formulario.errors)
        if formulario.is_valid():
            usuario = authenticate(username=formulario.cleaned_data['username'], password=formulario.cleaned_data['password'])
            print(usuario)
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
        if 'pedir_cita' in request.POST:     
            global dataformDate 
            dataformDate = {
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
            return render(request, 'clientes/cliente_Seleccionar_Fecha.html', dataformDate)    
        print("Request method = POST")
        if 'seleccionar_hora' in request.POST:
            global Fecha
            Fecha = DateForm(request.POST)
            print('Fecha:', Fecha)
            Fecha = Fecha.cleaned_data
            Fecha = Fecha['date']
            print('Fecha obtenida')
            Fecha= datetime.date(Fecha)
            print("Fecha")
            print(Fecha)
            print(type(Fecha))
            Fecha_Actual = datetime.today()
            Fecha_Actual = datetime.date(Fecha_Actual)
            print("Fecha Actual")
            print(Fecha_Actual)
            print(type(Fecha_Actual))
            if Fecha > Fecha_Actual:
                hora =  list(range(8,21))
                horacontext = {'hora':hora}
                print(hora)
                print(type(hora))
                print(horacontext)
                print("Pedir Hora Post")
                return render(request, 'clientes/cliente_Seleccionar_Hora.html', {'hora':horacontext})
            else:
                messages.error(request, "Seleccione una fecha mayor o igual a la actual.")
                return render(request, 'clientes/cliente_Seleccionar_Fecha.html',dataformDate)
        #Si pulsa el botón de seleccionar hora
        if 'hora_seleccionada' in request.POST:
            print("Hora Seleccionada")
            Usuario = User.objects.get(username=request.user.username)
            Mail = Usuario.email
            print("Usuario:\n")
            print(Usuario)
            print("Mail:\n")
            print(Mail)
            hora_seleccionada = request.POST.get('hora_seleccionada')
            hora = hora_seleccionada+':00'
            print(Fecha)
            hora_seleccionada = str(Fecha)+str(' '+hora)
            print(hora_seleccionada)
            print("ID_Especialistas:\n")
            print(Especialistas[0])
            Citas_Usuario = Cita.objects.filter(Fecha_Cita=Fecha).count()
            print("Deberia entrar al for")
            print(Citas_Usuario)
            if Citas_Usuario<3:
                Cita.objects.create(ID_Cita=hora_seleccionada,Fecha_Cita=Fecha, Hora_Cita=hora, ID_Cliente=Usuario, ID_Especialista=Especialistas[0])
                messages.success(request, "Hora creada con éxito")
                send_mail(
                    'Cita programada con éxito',
                    'Su cita con el especialista '+str(Especialistas[0])+' programada para la fecha: '+str(Fecha)+' a las '+str(hora)+' ha sido programada con éxito',
                    'settings.EMAIL_HOST_USER',
                    [Mail]  
                )
                return render(request, 'clientes/cliente_Hora_creada.html', {'hora_seleccionada':hora_seleccionada})
            else:
                messages.error(request, "Ha alcanzado el máximo de citas solicitadas en esta fecha: 3.")
                return render(request, 'clientes/cliente_Seleccionar_Fecha.html', dataformDate)
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
        Cita_usada=Cita.objects.filter(ID_Cita=Anular_Hora).get()
        Especialista_Cita=Cita_usada.ID_Especialista
        print(Especialista_Cita)
        Fecha=str(datetime.date(Anular_Hora))
        Hora=str(Anular_Hora.hour)+':'+str(Anular_Hora.minute)+str(Anular_Hora.minute)+':'+str(Anular_Hora.second)+str(Anular_Hora.second)
        Usuario=User.objects.get(username=request.user.username)
        Mail=Usuario.email
        Cita.objects.filter(ID_Cita=Anular_Hora).delete()
        send_mail(
                    'Cita anulada',
                    'Su cita con el especialista '+str(Especialista_Cita)+' programada para la fecha: '+str(Fecha)+' a las '+str(Hora)+' ha sido anulada.',
                    'settings.EMAIL_HOST_USER',
                    [Mail]  
                )
        messages.success(request, "Cita anulada con éxito")
        return render(request, 'clientes/cliente_Hora_anulada.html', {'hora_principal':Anular_Hora_Principal})
    if request.user.is_authenticated:
        Usuario = User.objects.get(username=request.user.username)
        citas_cliente = Cita.objects.filter(ID_Cliente=Usuario)
        
        return render(request, 'clientes/cliente_Anular_Hora.html', {'citas_cliente':citas_cliente})
    else:
        return render(request, 'clientes/cliente_Anular_Hora.html')
    

def Cliente_consultar_hora(request):
    if 'confirmar_cita' in request.POST:
        Confirmar_Cita_Principal = request.POST.get('confirmar_cita')
        Confirmar_Cita = Confirmar_Cita_Principal.replace('de','')
        Confirmar_Cita = Confirmar_Cita.replace('a las','')
        Confirmar_Cita = Confirmar_Cita.replace('  ',' ')
        print(Confirmar_Cita)
        if 'Enero' in Confirmar_Cita:
            Confirmar_Cita = Confirmar_Cita.replace('Enero','January')
        elif 'Febrero' in Confirmar_Cita:
            Confirmar_Cita = Confirmar_Cita.replace('Febrero','February')
        elif 'Marzo' in Confirmar_Cita:
            Confirmar_Cita = Confirmar_Cita.replace('Marzo','March')
        elif 'Abril' in Confirmar_Cita:
            Confirmar_Cita = Confirmar_Cita.replace('Abril','April')
        elif 'Mayo' in Confirmar_Cita:
            Confirmar_Cita = Confirmar_Cita.replace('Mayo','May')
        elif 'Junio' in Confirmar_Cita:    
            Confirmar_Cita = Confirmar_Cita.replace('Junio','June')
        elif 'Julio' in Confirmar_Cita:
            Confirmar_Cita = Confirmar_Cita.replace('Julio','July')
        elif 'Agosto' in Confirmar_Cita:
            Confirmar_Cita = Confirmar_Cita.replace('Agosto','August')
        elif 'Septiembre' in Confirmar_Cita:
            Confirmar_Cita = Confirmar_Cita.replace('Septiembre','September')
        elif 'Octubre' in Confirmar_Cita:
            Confirmar_Cita = Confirmar_Cita.replace('Octubre','October')
        elif 'Noviembre' in Confirmar_Cita:
            Confirmar_Cita = Confirmar_Cita.replace('Noviembre','November')
        elif 'Diciembre' in Confirmar_Cita:
            Confirmar_Cita = Confirmar_Cita.replace('Diciembre','December')
        Confirmar_Cita = datetime.strptime(Confirmar_Cita, '%d %B %Y %H:%M')
        print(Confirmar_Cita)
        #Cita.objects.filter(ID_Cita=Confirmar_Cita).update(Confirmacion_Cita=True)
        Datos=Cita.objects.filter(ID_Cita=Confirmar_Cita).get()
        Fecha=str(datetime.date(Confirmar_Cita))
        Hora=str(Confirmar_Cita.hour)+':'+str(Confirmar_Cita.minute)+str(Confirmar_Cita.minute)+':'+str(Confirmar_Cita.second)+str(Confirmar_Cita.second)
        Especialista_Cita=Datos.ID_Especialista
        Mail=User.objects.get(username=request.user.username).email
        Confirmar_Cita_str=str(Confirmar_Cita)
        send_mail(
                    'Cita confirmada',
                    'Su cita con el especialista '+str(Especialista_Cita)+' programada para la fecha: '+str(Fecha)+' a las '+str(Hora)+' ha sido confirmada.',
                    'settings.EMAIL_HOST_USER',
                    [Mail]  
                )
        messages.success(request,"Cita con fecha: "+Confirmar_Cita_str+ " confirmada con éxito")


    if 'consultar_hora' in request.POST:
        print("Pulsaste consultar Hora")
        Consultar_Hora_Principal = request.POST.get('consultar_hora')
        Consultar_Hora = Consultar_Hora_Principal.replace('de','')
        Consultar_Hora = Consultar_Hora.replace('a las','')
        Consultar_Hora = Consultar_Hora.replace('  ',' ')
        print(Consultar_Hora)
        if 'Enero' in Consultar_Hora:
            Consultar_Hora = Consultar_Hora.replace('Enero','January')
        elif 'Febrero' in Consultar_Hora:
            Consultar_Hora = Consultar_Hora.replace('Febrero','February')
        elif 'Marzo' in Consultar_Hora:
            Consultar_Hora = Consultar_Hora.replace('Marzo','March')
        elif 'Abril' in Consultar_Hora:
            Consultar_Hora = Consultar_Hora.replace('Abril','April')
        elif 'Mayo' in Consultar_Hora:
            Consultar_Hora = Consultar_Hora.replace('Mayo','May')
        elif 'Junio' in Consultar_Hora:    
            Consultar_Hora = Consultar_Hora.replace('Junio','June')
        elif 'Julio' in Consultar_Hora:
            Consultar_Hora = Consultar_Hora.replace('Julio','July')
        elif 'Agosto' in Consultar_Hora:
            Consultar_Hora = Consultar_Hora.replace('Agosto','August')
        elif 'Septiembre' in Consultar_Hora:
            Consultar_Hora = Consultar_Hora.replace('Septiembre','September')
        elif 'Octubre' in Consultar_Hora:
            Consultar_Hora = Consultar_Hora.replace('Octubre','October')
        elif 'Noviembre' in Consultar_Hora:
            Consultar_Hora = Consultar_Hora.replace('Noviembre','November')
        elif 'Diciembre' in Consultar_Hora:
            Consultar_Hora = Consultar_Hora.replace('Diciembre','December')
        Consultar_Hora = datetime.strptime(Consultar_Hora, '%d %B %Y %H:%M')
        print(Consultar_Hora)
        Cita_Seleccionada = Cita.objects.filter(ID_Cita=Consultar_Hora)
        print(Cita_Seleccionada)
        return render(request, 'clientes/cliente_Confirmar_Hora.html', {'cita_seleccionada':Cita_Seleccionada})
    if request.user.is_authenticated:
        Usuario = User.objects.get(username=request.user.username)
        citas_cliente = Cita.objects.filter(ID_Cliente=Usuario)
        
        return render(request, 'clientes/cliente_Consultar_Cita.html', {'citas_cliente':citas_cliente})
    else:
        return render(request, 'clientes/cliente_Consultar_Cita.html')


#####################################################################################
#####################################################################################
########################## Base de Datos de Admin_Agregar ############################

def AppReservaFacil(request):
    articulo = AdminAgregar.objects.all()
    if request.method == "POST":
        
        nombre = request.POST["nombre"]
        cargo = request.POST["cargo"]
        rut = request.POST["rut"]
        correo = request.POST["correo"]
        telefonoCelular = request.POST["telefonoCelular"]
        telefono = request.POST["telefono"]
        telefonoContacto = request.POST["telefonoContacto"]
        
        obj = AdminAgregar( nombre=nombre, cargo=cargo, rut=rut, correo=correo, telefonoCelular=telefonoCelular, telefono=telefono, telefonoContacto=telefonoContacto )
        obj.save()
        
        mensaje = "Se registro exitosamente exitosamente"
        return render(request,"admin/admin_Agregar.html", {"articulo":articulo,"rut": rut})
    
    return render(request,"admin/admin_Agregar.html",{"articulo":articulo})


########################## Base de Datos de Nuevo_Usuario ############################

def AppReservaFacil(request):
    articulos = NuevoUsuarios.objects.all()
    if request.method == "POST":
        
        nombreUser = request.POST["nombreUser"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        
        obj = NuevoUsuarios(nombreUser = nombreUser, password = password ,password2 = password2)
        obj.save()
        
        mensaje = "Se registro exitosamente exitosamente"
        return render(request,"admin/admin_crearUsuario.html", {"articulos":articulos,"password": password})
    
    return render(request,"admin/admin_crearUsuario.html",{"articulos":articulos})

#Definiciones de Especialista.
def homeEspecialista(request):
    
    return render(request,"Especialistas/inicio.html")