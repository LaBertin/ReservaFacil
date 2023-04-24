from django.shortcuts import render,redirect
from django.http import HttpResponse, QueryDict, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import *
from .models import *
from django.contrib.auth.forms import *
from datetime import datetime, timedelta, time
from django.core.mail import send_mail
from django.conf import settings
from django import template
import calendar
from django.urls import reverse
import unicodedata


# Create your views here.



#Def necesario para cambiar header dependiendo del rol
register = template.Library() 

@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists() 


# Dirección URL de vistas de Clientes
def index(request):
    if request.user.is_authenticated==True:
        nombre_Usuario = User.objects.get(username=request.user.username)
        Bool_Grupo = nombre_Usuario.groups.filter(name__in=['Especialistas']).exists()
        if Bool_Grupo == True:
            print(nombre_Usuario)
            nombre_Especialista = Especialista.objects.filter(Usuario_E=nombre_Usuario)[0].Nombre_completo_E
            nombre_Especialista = nombre_Especialista.split(' ')
            nombre_Especialista = nombre_Especialista[0]+' '+nombre_Especialista[-2]
            Especialista_Cont = Especialista.objects.get(Usuario_E=nombre_Usuario)
            print(nombre_Especialista)
            return render(request, "Clientes/index.html", {'Nombre_E':nombre_Especialista,'Especialista_Cont':Especialista_Cont})

        else:
            print("Otro")
            Bool_Grupo = nombre_Usuario.groups.filter(name__in=['Operadores']).exists()
            if Bool_Grupo == True:
                print(nombre_Usuario)
                nombre_Operador = Operador.objects.filter(Usuario_O=nombre_Usuario)[0].Nombre_completo_O
                img_Operador = Operador.objects.filter(Usuario_O=nombre_Usuario)[0].Foto_O
                nombre_Operador = nombre_Operador.split(' ')
                nombre_Operador = nombre_Operador[0]+' '+nombre_Operador[3]
                print(nombre_Operador)
                print(img_Operador)
                return render(request, "Clientes/index.html", {'Nombre_O':nombre_Operador,'Foto_O':img_Operador})

            else:
                print("Otro")
                Bool_Grupo = nombre_Usuario.groups.filter(name__in=['Operadores']).exists()
                return render(request, "Clientes/index.html")
        
    else:
        return render(request, "Clientes/index.html")

def inicio(request):
    return render(request, "Especialistas/inicio.html")

def inicioSesion(request):
    return render(request, "Clientes/inicioSesion.html")
# Dirección URL de vistas de Admin
# admin es el nombre de la carper donde se almacena los html
def admin_crearUsuario(request):
    return render(request, 'admin/admin_crearUsuario.html')
#Definiciones del 

def registrousuario(request):
    formulario1 = {
        'formRegistarUsuario': FormRegistrarUsuario()
    }

    if request.method=='POST':
        print(request.POST)
        formulario=FormRegistrarUsuario(data=request.POST)
        print(formulario)
        print(formulario.errors)
        if formulario.is_valid():
            usuario = request.POST.get('username')
            print(usuario)
            formulario.save()
            user = User.objects.get(username = usuario)
            grupo_Pacientes = Group.objects.get(name='Pacientes') 
            user.groups.add(grupo_Pacientes)
            count_paciente = Paciente.objects.all().count()+1
            Usuario_P = User.objects.filter(username=usuario)[0]
            Paciente.objects.create(ID_Paciente=count_paciente, Usuario_P = Usuario_P)
            messages.success(request, "Te has registrado con éxito")
            return redirect('inicioSesion')
        else:
            formulario=FormRegistrarUsuario()
            messages.error(request, "Error al registrarte")

    return render(request, 'Clientes/registro.html', formulario1)

def perfil_cliente(request):
    formulario_pac = {'formulario_pac': FormPaciente}
    if request.method=='POST':
        form_completo = FormPaciente(data = request.POST)
        if form_completo.is_valid():

            nombre_pac = form_completo.cleaned_data['nom_com_pac']
            rut_pac = form_completo.cleaned_data['rut_pac']
            sexo_pac = form_completo.cleaned_data['sexo_pac']
            fecha_nac_pac = form_completo.cleaned_data['fecha_nac_pac']
            direccion_pac = form_completo.cleaned_data['direccion_pac']
            telefono_pac = form_completo.cleaned_data['telefono_pac']
            first_login = False

            usuario = User.objects.get(username=request.user.username)
            Paciente.objects.filter(Usuario_P = usuario).update(Nombre_Paciente=nombre_pac,Rut=rut_pac,Sexo=sexo_pac,Fecha_de_nacimiento_P=fecha_nac_pac,Direccion_P=direccion_pac,Telefono_P=telefono_pac,Primer_Login=first_login)
            messages.success(request, "Exito al actualizar")
            return redirect('index')
        else:
            formulario_pac = FormPaciente()
            messages.error(request, "Error")
    return render(request, 'Clientes/perfil_cliente.html', formulario_pac)

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
            print(f'Usuario: {usuario}')
            login(request,usuario)
            usuario_prueba = User.objects.get(username = formulario.cleaned_data['username'])

            usuarioqs = User.objects.filter(username = request.user.username)
            print('PASO EL LOGIN LOCO')
            paciente_qs = Paciente.objects.filter(Usuario_P = usuario_prueba)
            
            valor_hasgroup = has_group(usuarioqs[0], 'Pacientes')
            print(f'retorno: {valor_hasgroup}')
            if valor_hasgroup:
                if paciente_qs[0].Primer_Login:
                    paciente_qs[0].Primer_Login = False
                    messages.success(request, "Has iniciado sesión con éxito")
                    return redirect(to='perfil')
                else:
                    messages.success(request, "Has iniciado sesión con éxito")
                    return redirect(to='index')
            else:
                messages.success(request, "Has iniciado sesión con éxito")
                return redirect(to='index')

        else:
            messages.error(request, "Error al iniciar sesión")

    return render(request, 'Clientes/inicioSesion.html', data)

def cerrarsesionusuario(request):
    logout(request)
    messages.success(request, "Has cerrado sesión con éxito")
    return render(request,  'Clientes/cerrarSesion.html')

def cliente_Agendar_hora(request):
    formulario_area_medica = {'formAreaMedica':AgendarForm}
    if request.method == 'POST':
        if 'ver_especialista' in request.POST:
            global especialidad_select

            values = request.POST.get('pedir_hora')
            especialidad_select = request.POST.get('especialidad_a')
            print(especialidad_select)
            
            #Obtenemos todos los medicos con la especialidad registrada.
            qspecialista = Especialista.objects.filter(Especialidad_P = especialidad_select)
            qspecialistas = Especialista.objects.filter(Especialidad_S = especialidad_select)
            
            qsListaEspecialidad=[]
            for x in qspecialista:
                qsListaEspecialidad.append(x.Dia_Esp_P)

            for x in qspecialistas:
                qsListaEspecialidad.append(x.Dia_Esp_S)

            print(qsListaEspecialidad)

            #Juntamos todos los resultados en un mismo Queryset
            qspecialista = qspecialista | qspecialistas 

            qspecialista = {'qspecialista':qspecialista, 'qsListaEspecialidad':qsListaEspecialidad,'especialidad_select':especialidad_select}

            return render(request, 'clientes/listar_Especialistas.html', qspecialista)
        if 'pedir_cita' in request.POST:    
            global Especialistas
            global dias_es
            global fechas
            global dataformDate 
            global ID_Especialista
            global dias_p
            global dias_s
            
            valores = request.POST.get('pedir_cita')
            print(f'Valores del pedir cita {valores}')
            print(type(valores))
            values = valores.split(' ')[0]
            dias_es = str(valores.split(' ',1)[1].replace(' ',''))
            dias_en = dias_es.replace('Lunes','Monday').replace('Martes','Tuesday').replace('Miercoles','Wednesday').replace('Jueves','Thursday').replace('Viernes','Friday').replace('Sabado','Saturday').replace('Domingo','Sunday')
            dias_es2 = dias_es.replace('Lunes','lun').replace('Martes','mar').replace('Miercoles','mie').replace('Jueves','jue').replace('Viernes','vie').replace('Sabado','sab').replace('Domingo','dom').split(',')
            print(dias_en)
            Especialistas = Especialista.objects.filter(ID_Especialista=values)
            Especialistas2 = Especialista.objects.get(ID_Especialista=values)
            print(type(Especialistas2.Dia_Esp_P))

            dias_p = Especialistas2.Dia_Esp_P
            dias_p = [d.strip() for d in dias_p]
            print(f'dias P {dias_p}')

            dias_s = Especialistas2.Dia_Esp_S
            dias_s = [d.strip() for d in dias_s]
            print(f'dias S {dias_s}')
            
            print(Especialistas)
            ID_Especialista = Especialistas[0].ID_Especialista
            print("ID_Especialistas:\n")
            print(ID_Especialista)

            # Obtener la fecha actual
            hoy = date.today()

            # Calcular la fecha dentro de un año
            next_year = hoy + timedelta(days=365)
            print(next_year)

            # Verificar si el año resultante es bisiesto
            if calendar.isleap(next_year.year):
                print("Bisiesto")
                # Si es bisiesto, ajustar la fecha al 29 de febrero
                next_year = next_year.replace(month=2, day=29)
            else:
                print("No")
                # Si no es bisiesto, mantener la fecha tal como está
                next_year = next_year.replace(year=next_year.year)

            # Imprimir la fecha resultante
            print(next_year)
            fechas = []
            while hoy <= next_year:
                diasemana = hoy.weekday()
                nombredia = calendar.day_name[diasemana]
                if nombredia in dias_en:
                    fechas.append(hoy)
                hoy += timedelta(days=1)

            dataformDate = {
                'formDate': DateForm(),
                'fechas': fechas,
            }

            return render(request, 'clientes/cliente_Seleccionar_Fecha.html', dataformDate)    
        if 'seleccionar_hora' in request.POST:
            global Fecha
            Fecha = DateForm(request.POST)
            
            if Fecha.is_valid():    
                Fecha = Fecha.cleaned_data['date']
                print(type(Fecha))
                print(Fecha)
                dia_semana = calendar.day_name[Fecha.weekday()]
                dia_semana = dia_semana.replace('Monday','Lun').replace('Tuesday','Mar').replace('Wednesday','Mie').replace('Thursday','Jue').replace('Friday','Vie').replace('Saturday','Sab').replace('Sunday','Dom')
                print(dia_semana)
                print(type(especialidad_select))
                print(especialidad_select)
                Especialiades = Especialidad.objects.get(Codigo_especialidad = especialidad_select)
                print(type(Especialiades))
                print(Especialistas[0].Especialidad_P)
                print(type(Especialistas[0].Especialidad_P))
                if Especialiades == Especialistas[0].Especialidad_P:
                    Minutes_Esp_Dinamico = "Minutes_Esp_P_" + dia_semana
                    minutos_especialidad = Especialistas[0].__dict__[Minutes_Esp_Dinamico]  
                if Especialiades == Especialistas[0].Especialidad_S:
                    Minutes_Esp_Dinamico = "Minutes_Esp_S_" + dia_semana
                    minutos_especialidad = Especialistas[0].__dict__[Minutes_Esp_Dinamico]

                #Saber los minutos del día seleccionado.
                
                if Fecha in fechas:
                    fecha_ini = datetime.combine(Fecha, time(hour=8, minute=0))
                    hora_ini = fecha_ini.hour
                    print(hora_ini)
                    fecha_fin = datetime.combine(Fecha, time(hour=21, minute=0))
                    hora_fin = fecha_fin.hour
                    print(hora_fin)
                    list_horas = []
                    while fecha_ini.hour < hora_fin:
                        list_horas.append(fecha_ini.strftime('%H:%M:%S'))
                        fecha_ini = fecha_ini + timedelta(minutes=minutos_especialidad)
                    print(list_horas)
                    Citas_Reservadas = Cita.objects.filter(ID_Especialista=ID_Especialista,Fecha_Cita=Fecha)
                    list_Citas_Reservadas = []
                    for x in Citas_Reservadas:
                        list_Citas_Reservadas.append(x.Hora_Cita.split(' ')[-1])
                        print("Hora_Cita")
                        print(x.Hora_Cita)

                    print(list_Citas_Reservadas)
                    list_horas = {'list_horas':list_horas, 'list_Citas_Reservadas':list_Citas_Reservadas}
                    return render(request, 'clientes/cliente_Seleccionar_Hora.html', list_horas)
                else:
                    messages.error(request, "Ingrese una fecha en los dias: "+dias_es+".")
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
            print("hora seleccionada")
            print(hora_seleccionada)
            print(Fecha)
            hora_seleccionada = str(Fecha)+str(' '+hora_seleccionada)
            print(hora_seleccionada)
            print("ID_Especialistas:\n")
            print(Especialistas[0])
            Citas_Usuario = Cita.objects.filter(Fecha_Cita=Fecha).count()
            print("Deberia entrar al for")
            print(Citas_Usuario)
            if Citas_Usuario<3:
                Cita.objects.create(ID_Cita=hora_seleccionada,Fecha_Cita=Fecha, Hora_Cita=hora_seleccionada, ID_Cliente=Usuario, ID_Especialista=Especialistas[0])
                messages.success(request, "Hora creada con éxito")
                """
                send_mail(
                    'Cita programada con éxito',
                    'Su cita con el especialista '+str(Especialistas[0])+' programada para la fecha: '+str(Fecha)+' a las '+str(hora_seleccionada)+' ha sido programada con éxito',
                    'settings.EMAIL_HOST_USER',
                    [Mail]  
                )
                """
                return render(request, 'clientes/cliente_Hora_creada.html', {'hora_seleccionada':hora_seleccionada})
            else:
                messages.error(request, "Ha alcanzado el máximo de citas solicitadas en esta fecha: 3.")
                return render(request, 'clientes/cliente_Seleccionar_Fecha.html', dataformDate)
    return render(request, 'clientes/cliente_Agendar_Hora.html', formulario_area_medica)

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
        """
        send_mail(
                    'Cita anulada',
                    'Su cita con el especialista '+str(Especialista_Cita)+' programada para la fecha: '+str(Fecha)+' a las '+str(Hora)+' ha sido anulada.',
                    'settings.EMAIL_HOST_USER',
                    [Mail]  
                )
        """
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
        Cita.objects.filter(ID_Cita=Confirmar_Cita).update(Confirmacion_Cita=True)
        Datos=Cita.objects.filter(ID_Cita=Confirmar_Cita).get()
        Fecha=str(datetime.date(Confirmar_Cita))
        Hora=str(Confirmar_Cita.hour)+':'+str(Confirmar_Cita.minute)+str(Confirmar_Cita.minute)+':'+str(Confirmar_Cita.second)+str(Confirmar_Cita.second)
        Especialista_Cita=Datos.ID_Especialista
        Mail=User.objects.get(username=request.user.username).email
        Confirmar_Cita_str=str(Confirmar_Cita)
        """
        send_mail(
                    'Cita confirmada',
                    'Su cita con el especialista '+str(Especialista_Cita)+' programada para la fecha: '+str(Fecha)+' a las '+str(Hora)+' ha sido confirmada.',
                    'settings.EMAIL_HOST_USER',
                    [Mail]  
                )
        """
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

def agregar_empleado(request):
    nuevo_emp_form = {
        'formEspecialista': FormEspecialista()
    }
    if request.method=='POST':
        csrfmiddlewaretoken=request.POST['csrfmiddlewaretoken']
        formulario = FormEspecialista(data = request.POST)

        if formulario.is_valid():
            nom_com_especialista = request.POST.get('nom_com_especialista')
            print(nom_com_especialista)

            fecha_nac_especialista = request.POST.get('fecha_nac_especialista')
            print(fecha_nac_especialista)

            direccion_especialista = request.POST.get('direccion_especialista')
            print(direccion_especialista)

            
            foto_e = request.FILES['Foto_E']
            print(type(foto_e))
            print(foto_e)

            contacto_especialista = request.POST.get('contacto_especialista')
            print(contacto_especialista)
            
            rut = request.POST.get('rut')
            print(rut)

            sexo = request.POST.get('sexo')
            print(sexo)

            fecha_ini_con = request.POST.get('ini_con_especialista')
            print(fecha_ini_con)

            fecha_ini_fin = request.POST.get('fin_con_especialista')
            print(fecha_ini_fin)


            especialidad_p = request.POST.get('especialidad_p')
            print(especialidad_p)
            especialidad_p=Especialidad.objects.filter(Codigo_especialidad=especialidad_p).get()
            print(especialidad_p)

            especialidad_s = request.POST.get('especialidad_s')
            print(especialidad_s)

            if especialidad_s != "":
                especialidad_s=Especialidad.objects.filter(Codigo_especialidad=especialidad_s).get()
                print(especialidad_s)
            else:
                especialidad_s = None

            dia_p = formulario.cleaned_data['dia_p'].replace("'","").strip('][').split(', ')
            print(dia_p)
            print(type(dia_p))
            
            if formulario.cleaned_data['dia_s']!="":
                dia_s = formulario.cleaned_data['dia_s'].replace("'","").strip('][').split(', ')
                print(dia_s)
            else:
                print("dia_s sin nada")
                dia_s = None


            #Minutos Especialidad P

            if formulario.cleaned_data['Minutes_Esp_P_Lun']!="":
                Minutes_Esp_P_Lun = formulario.cleaned_data['Minutes_Esp_P_Lun']
                print(f'Minutes_Esp_P_Lun {Minutes_Esp_P_Lun}')
                print(type(Minutes_Esp_P_Lun))
            else:
                print("Minutes_Esp_P_Lun nada")
                Minutes_Esp_P_Lun=None
                print(Minutes_Esp_P_Lun)
                print(type(Minutes_Esp_P_Lun))

            if formulario.cleaned_data['Minutes_Esp_P_Mar']!="":
                Minutes_Esp_P_Mar = formulario.cleaned_data['Minutes_Esp_P_Mar']
                print(f'Minutes_Esp_P_Mar {Minutes_Esp_P_Mar}')
                print(type(Minutes_Esp_P_Mar))
            else:
                print("Minutes_Esp_P_Mar nada")
                Minutes_Esp_P_Mar=None
                print(Minutes_Esp_P_Mar)
                print(type(Minutes_Esp_P_Mar))

            if formulario.cleaned_data['Minutes_Esp_P_Mie']!="":
                Minutes_Esp_P_Mie = formulario.cleaned_data['Minutes_Esp_P_Mie']
                print(f'Minutes_Esp_P_Mie {Minutes_Esp_P_Mie}')
                print(type(Minutes_Esp_P_Mie))
            else:
                print("Minutes_Esp_P_Mie nada")
                Minutes_Esp_P_Mie=None
                print(Minutes_Esp_P_Mie)
                print(type(Minutes_Esp_P_Mie))            

            if formulario.cleaned_data['Minutes_Esp_P_Jue']!="":
                Minutes_Esp_P_Jue = formulario.cleaned_data['Minutes_Esp_P_Jue']
                print(f'Minutes_Esp_P_Jue {Minutes_Esp_P_Jue}')
                print(type(Minutes_Esp_P_Jue))
            else:
                print("Minutes_Esp_P_Jue nada")
                Minutes_Esp_P_Jue=None
                print(Minutes_Esp_P_Jue)
                print(type(Minutes_Esp_P_Jue))     

            if formulario.cleaned_data['Minutes_Esp_P_Vie']!="":
                Minutes_Esp_P_Vie = formulario.cleaned_data['Minutes_Esp_P_Vie']
                print(f'Minutes_Esp_P_Vie {Minutes_Esp_P_Vie}')
                print(type(Minutes_Esp_P_Vie))
            else:
                print("Minutes_Esp_P_Vie nada")
                Minutes_Esp_P_Vie=None
                print(Minutes_Esp_P_Vie)
                print(type(Minutes_Esp_P_Vie))  

            if formulario.cleaned_data['Minutes_Esp_P_Sab']!="":
                Minutes_Esp_P_Sab = formulario.cleaned_data['Minutes_Esp_P_Sab']
                print(f'Minutes_Esp_P_Sab {Minutes_Esp_P_Sab}')
                print(type(Minutes_Esp_P_Sab))
            else:
                print("Minutes_Esp_P_Sab nada")
                Minutes_Esp_P_Sab=None
                print(Minutes_Esp_P_Sab)
                print(type(Minutes_Esp_P_Sab))  

            if formulario.cleaned_data['Minutes_Esp_P_Dom']!="":
                Minutes_Esp_P_Dom = formulario.cleaned_data['Minutes_Esp_P_Dom']
                print(f'Minutes_Esp_P_Dom {Minutes_Esp_P_Dom}')
                print(type(Minutes_Esp_P_Dom))
            else:
                print("Minutes_Esp_P_Dom nada")
                Minutes_Esp_P_Dom=None
                print(Minutes_Esp_P_Dom)
                print(type(Minutes_Esp_P_Dom))  

            #Minutos Especialidad S

            if formulario.cleaned_data['Minutes_Esp_S_Lun']!="":
                Minutes_Esp_S_Lun = formulario.cleaned_data['Minutes_Esp_S_Lun']
                print(f'Minutes_Esp_S_Lun {Minutes_Esp_S_Lun}')
                print(type(Minutes_Esp_S_Lun))
            else:
                print("Minutes_Esp_S_Lun nada")
                Minutes_Esp_S_Lun=None
                print(Minutes_Esp_S_Lun)
                print(type(Minutes_Esp_S_Lun))

            if formulario.cleaned_data['Minutes_Esp_S_Mar']!="":
                Minutes_Esp_S_Mar = formulario.cleaned_data['Minutes_Esp_S_Mar']
                print(f'Minutes_Esp_S_Mar {Minutes_Esp_S_Mar}')
                print(type(Minutes_Esp_S_Mar))
            else:
                print("Minutes_Esp_S_Mar nada")
                Minutes_Esp_S_Mar=None
                print(Minutes_Esp_S_Mar)
                print(type(Minutes_Esp_S_Mar))

            if formulario.cleaned_data['Minutes_Esp_S_Mie']!="":
                Minutes_Esp_S_Mie = formulario.cleaned_data['Minutes_Esp_S_Mie']
                print(f'Minutes_Esp_S_Mie {Minutes_Esp_S_Mie}')
                print(type(Minutes_Esp_S_Mie))
            else:
                print("Minutes_Esp_S_Mie nada")
                Minutes_Esp_S_Mie=None
                print(Minutes_Esp_S_Mie)
                print(type(Minutes_Esp_S_Mie))            

            if formulario.cleaned_data['Minutes_Esp_S_Jue']!="":
                Minutes_Esp_S_Jue = formulario.cleaned_data['Minutes_Esp_S_Jue']
                print(f'Minutes_Esp_S_Jue {Minutes_Esp_S_Jue}')
                print(type(Minutes_Esp_S_Jue))
            else:
                print("Minutes_Esp_S_Jue nada")
                Minutes_Esp_S_Jue=None
                print(Minutes_Esp_S_Jue)
                print(type(Minutes_Esp_S_Jue))     

            if formulario.cleaned_data['Minutes_Esp_S_Vie']!="":
                Minutes_Esp_S_Vie = formulario.cleaned_data['Minutes_Esp_S_Vie']
                print(f'Minutes_Esp_S_Vie {Minutes_Esp_S_Vie}')
                print(type(Minutes_Esp_S_Vie))
            else:
                print("Minutes_Esp_S_Vie nada")
                Minutes_Esp_S_Vie=None
                print(Minutes_Esp_S_Vie)
                print(type(Minutes_Esp_S_Vie))            
            
            if formulario.cleaned_data['Minutes_Esp_S_Sab']!="":
                Minutes_Esp_S_Sab = formulario.cleaned_data['Minutes_Esp_S_Sab']
                print(f'Minutes_Esp_S_Sab {Minutes_Esp_S_Sab}')
                print(type(Minutes_Esp_S_Sab))
            else:
                print("Minutes_Esp_S_Sab nada")
                Minutes_Esp_S_Sab=None
                print(Minutes_Esp_S_Sab)
                print(type(Minutes_Esp_S_Sab))          

            if formulario.cleaned_data['Minutes_Esp_S_Dom']!="":
                Minutes_Esp_S_Dom = formulario.cleaned_data['Minutes_Esp_S_Dom']
                print(f'Minutes_Esp_S_Dom {Minutes_Esp_S_Dom}')
                print(type(Minutes_Esp_S_Dom))
            else:
                print("Minutes_Esp_S_Dom nada")
                Minutes_Esp_S_Dom=None
                print(Minutes_Esp_S_Dom)
                print(type(Minutes_Esp_S_Dom))              

            if especialidad_s == None:
                dia_s = None
                Minutes_Esp_S_Lun = None
                Minutes_Esp_S_Mar = None
                Minutes_Esp_S_Mie = None
                Minutes_Esp_S_Jue = None
                Minutes_Esp_S_Vie = None
                Minutes_Esp_S_Sab = None
                Minutes_Esp_S_Dom = None
            
            id_especialista = Especialista.objects.all().count()+1
            us = nom_com_especialista[:2].lower()
            uar = " ".join(nom_com_especialista.split()[-2:-1]).lower()
            print(f'uar: {uar}')
            io = fecha_nac_especialista[:-6]
            print(io)
            usuario=us+'.'+uar+io
            usuario=unicodedata.normalize('NFKD', usuario)
            usuario=''.join([c for c in usuario if not unicodedata.combining(c)])
            print(f'Usuario: {usuario}')
            contra=rut
            print(contra)
            sena= nom_com_especialista.split()[-1].lower()
            print(sena)
            contrasena=contra+sena
            Reg = {'csrfmiddlewaretoken':csrfmiddlewaretoken,'username':usuario,'password1':contrasena,'password2':contrasena,'email':'lazarino18@gmail.com'}
            q_dict = QueryDict('', mutable=True)
            q_dict.update(Reg)
            formulario = FormRegistrarUsuario(data=q_dict)
            if formulario.is_valid():
                formulario.save()
                user = User.objects.get(username = usuario)
                grupo_Especialistas = Group.objects.get(name='Especialistas') 
                user.groups.add(grupo_Especialistas)
                Usuario_E = User.objects.filter(username=usuario)[0]
                print(Usuario_E)
                print("Usuario Creado")
                Especialista.objects.create(ID_Especialista=id_especialista, Nombre_completo_E=nom_com_especialista, Fecha_de_nacimiento_E=fecha_nac_especialista, Direccion_E=direccion_especialista, Foto_E = foto_e,
                                            Telefono_E=contacto_especialista, ini_con_especialista=fecha_ini_con,fin_con_especialista=fecha_ini_fin,Rut=rut, Sexo=sexo, Especialidad_P=especialidad_p, 
                                            Especialidad_S=especialidad_s, Usuario_E=Usuario_E, Dia_Esp_P=dia_p, Dia_Esp_S = dia_s, Minutes_Esp_P_Lun = Minutes_Esp_P_Lun, Minutes_Esp_P_Mar = Minutes_Esp_P_Mar,
                                            Minutes_Esp_P_Mie = Minutes_Esp_P_Mie, Minutes_Esp_P_Jue = Minutes_Esp_P_Jue, Minutes_Esp_P_Sab = Minutes_Esp_P_Sab, Minutes_Esp_P_Dom = Minutes_Esp_P_Dom,
                                            Minutes_Esp_S_Lun = Minutes_Esp_S_Lun, Minutes_Esp_S_Mar = Minutes_Esp_S_Mar, Minutes_Esp_S_Mie = Minutes_Esp_S_Mie, Minutes_Esp_S_Jue = Minutes_Esp_S_Jue,
                                            Minutes_Esp_S_Vie = Minutes_Esp_S_Vie, Minutes_Esp_S_Sab = Minutes_Esp_S_Sab, Minutes_Esp_S_Dom = Minutes_Esp_S_Dom)
                messages.success(request, "Te has registrado con éxito")
                return render(request, 'admin/admin_Agregar.html', nuevo_emp_form)
            else:
                print(formulario)
                formulario=FormEspecialista()
                messages.error(request, "Error al Agregar")
                return render(request, 'admin/admin_Agregar.html', nuevo_emp_form)
        else:
            formulario=FormEspecialista()
            messages.error(request, "Error al Agregar")

    
    return render(request, 'admin/admin_Agregar.html', nuevo_emp_form)

def agregar_operador(request):
    nuevo_o_form={'formOperador':FormOperador()}
    if request.method=='POST':
        csrfmiddlewaretoken=request.POST['csrfmiddlewaretoken']
        formulario=FormOperador(data=request.POST)
        if formulario.is_valid():
            nombre_O = formulario.cleaned_data['nom_com_operador']
            print(nombre_O)
            rut_o = formulario.cleaned_data['rut']
            print(rut_o)
            sexo_o = formulario.cleaned_data['sexo']
            print(sexo_o)
            email_o = formulario.cleaned_data['email_o']
            print(email_o)
            fecha_nac_operador_o = formulario.cleaned_data['fecha_nac_operador']
            print(fecha_nac_operador_o)
            direccion_operador_o = formulario.cleaned_data['direccion_operador']
            print(direccion_operador_o)
            contacto_operador_o = formulario.cleaned_data['contacto_operador']
            print(contacto_operador_o)
            fecha_ini_con_operador_o = formulario.cleaned_data['fecha_ini_con_operador']
            print(fecha_ini_con_operador_o)
            fecha_fin_con_operador_o = formulario.cleaned_data['fecha_fin_con_operador']
            print(fecha_fin_con_operador_o)
            foto_o = request.FILES['Foto_O']
            id_operador = User.objects.all().count()+1
            us = nombre_O[:2].lower()
            uar = " ".join(nombre_O.split()[-2:-1]).lower()
            io = str(fecha_nac_operador_o)[:-6]
            print(io)
            usuario=us+'.'+uar+io

            contra=rut_o
            print(contra)
            sena= nombre_O.split()[-1].lower()
            print(sena)
            contrasena=contra+sena
            Reg = {'csrfmiddlewaretoken':csrfmiddlewaretoken,'username':usuario,'password1':contrasena,'password2':contrasena,'email':email_o}
            q_dict = QueryDict('', mutable=True)
            q_dict.update(Reg)
            formulario = FormRegistrarUsuario(data=q_dict)
            if formulario.is_valid():
                formulario.save()
                usuario_nom = User.objects.get(username=usuario)
                print(usuario_nom)
                grupo_o = Group.objects.get(name='Operadores')
                usuario_nom.groups.add(grupo_o)
                Usuario_O = User.objects.filter(username=usuario)[0]
                Operador.objects.create(ID_Operador=id_operador, Nombre_completo_O=nombre_O, Rut=rut_o, Sexo=sexo_o,Foto_O=foto_o,
                                        Fecha_de_nacimiento_O=fecha_nac_operador_o, Direccion_O=direccion_operador_o,
                                        Telefono_O=contacto_operador_o, Fecha_de_contrato_O = fecha_ini_con_operador_o,
                                        Fecha_fin_de_contrato_O = fecha_fin_con_operador_o, Usuario_O=Usuario_O)
                return render(request, "Admin/admin_agregar_Operador.html",nuevo_o_form)
            else:
                formulario=FormOperador()
                print("Error formulario isnt valid 2")
            
            
        else:
            formulario=FormOperador()
            print("Error formulario isnt valid")
            
    
    return render(request, "Admin/admin_agregar_Operador.html",nuevo_o_form)

def obtener_especialidades(request, area_medica_id):
    especialidades = Especialidad.objects.filter(Area_Medica_F=area_medica_id)
    options = [(especialidad.pk, str(especialidad)) for especialidad in especialidades]
    return JsonResponse(options, safe=False)

#Views Especialistas

def especialista_Agenda(request):
    form_agenda = {'form_agenda': DateForm()}
    user = User.objects.get(username=request.user.username)
    datos_esp = Especialista.objects.get(Usuario_E=user)

    if request.method=='POST':
        form_enviado = DateForm(request.POST)
        if form_enviado.is_valid(): 
            Fecha = form_enviado.cleaned_data['date']
            print(type(Fecha))
            print(Fecha)
            dia_semana = calendar.day_name[Fecha.weekday()]
            dia_semana_chi = dia_semana.replace('Monday','Lun').replace('Tuesday','Mar').replace('Wednesday','Mie').replace('Thursday','Jue').replace('Friday','Vie').replace('Saturday','Sab').replace('Sunday','Dom')
            dia_semana_com = dia_semana.replace('Monday','Lunes').replace('Tuesday','Martes').replace('Wednesday','Miercoles').replace('Thursday','Jueves').replace('Friday','Viernes').replace('Saturday','Sabado').replace('Sunday','Domingo')

            print(dia_semana_chi)
            print(dia_semana_com)

            usuario = User.objects.get(username = request.user.username)
            Dias_Esp_P = Especialista.objects.get(Usuario_E = usuario).Dia_Esp_P
            Dias_Esp_S = Especialista.objects.get(Usuario_E = usuario).Dia_Esp_S

            Dias_Esp_P_En = str(Dias_Esp_P).replace('Lunes','Monday').replace('Martes','Tuesday').replace('Miercoles','Wednesday').replace('Jueves','Thursday').replace('Viernes','Friday').replace('Sabado','Saturday').replace('Domingo','Sunday')
            Dias_Esp_S_En = str(Dias_Esp_S).replace('Lunes','Monday').replace('Martes','Tuesday').replace('Miercoles','Wednesday').replace('Jueves','Thursday').replace('Viernes','Friday').replace('Sabado','Saturday').replace('Domingo','Sunday')

            Dias_Esp_P = str(Dias_Esp_P).replace(' ','').split(',')
            Dias_Esp_S = str(Dias_Esp_S).replace(' ','').split(',')

            Dias_Esp_P_En = str(Dias_Esp_P_En).replace(' ','').split(',')
            Dias_Esp_S_En = str(Dias_Esp_S_En).replace(' ','').split(',')

            Dias_Esp_Comp = Dias_Esp_P + Dias_Esp_S
            Dias_Esp_Comp_En = Dias_Esp_P_En + Dias_Esp_S_En
            
            Especialistas = Especialista.objects.filter(Usuario_E = usuario)
            ID_Especialista = Especialistas[0].ID_Especialista

            if dia_semana_com in Dias_Esp_P:
                Minutes_Esp_Dinamico = "Minutes_Esp_P_" + dia_semana_chi
                minutos_especialidad = Especialistas[0].__dict__[Minutes_Esp_Dinamico]  
                Especialidad_del_dia = Especialistas[0].Especialidad_P
            if dia_semana_com in Dias_Esp_S:
                Minutes_Esp_Dinamico = "Minutes_Esp_S_" + dia_semana_chi
                minutos_especialidad = Especialistas[0].__dict__[Minutes_Esp_Dinamico]  
                Especialidad_del_dia = Especialistas[0].Especialidad_S
            else:
                print("NOP")

            hoy = date.today()

            # Calcular la fecha dentro de un año
            next_year = hoy + timedelta(days=365)
            print(next_year)

            # Verificar si el año resultante es bisiesto
            if calendar.isleap(next_year.year):
                print("bisiesto")
                # Si es bisiesto, ajustar la fecha al 29 de febrero
                next_year = next_year.replace(month=2, day=29)
            else:
                print("No")
                # Si no es bisiesto, mantener la fecha tal como está
                next_year = next_year.replace(year=next_year.year)

            # Imprimir la fecha resultante
            print(next_year)
            fechas = []
            while hoy <= next_year:
                diasemana = hoy.weekday()
                nombredia = calendar.day_name[diasemana]
                if nombredia in Dias_Esp_Comp_En:
                    fechas.append(hoy)
                hoy += timedelta(days=1)
            if Fecha in fechas:
                print(f'Fecha estaba en fechas')
                fecha_ini = datetime.combine(Fecha, time(hour=8, minute=0))
                hora_ini = fecha_ini.hour
                print(hora_ini)
                fecha_fin = datetime.combine(Fecha, time(hour=21, minute=0))
                hora_fin = fecha_fin.hour
                print(hora_fin)
                list_horas = []
                while fecha_ini.hour < hora_fin:
                    list_horas.append(fecha_ini.strftime('%H:%M:%S'))
                    fecha_ini = fecha_ini + timedelta(minutes=minutos_especialidad)
                print(list_horas)
                Citas_Reservadas = Cita.objects.filter(ID_Especialista=ID_Especialista,Fecha_Cita=Fecha)
                list_Citas_Reservadas = []
                for x in Citas_Reservadas:
                    list_Citas_Reservadas.append(x.Hora_Cita.split(' ')[-1])
                    print("Hora_Cita")
                    print(x.Hora_Cita)
                print(list_Citas_Reservadas)
                Fecha = Fecha.strftime('%d/%m/%Y')
                url = reverse('agenda_dia') + '?list_horas={}&list_Citas_Reservadas={}&fecha_Elegida={}&esp_Del_Dia={}'.format(
                list_horas, list_Citas_Reservadas, Fecha, Especialidad_del_dia)

                if len(list_Citas_Reservadas) == 0:
                    messages.error(request, "No existe ninguna cita agendada en la fecha seleccionada")
                    return render(request,  "Especialistas/especialista_Agenda.html", form_agenda)
                else:
                    
                    return redirect(url)
            else:
                messages.error(request, "Ingrese una fecha en los dias: "+str(Dias_Esp_Comp).replace('[','').replace(']','').replace("'","")+".")
                print('ESTOY EN EL ELSE')
                return render(request,  "Especialistas/especialista_Agenda.html", form_agenda)
    return render(request, "Especialistas/especialista_Agenda.html", form_agenda)

def especialista_list_citas(request):
    list_horas = request.GET.get('list_horas').replace("'","").replace("[","").replace("]","").split(', ')
    list_Citas_Reservadas = request.GET.get('list_Citas_Reservadas')
    fecha_Elegida = request.GET.get('fecha_Elegida')
    esp_Del_Dia = request.GET.get('esp_Del_Dia')

    print(f'list_horas: {list_horas}')
    print(type(list_horas))
    print(f'list_Citas_Reservadas: {list_Citas_Reservadas}')
    print(type(list_Citas_Reservadas))
    print(f'fecha_Elegida: {fecha_Elegida}')
    print(type(fecha_Elegida))
    print(f'esp_Del_Dia: {esp_Del_Dia}')
    print(type(esp_Del_Dia))
    list_Real_Horas = []
    nombre_Pacientes = []
    for horas in list_Citas_Reservadas.replace("'","").replace("[","").replace("]","").split(', '):
        ID_Cita = fecha_Elegida +' '+ horas
        ID_Cita = datetime.strptime(ID_Cita,'%d/%m/%Y %H:%M:%S')
        print(ID_Cita)
        print(type(ID_Cita))
        cita_ID_Paciente = Cita.objects.get(ID_Cita = ID_Cita).ID_Cliente
        fecha_El = Cita.objects.get(ID_Cita = ID_Cita).ID_Cita
        nombre_Paciente = Paciente.objects.get(Usuario_P = cita_ID_Paciente).Nombre_Paciente
        nombre_Pacientes.append(nombre_Paciente)
        list_Real_Horas.append(fecha_El)
        print(f'Paciente Lista: {nombre_Pacientes}')
        print(f'Horas reales {list_Real_Horas}')

    list_horas = {'list_horas':list_Real_Horas, 'list_Citas_Reservadas':list_Citas_Reservadas, 'fecha_Elegida':fecha_Elegida, 'esp_Del_Dia':esp_Del_Dia, 'list_Paciente_Nom':nombre_Pacientes}

    return render(request, "Especialistas/agenda_dia.html", list_horas)

#Views Operadores

def select_destinatario(request):
    global destinatario
    todos_Especialistas = Especialista.objects.all()
    filtro = request.GET.get('filtro')
    if filtro:
        todos_Especialistas = todos_Especialistas.filter(Nombre_completo_E__icontains=filtro)

    contexto = {
        'especialistas_filtrados': todos_Especialistas,
    }

    if request.method=='POST':
        destinatario = request.POST['chat_btn']
        print("destinatario")
        print(destinatario)
        return redirect('chat')

    return render(request, "General/select_Destinatario.html", contexto)

def chatsito(request):
    remitente = User.objects.filter(username=request.user.username)
    destinatario_E = Especialista.objects.get(Nombre_completo_E=destinatario)
    print(remitente)
    print(destinatario_E)
    mensajes = Mensaje.objects.filter(Nombre_Remitente=remitente, Nombre_Destinatario=destinatario_E) | Mensaje.objects.filter(Nombre_Remitente=destinatario_E, Nombre_Destinatario=remitente)
    mensajes = mensajes.order_by('fecha')
    return render(request, 'General/chat.html', {'remitente': remitente, 'destinatario': destinatario_E, 'mensajes': mensajes})
    

def listadias(lista,diap,dias):
    for x in diap:
        lista.append(x)

    for x in dias:
        lista.append(x)

    return lista

