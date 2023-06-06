from django.shortcuts import render,redirect
from django.http import HttpResponse, QueryDict, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
from django.contrib import messages
import requests
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
import itertools
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4


# Create your views here.



#Def necesario para cambiar header dependiendo del rol
register = template.Library() 

@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists() 

# Dirección URL de vistas de Clientes

def hello(c):
     # Configura el tamaño de página (A4)
    width, height = A4

    # Crea el objeto Canvas con el tamaño de página
    c = canvas.Canvas("boleta.pdf", pagesize=A4)

    print(height)
    # Dibuja la línea separadora
    line_y = height - 100
    c.line(50, line_y, width - 50, line_y)

    # Dibuja el texto "Boleta" centrado
    c.setFont("Helvetica-Bold", 18)
    text = "Boleta"
    text_width = c.stringWidth(text, "Helvetica-Bold", 18)
    text_x = (width - text_width) / 2
    text_y = line_y - 30
    c.drawString(text_x, text_y, text)

    # Dibuja el cuadro de la boleta
    # box_x1 = 50
    # box_y1 = line_y - 150
    # box_x2 = width - 50
    # box_y2 = line_y - 300
    # c.rect(box_x1, box_y1, box_x2 - box_x1, box_y2 - box_y1)

    #Cuadrado propio
    x1 = width - 250
    y1 = line_y - 50
    x2 = width - 50
    y2 = line_y - 150
    c.rect(x1, y1, x2 - x1, y2 - y1)

    
    
    # Guarda el PDF y cierra el objeto Canvas
    c.showPage()
    c.save()

def index(request):
    fecha = date.today()
    hoy = fecha
    hoy = hoy.strftime("%d de %B").replace('Jan','Enero').replace('February','Febrero').replace('March','Marzo').replace('April','Abril').replace('May','Mayo').replace('June','Junio').replace('July','Julio').replace('August','Agosto').replace('September','Septiembre').replace('October','Octubre').replace('November','Noviembre').replace('December','Diciembre')

    print(fecha)
    
    if request.method == 'POST':
        
        print(f'ESTAMOS EN INDEX')
        valores = request.POST.get('seleccion_ficha')
        print(f'antes del split{valores}')
        valores = valores.split(',')
        print(valores)
        rut = valores[0]
        nom = valores[1]
        fecha = valores[2]
        id_cita = valores[3]
        print(fecha)
        print(f'Valor del Nom: {nom}')
        print(f'Valor del fecha: {fecha}')
        url = reverse('ficha_medica')+"?nom_pac={}&id_fecha={}&rut={}&id_cita={}".format(nom,fecha,rut,id_cita)
        return redirect(url)

    
    if request.user.is_authenticated==True:
        nombre_Usuario = User.objects.get(username=request.user.username)
        Bool_Grupo = nombre_Usuario.groups.filter(name__in=['Especialistas']).exists()
        if Bool_Grupo == True:
            
            print(nombre_Usuario)
            especialista = Especialista.objects.filter(Usuario_E=nombre_Usuario)

        # if Cita.objects.filter(ID_Especialista = especialista[0].ID_Especialista, Fecha_Cita = hoy).exists():
            
            cita_con_usuario = Cita.objects.filter(ID_Especialista = especialista[0].ID_Especialista, Fecha_Cita=fecha)
            cita_sin_usuario = CitaSinUsuario.objects.filter(ID_Especialista = especialista[0].ID_Especialista, Fecha_Cita=fecha)
            hay_cita_con_usuario = cita_con_usuario.exists()
            hay_cita_sin_usuario = cita_sin_usuario.exists()

            lista_agenda=[]
            lista_sin=[]
            if cita_sin_usuario.exists():
                for cita_sin in cita_sin_usuario:
                    rut_cita = cita_sin.Rut_Paciente
                    paciente = Paciente.objects.get(Rut = rut_cita)
                    nombre_com = paciente.Nombre_Paciente
                    nombre = nombre_com.split()
                    nombre_pac = nombre[0]
                    apellido_pac = " ".join(nombre[-2:-1])
                    edad = date.today().year - paciente.Fecha_de_nacimiento_P.year
                    telefono = cita_sin.Telefono_Contacto
                    lista_sin.append({'cita_sin':cita_sin, 'paciente':paciente, 'nombre_com':nombre_com, 'telefono':telefono, 'rut_cita':rut_cita, "edad":edad})
            if cita_con_usuario.exists():
                for cita in cita_con_usuario:
                    paciente = Paciente.objects.get(Usuario_P = cita.ID_Cliente)
                    nombre_com = paciente.Nombre_Paciente
                    nombre = nombre_com.split()
                    nombre_pac = nombre[0]
                    apellido_pac = " ".join(nombre[-2:-1])
                    rut_cita = paciente.Rut
                    edad = date.today().year - paciente.Fecha_de_nacimiento_P.year
                    lista_agenda.append({'cita':cita, 'paciente':paciente,"nombre_pac":nombre_pac,"apellido_pac":apellido_pac, "rut_cita":rut_cita, "edad":edad, "nombre_com":nombre_com})
                    

            # print('ANTES DEL IF')
            # if cita_con_usuario.exists():
            #     print('DENTRO DEL IF')
            #     paciente = Paciente.objects.filter(Usuario_P = cita_con_usuario[0].ID_Cliente)
            #     for cita in cita_con_usuario:
            #         paciente = Paciente.objects.get(Usuario_P = cita.ID_Cliente)
            #         nombre_com = paciente.Nombre_Paciente
            #         nombre = nombre_com.split()
            #         nombre_pac = nombre[0]
            #         apellido_pac =  " ".join(paciente.Nombre_Paciente.split()[-2:-1])
            #         rut_pac = paciente.Rut
            #         edad = paciente.Fecha_de_nacimiento_P
            #         edad = date.today().year - edad.year
            #         lista_agenda.append({'cita':cita, 'paciente':paciente,"nombre_pac":nombre_pac,"apellido_pac":apellido_pac, "rut_pac":rut_pac, "edad":edad, "nombre_com":nombre_com})
                    
            #         nombre_Especialista = especialista[0].Nombre_completo_E
            #         nombre_Especialista = nombre_Especialista.split(' ')
            #         nombre_Especialista = nombre_Especialista[0]+' '+nombre_Especialista[-2]
            #         Especialista_Cont = Especialista.objects.get(Usuario_E=nombre_Usuario)
                
            #     print(lista_agenda)
            # print(f'Comprobando los campos de: {cita_sin_usuario}')
            # if cita_sin_usuario.exists():
            #     for cita_sin in cita_sin_usuario:
            #         rut_cita = cita_sin.Rut_Paciente
                    
            #         nombre_Especialista = especialista[0].Nombre_completo_E
            #         nombre_Especialista = nombre_Especialista.split(' ')
            #         nombre_Especialista = nombre_Especialista[0]+' '+nombre_Especialista[-2]
            #         Especialista_Cont = Especialista.objects.get(Usuario_E=nombre_Usuario)
            #         if Paciente.objects.filter(Rut = rut_cita).exists():
            #             paciente = Paciente.objects.get(Rut = rut_cita)
            #             nombre_com = paciente.Nombre_Paciente
            #             nombre = nombre_com.split()
            #             nombre_pac = nombre[0]
            #             apellido_pac =  " ".join(paciente.Nombre_Paciente.split()[-2:-1])
            #             rut_pac = paciente.Rut
            #             edad = paciente.Fecha_de_nacimiento_P
            #             edad = date.today().year - edad.year
            #             lista_agenda.append({'cita_sin':cita_sin, 'paciente':paciente,"nombre_pac":nombre_pac,"apellido_pac":apellido_pac, "rut_cita":rut_cita, "edad":edad, "nombre_com":nombre_com})
                    
            #         else:   
                        
            #             paciente = None
            #             nombre_com = None
            #             telefono = cita_sin.Telefono_Contacto
            #             lista_agenda.append({'cita_sin':cita_sin, 'rut_cita':rut_cita, 'nombre_com':nombre_com, 'telefono':telefono})

            #     print('Dentro del exists de sin usuario')
                    

                # context = {'Nombre_E':nombre_Especialista,'Especialista_Cont':Especialista_Cont, "hoy":hoy, "cita_con_usuario":cita_con_usuario, "cita_sin_usuario":cita_sin_usuario, "paciente":paciente, "lista_agenda":lista_agenda}
            

            print('ESTOY AQUI AMIGO')
            print(f'Citas con usuario: {cita_con_usuario}')
            print(f'Citas sin usuario: {cita_sin_usuario}')
            # lista_nom_paci=[]
            # lista_rut_pac=[]
            # lista_edad_pac=[]
            # for x in cita_con_usuario:
            #     lista_agenda.append(x.Hora_Cita.split(' ')[-1])
            
            # for x in range(len(lista_agenda)):
            
            nombre_Especialista = especialista[0].Nombre_completo_E
            nombre_Especialista = nombre_Especialista.split(' ')
            nombre_Especialista = nombre_Especialista[0]+' '+nombre_Especialista[-2]
            Especialista_Cont = Especialista.objects.get(Usuario_E=nombre_Usuario)
            print(nombre_Especialista)
            context = {'lista_sin':lista_sin, 'hay_cita_con_usuario':hay_cita_con_usuario, 'hay_cita_sin_usuario':hay_cita_sin_usuario, 'Nombre_E':nombre_Especialista,'Especialista_Cont':Especialista_Cont, "hoy":hoy, "cita_con_usuario":cita_con_usuario, "cita_sin_usuario":cita_sin_usuario, "lista_agenda":lista_agenda}
            return render(request, "Clientes/index.html", context)

        else:
            print("Otro")
            Bool_Grupo = nombre_Usuario.groups.filter(name__in=['Operadores']).exists()
            Bool_Grupo_pac = nombre_Usuario.groups.filter(name__in=['Pacientes']).exists()
            if Bool_Grupo == True:
                print(nombre_Usuario)
                nombre_Operador = Operador.objects.filter(Usuario_O=nombre_Usuario)[0].Nombre_completo_O
                Operador_Cont = Operador.objects.get(Usuario_O=nombre_Usuario)
                nombre_Operador = nombre_Operador.split(' ')
                nombre_Operador = nombre_Operador[0]+' '+nombre_Operador[-2]
                print(nombre_Operador)
                print(Operador_Cont)
                return render(request, "Clientes/index.html", {'Nombre_O':nombre_Operador,'Operador_Cont':Operador_Cont})

            elif Bool_Grupo_pac == True:
                paciente = Paciente.objects.get(Usuario_P=nombre_Usuario)
                if paciente.Primer_Login:
                    print('Estoy aquii aloooo')
                    return redirect('perfil')
                else:
                    return render(request, "Clientes/index.html")
            
            else:
                return render(request, "Clientes/index.html")
        
    else:
        return render(request, "Clientes/index.html")
    
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
            formPac = FormPaciente()
            formPac.save(usuario)
            messages.success(request, "Te has registrado con éxito")
            return redirect('inicioSesion')
        
        else:
            formulario=FormRegistrarUsuario()
            messages.error(request, "Error al registrarte")

    return render(request, 'Clientes/registro.html', formulario1)

def perfil_cliente(request):
    id_cita =request.GET.get('id_cita')
    rut = request.GET.get('rut')
    id_fecha = request.GET.get('id_fecha')
    telefono = request.GET.get('telefono')
    print(f'Rut desde ficha: {rut}')
    datos_form = {'rut_pac':rut, 'telefono_pac':telefono}
    formulario_pac = {'formulario_pac': FormPaciente(initial = datos_form), 'id_cita':id_cita}
    if rut is None:
        print('Estoy dentro del rut is None')
        if request.method=='POST':
            print('Metodo post del is None')
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
                print('Else del POST sin rut')
                formulario_pac = FormPaciente()
                messages.error(request, "Error")
    else:      
        if request.method=='POST':
            print(f'dentro del request post de rut')
            
            if id_cita is None:
                formulario_pac = FormPaciente(data = request.POST)
                csrfmiddlewaretoken=request.POST['csrfmiddlewaretoken']
                if formulario_pac.is_valid():
                    nombre_pac = formulario_pac.cleaned_data['nom_com_pac']
                    rut_pac = formulario_pac.cleaned_data['rut_pac']
                    sexo_pac = formulario_pac.cleaned_data['sexo_pac']
                    fecha_nac_pac = formulario_pac.cleaned_data['fecha_nac_pac']
                    direccion_pac = formulario_pac.cleaned_data['direccion_pac']
                    telefono_pac = formulario_pac.cleaned_data['telefono_pac']
                    first_login = False
                    
                    us = nombre_pac[:2].lower()
                    uar = " ".join(nombre_pac.split()[2:3]).lower()
                    print(f'uar: {uar}')
                    io = str(fecha_nac_pac.year)
                    print(io)
                    usuario=us+'.'+uar+io
                    usuario=unicodedata.normalize('NFKD', usuario)
                    usuario=''.join([c for c in usuario if not unicodedata.combining(c)])
                    print(f'Usuario: {usuario}')
                    contra=rut
                    print(contra)
                    sena= nombre_pac.split()[-1].lower()
                    print(sena)
                    contrasena=contra+sena
                    Reg = {'csrfmiddlewaretoken':csrfmiddlewaretoken,'username':usuario,'password1':contrasena,'password2':contrasena,'email':'lazarino18@gmail.com'}
                    q_dict = QueryDict('', mutable=True)
                    q_dict.update(Reg)
                    formulario = FormRegistrarUsuario(data=q_dict)
                    if formulario.is_valid():
                        formulario.save()
                        user = User.objects.get(username = usuario)
                        grupo_Pacientes = Group.objects.get(name='Pacientes')
                        user.groups.add(grupo_Pacientes)
                        usuario = User.objects.filter(username=usuario)[0]
                        formPac = FormPaciente()
                        formPac.save(usuario)
                        Paciente.objects.filter(Usuario_P = usuario).update(Nombre_Paciente = nombre_pac, Rut=rut_pac,Sexo=sexo_pac,Fecha_de_nacimiento_P=fecha_nac_pac,Direccion_P=direccion_pac,Telefono_P=telefono_pac,Primer_Login=first_login)
                        
                        usuario_operador = request.user
                        validar_usuario = User.objects.get(username = usuario_operador)
                        messages.success(request, "Exito al actualizar")
                        if validar_usuario.groups.filter(name='Operadores'):
                            url = reverse('index')
                            return redirect(url)
                        else:
                            url = reverse('ficha_medica') + '?nom_pac={}&id_fecha={}&rut={}'.format(nombre_pac,id_fecha,rut)
                            return redirect(url)
                else:
                    print('Else del POST con rut')
                    formulario_pac = FormPaciente(initial = datos_form)
                    messages.error(request, "Error")
            else:
                formulario_pac = FormPaciente(data = request.POST)
                csrfmiddlewaretoken=request.POST['csrfmiddlewaretoken']
                if formulario_pac.is_valid():
                    nombre_pac = formulario_pac.cleaned_data['nom_com_pac']
                    rut_pac = formulario_pac.cleaned_data['rut_pac']
                    sexo_pac = formulario_pac.cleaned_data['sexo_pac']
                    fecha_nac_pac = formulario_pac.cleaned_data['fecha_nac_pac']
                    direccion_pac = formulario_pac.cleaned_data['direccion_pac']
                    telefono_pac = formulario_pac.cleaned_data['telefono_pac']
                    first_login = False

                    us = nombre_pac[:2].lower()
                    uar = " ".join(nombre_pac.split()[2:3]).lower()
                    print(f'uar: {uar}')
                    io = str(fecha_nac_pac.year)
                    print(io)
                    usuario=us+'.'+uar+io
                    usuario=unicodedata.normalize('NFKD', usuario)
                    usuario=''.join([c for c in usuario if not unicodedata.combining(c)])
                    print(f'Usuario: {usuario}')
                    contra=rut
                    print(contra)
                    sena= nombre_pac.split()[-1].lower()
                    print(sena)
                    contrasena=contra+sena
                    Reg = {'csrfmiddlewaretoken':csrfmiddlewaretoken,'username':usuario,'password1':contrasena,'password2':contrasena,'email':'lazarino18@gmail.com'}
                    q_dict = QueryDict('', mutable=True)
                    q_dict.update(Reg)
                    formulario = FormRegistrarUsuario(data=q_dict)
                    if formulario.is_valid():
                        formulario.save()
                        user = User.objects.get(username = usuario)
                        grupo_Pacientes = Group.objects.get(name='Pacientes')
                        user.groups.add(grupo_Pacientes)
                        usuario = User.objects.filter(username=usuario)[0]
                        formPac = FormPaciente()
                        formPac.save(usuario)
                        Paciente.objects.filter(Usuario_P = usuario).update(Nombre_Paciente = nombre_pac, Rut=rut_pac,Sexo=sexo_pac,Fecha_de_nacimiento_P=fecha_nac_pac,Direccion_P=direccion_pac,Telefono_P=telefono_pac,Primer_Login=first_login)
                        messages.success(request, "Exito al actualizar")
                        url = reverse('ficha_medica') + '?nom_pac={}&id_fecha={}&rut={}'.format(nombre_pac,id_fecha,rut)
                        return redirect(url)
                else:
                    print('Else del POST con rut')
                    formulario_pac = FormPaciente(initial = datos_form)
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
        metodo = None  # Declarar la variable metodo
        if 'ver_especialista' in request.POST:
            metodo = request.POST.get('metodo_pago')
            request.session['metodo'] = metodo
            print(f'metodo de pago en el post: {metodo}')
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

            qspecialista = {'qspecialista':qspecialista, 'qsListaEspecialidad':qsListaEspecialidad,'especialidad_select':especialidad_select, 'metodo': metodo}

            return render(request, 'Clientes/listar_Especialistas.html', qspecialista)
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

            fechas = dias_trabaja_especialista(dias_en)
            dataformDate = {
                'formDate': DateForm(),
                'fechas': fechas,
                'metodo': metodo
            }

            return render(request, 'Clientes/cliente_Seleccionar_Fecha.html', dataformDate)    
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
                    Citas_Sin_usuario = CitaSinUsuario.objects.filter(ID_Especialista=ID_Especialista,Fecha_Cita=Fecha)
                    list_Citas_Reservadas = []
                    for x in Citas_Reservadas:
                        list_Citas_Reservadas.append(x.Hora_Cita.split(' ')[-1])
                        print("Hora_Cita")
                        print(x.Hora_Cita)
                    for y in Citas_Sin_usuario:
                        list_Citas_Reservadas.append(y.Hora_Cita.split(' ')[-1])
                        print("Hora_Cita")
                        print(y.Hora_Cita)

                    print(list_Citas_Reservadas)
                    list_horas = {'list_horas':list_horas, 'list_Citas_Reservadas':list_Citas_Reservadas , 'metodo': metodo}
                    return render(request, 'Clientes/cliente_Seleccionar_Hora.html', list_horas)
                else:
                    messages.error(request, "Ingrese una fecha en los dias: "+dias_es+".")
                    return render(request, 'Clientes/cliente_Seleccionar_Fecha.html',dataformDate)
        #Si pulsa el botón de seleccionar hora
        if 'hora_seleccionada' in request.POST:
            print("Hora Seleccionada")
            Usuario = User.objects.get(username=request.user.username)
            username = Usuario
            Mail = Usuario.email
            print("Usuario:\n")
            print(Usuario)
            print("Mail:\n")
            print(Mail)
            hora_seleccionada = request.POST.get('hora_seleccionada')
            print("hora seleccionada")
            print(hora_seleccionada)
            print(Fecha)
            
            feccha_id = str(Fecha)+str(' '+hora_seleccionada)

            print(hora_seleccionada)
            print("ID_Especialistas:\n")
            print(Especialistas[0])
            Citas_Usuario = Cita.objects.filter(Fecha_Cita=Fecha, ID_Cliente = username).count()
            print("Deberia entrar al for")
            print(Citas_Usuario)
            cita_existe = Cita.objects.filter(ID_Cita = feccha_id).exists()
            metodo = request.session.get('metodo')
            print(f'metodo de pago Antes de agregar la cita: {metodo}')
            if cita_existe:
                messages.error(request, "La cita seleccionada ya ha sido reservada")
                return render(request, 'Clientes/cliente_Seleccionar_Fecha.html', dataformDate)
            else:
                if Citas_Usuario<3:
                    Cita.objects.create(ID_Cita=feccha_id,Fecha_Cita=Fecha, Hora_Cita=hora_seleccionada, ID_Cliente=Usuario, ID_Especialista=Especialistas[0], Metodo_Pago_Cita= metodo)
                    messages.success(request, "Hora creada con éxito")
                    """
                    send_mail(
                        'Cita programada con éxito',
                        'Su cita con el especialista '+str(Especialistas[0])+' programada para la fecha: '+str(Fecha)+' a las '+str(hora_seleccionada)+' ha sido programada con éxito',
                        'settings.EMAIL_HOST_USER',
                        [Mail]  
                    )
                    """
                    return render(request, 'Clientes/cliente_Hora_creada.html', {'fecha':Fecha, 'valor':hora_seleccionada})
                else:
                    messages.error(request, "Ha alcanzado el máximo de citas solicitadas en esta fecha: 3.")
                    return render(request, 'Clientes/cliente_Seleccionar_Fecha.html', dataformDate)
    return render(request, 'Clientes/cliente_Agendar_Hora.html', formulario_area_medica)

def dias_trabaja_especialista(dias_en):
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

    return fechas

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
        return render(request, 'Clientes/cliente_Hora_anulada.html', {'hora_principal':Anular_Hora_Principal})
    if request.user.is_authenticated:
        Usuario = User.objects.get(username=request.user.username)
        citas_cliente = Cita.objects.filter(ID_Cliente=Usuario)
        
        return render(request, 'Clientes/cliente_Anular_Hora.html', {'citas_cliente':citas_cliente})
    else:
        return render(request, 'Clientes/cliente_Anular_Hora.html')    

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
        return render(request, 'Clientes/cliente_Confirmar_Hora.html', {'cita_seleccionada':Cita_Seleccionada})
    if request.user.is_authenticated:
        Usuario = User.objects.get(username=request.user.username)
        citas_cliente = Cita.objects.filter(ID_Cliente=Usuario)
        
        return render(request, 'Clientes/cliente_Consultar_Cita.html', {'citas_cliente':citas_cliente})
    else:
        return render(request, 'Clientes/cliente_Consultar_Cita.html')
#Views admin
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
                                            Minutes_Esp_P_Mie = Minutes_Esp_P_Mie, Minutes_Esp_P_Jue = Minutes_Esp_P_Jue, Minutes_Esp_P_Vie = Minutes_Esp_P_Vie, Minutes_Esp_P_Sab = Minutes_Esp_P_Sab, Minutes_Esp_P_Dom = Minutes_Esp_P_Dom,
                                            Minutes_Esp_S_Lun = Minutes_Esp_S_Lun, Minutes_Esp_S_Mar = Minutes_Esp_S_Mar, Minutes_Esp_S_Mie = Minutes_Esp_S_Mie, Minutes_Esp_S_Jue = Minutes_Esp_S_Jue,
                                            Minutes_Esp_S_Vie = Minutes_Esp_S_Vie, Minutes_Esp_S_Sab = Minutes_Esp_S_Sab, Minutes_Esp_S_Dom = Minutes_Esp_S_Dom)
                
                esp = Especialista.objects.get(ID_Especialista=id_especialista)
                print(esp)
                Reg2 = {'id_especialista':esp}
                q_dict2 = QueryDict('', mutable=True)
                q_dict2.update(Reg2)
                formulario2 = FormRegistrarCobros(data=q_dict2)
                if formulario2.is_valid():
                    print('Estoy dentro del formulario2 ')
                    formulario2.save()
                
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

def admin_Eliminar_Especialista(request):
    if request.method == 'POST':
        if 'conf_delet_cit' in request.POST:
            ID_Esp_del = request.POST.get('conf_delet_cit')
            print("MANUEEEH")
            print(ID_Esp_del)
            print(type(ID_Esp_del))
            Especialista_Del = Especialista.objects.get(ID_Especialista = ID_Esp_del)
            Usuario_Del = User.objects.get(username = Especialista_Del.Usuario_E)
            Especialista_Del.delete()
            Usuario_Del.delete()
            messages.success(request,"¡Especialista eliminado con éxito!")
            
    Especialistas_All = Especialista.objects.all()
    contexto = {'Especialistas_All':Especialistas_All}
    return render(request, 'admin/admin_Eliminar_Especialista.html', contexto)

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
            foto_o = request.FILES['foto_o']
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
                usuario_nom = User.objects.get(username = usuario)
                print(usuario_nom)
                grupo_o = Group.objects.get(name='Operadores')
                usuario_nom.groups.add(grupo_o)
                Usuario_O = User.objects.filter(username=usuario)[0]
                Operador.objects.create(ID_Operador=id_operador, Nombre_completo_O=nombre_O, Rut=rut_o, Sexo=sexo_o,Foto_O=foto_o,
                                        Fecha_de_nacimiento_O=fecha_nac_operador_o, Direccion_O=direccion_operador_o,
                                        Telefono_O=contacto_operador_o, Fecha_de_contrato_O = fecha_ini_con_operador_o,
                                        Fecha_fin_de_contrato_O = fecha_fin_con_operador_o, Usuario_O=Usuario_O)
                messages.success(request, "¡Operador registrado exitosamente!")
                return render(request, "admin/admin_agregar_Operador.html",nuevo_o_form)
            else:
                formulario=FormOperador()
                print("Error formulario isnt valid 2")
            
            
        else:
            formulario=FormOperador()
            print("Error formulario isnt valid")
            
    
    return render(request, "admin/admin_agregar_Operador.html",nuevo_o_form)

def admin_Eliminar_Operador(request):
    if request.method == 'POST':
        if 'conf_delet_cit' in request.POST:
            ID_Ope_del = request.POST.get('conf_delet_cit')
            print(ID_Ope_del)
            print(type(ID_Ope_del))
            Operador_Del = Operador.objects.get(ID_Operador = ID_Ope_del)
            Usuario_Del = User.objects.get(username = Operador_Del.Usuario_O)
            Operador_Del.delete()
            Usuario_Del.delete()
            messages.success(request,"¡Operador eliminado con éxito!")
            
    Operadores_All = Operador.objects.all()
    contexto = {'Operadores_All':Operadores_All}
    return render(request, 'admin/admin_Eliminar_Operador.html', contexto)

def obtener_especialidades(request, area_medica_id):
    especialidades = Especialidad.objects.filter(Area_Medica_F=area_medica_id)
    options = [(especialidad.pk, str(especialidad)) for especialidad in especialidades]
    return JsonResponse(options, safe=False)

def admin_Agregar_Especialidad(request):
    if request.method=='POST':
        formulario=FormEspecialidad(data=request.POST)
        print(formulario)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "¡Especialidad creada con éxito!")
            return redirect('index')

    formulario = FormEspecialidad()
    contexto = {'FormEspecialidad':formulario}
    return render(request, 'admin/admin_agregar_Especialidad.html', contexto)

def admin_Eliminar_Especialidad(request):
    if request.method == 'POST':
        if 'conf_delet_cit' in request.POST:
            ID_Esp_del = request.POST.get('conf_delet_cit')
            print("MANUEEEH")
            print(ID_Esp_del)
            print(type(ID_Esp_del))
            Esp_del = Especialidad.objects.get(Codigo_especialidad = ID_Esp_del)
            Esp_del.delete()
            messages.success(request,"¡Especialidad eliminada con éxito!")
            
    Especialidades_All = Especialidad.objects.all()
    contexto = {'Especialidades_All':Especialidades_All}
    return render(request, 'admin/admin_Eliminar_Especialidad.html', contexto)
#Views Especialistas
def especialista_Agenda(request):
    form_agenda = {'form_agenda': DateForm()}

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


            fechas = dias_trabaja_especialista(Dias_Esp_Comp_En)
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

def dias_minutos_especialidad(dia_seleccionado, dias_str, dias_especialista, fecha, id_especialista):
    if dia_seleccionado in dias_str:
        dia_seleccionado = dia_seleccionado.replace('lun','Lun').replace('mar','Mar').replace('mie','Mie').replace('jue','Jue').replace('vie','Vie').replace('sab','Sab').replace('dom','Dom')
        Minutes_Esp_Dinamico = "Minutes_Esp_P_" + dia_seleccionado
        minutos_esp = dias_especialista[0].__dict__[Minutes_Esp_Dinamico]
        especialidad = dias_especialista[0].Especialidad_P
        print(f'Especialidad_P: {especialidad}')
        print(f'Especialidad_P minutos_esp: {minutos_esp}')
    else:
        dia_seleccionado = dia_seleccionado.replace('lun','Lun').replace('mar','Mar').replace('mie','Mie').replace('jue','Jue').replace('vie','Vie').replace('sab','Sab').replace('dom','Dom')
        Minutes_Esp_Dinamico = "Minutes_Esp_S_" + dia_seleccionado
        minutos_esp = dias_especialista[0].__dict__[Minutes_Esp_Dinamico]
        especialidad = dias_especialista[0].Especialidad_S
        print(f'Especialidad_S: {especialidad}')
    fecha_ini = datetime.combine(fecha, time(hour=8, minute=0))
    hora_ini = fecha_ini.hour
    print(hora_ini)
    fecha_fin = datetime.combine(fecha, time(hour=21, minute=0))
    hora_fin = fecha_fin.hour
    print(hora_fin)
    list_horas = []
    while fecha_ini.hour < hora_fin:
        list_horas.append(fecha_ini.strftime('%H:%M:%S'))
        fecha_ini = fecha_ini + timedelta(minutes=minutos_esp)
    print(list_horas)
    Citas_Reservadas = Cita.objects.filter(ID_Especialista=id_especialista,Fecha_Cita=fecha)
    Citas_Sin_usuario = CitaSinUsuario.objects.filter(ID_Especialista=id_especialista,Fecha_Cita=fecha)
    list_Citas_Reservadas = []
    for x in itertools.chain(Citas_Reservadas, Citas_Sin_usuario):
        list_Citas_Reservadas.append(x.Hora_Cita.split(' ')[-1])
        print("Hora_Cita")
        print(x.Hora_Cita)

    return list_horas, list_Citas_Reservadas, especialidad

def especialista_list_citas(request):
    # Si la solicitud es de tipo POST, verificar si se ha enviado una solicitud para eliminar una cita o para ver la ficha médica de un paciente
    if request.method == 'POST':
        if 'doc_pac' in request.POST:
            # Si se ha solicitado la ficha médica de un paciente, obtener el nombre del paciente y redirigir a la página de ficha médica
            nom_pac = request.POST.get('doc_pac')
            paciente = Paciente.objects.get(Nombre_Paciente = nom_pac)
            url = reverse('ficha_medica') + '?nom_pac={}'.format(nom_pac)
            return redirect(url)
        if 'conf_delet_cit' in request.POST:
            # Si se ha solicitado eliminar una cita, obtener la fecha y hora de la cita y eliminarla de la base de datos
            ID_Cita_del = request.POST.get('conf_delet_cit').split(' ')
            Ndia = ID_Cita_del[0]
            Mes = ID_Cita_del[2].replace('Enero','01').replace('Febrero','02').replace('Marzo','03').replace('Abril','04').replace('Mayo','05').replace('Junio','06').replace('Julio','07').replace('Agosto','08').replace('Septiembre','09').replace('Octubre','10').replace('Noviembre','11').replace('Diciembre','12')
            Anno = ID_Cita_del[4]
            Hora = ID_Cita_del[7]
            # Formatear la fecha y hora de la cita en un formato adecuado para eliminarla de la base de datos
            ID_Cita_del = Ndia+'/'+Mes+'/'+Anno+' '+Hora
            ID_Cita_del = datetime.strptime(ID_Cita_del,'%d/%m/%Y %H:%M')
            # Eliminar la cita de la base de datos
            Cita.objects.get(ID_Cita = ID_Cita_del).delete()
            # Mostrar un mensaje de éxito y redirigir a la página de agenda del especialista
            messages.success(request, "Hora anulada con éxito")
            return redirect('agenda_especialista')
    # Si la solicitud no es de tipo POST, obtener la información de la agenda del especialista a partir de los parámetros de la solicitud
    list_horas = request.GET.get('list_horas').replace("'","").replace("[","").replace("]","").split(', ')
    list_Citas_Reservadas = request.GET.get('list_Citas_Reservadas').replace("'","").replace("[","").replace("]","").split(', ')
    fecha_Elegida = request.GET.get('fecha_Elegida')
    esp_Del_Dia = request.GET.get('esp_Del_Dia').replace("'","").replace("[","").replace("]","").split(', ')
    list_Real_Horas = []
    nombre_Pacientes = []
    list_Citas_Agen = []

    # Para cada cita reservada, obtener información como el nombre del paciente y la hora de la cita
    for i in range(len(list_Citas_Reservadas)):
        horas = list_Citas_Reservadas[i]
        ID_Cita = fecha_Elegida +' '+ horas
        ID_Cita = datetime.strptime(ID_Cita,'%d/%m/%Y %H:%M:%S')
        cita_ID_Paciente = Cita.objects.get(ID_Cita = ID_Cita).ID_Cliente
        fecha_El = Cita.objects.get(ID_Cita = ID_Cita).ID_Cita
        nombre_Paciente = Paciente.objects.get(Usuario_P = cita_ID_Paciente).Nombre_Paciente
        nombre_Pacientes.append(nombre_Paciente)
        list_Real_Horas.append(fecha_El)
        for j in range(len(esp_Del_Dia)):
            esp = esp_Del_Dia[j]
        list_Citas_Agen.append([fecha_El,nombre_Paciente,esp])

    #Ordenar Citas obtenidas en orden de fecha.
    list_Citas_Agen = sorted(list_Citas_Agen, key=lambda cita: cita[0])
    #Crear contexto para poder usarlo en template
    list_horas = {'list_Citas_Reservadas':list_Citas_Agen}
    #Renderizar template con su contexto respectivo
    return render(request, "Especialistas/agenda_dia.html", list_horas)

def list_ficha_medica(request):
    nombre_pac = request.GET.get('nom_pac')
    id_fecha = request.GET.get('id_fecha')
    rut = request.GET.get('rut')
    id_cita = request.GET.get('id_cita')
    print(f'Valor del id_fecha {id_fecha}')
    print(f'Nombre en la lista ficha {nombre_pac}')
    if request.method == 'POST':  # Si se recibe una solicitud POST
        if 'red_form_ficha_med' in request.POST:  # Si el botón 'red_form_ficha_med' está presente en la solicitud POST
            url = reverse('crear_ficha_medica') + '?nombre_pac={}&rut={}&id_fecha={}'.format(nombre_pac,rut,id_fecha)
            return redirect(url) # Redirige al usuario a la página 'crear_ficha_medica'
        if 'agregar_cita_medica' in request.POST:  # Si el botón 'agregar_cita_medica' está presente en la solicitud POST
            # Obtiene los datos necesarios de la solicitud POST
            datos_list = request.POST.get('agregar_cita_medica').split(',')
            Ficha_Medica_Pac = datos_list[0]
            RUT_Pac = datos_list[1]
            Nombre_Com_Pac = datos_list[2]
            # Crea la URL para agregar una cita médica y redirige al usuario a ella
            url = reverse('agregar_cita_medica') + '?Ficha_Medica_Pac={}&RUT_Pac={}&Nombre_Com_Pac={}&id_fecha={}&id_cita={}'.format(
                Ficha_Medica_Pac, RUT_Pac, Nombre_Com_Pac,id_fecha,id_cita)
            return redirect(url)
        if 'ver_cita_medica' in request.POST:
            ID_Ficha_Cita = request.POST.get('ver_cita_medica')
            print(ID_Ficha_Cita)
            url = reverse('ver_cita_medica') + '?ID_Ficha_Cita={}&nombre_pac={}'.format(ID_Ficha_Cita,nombre_pac)
            return redirect(url)
        if 'ver_receta' in request.POST:
            receta = request.POST.get('ver_receta')
            print(f'Numero de receta en ver receta: {receta}')
            url = reverse('receta_medica') + '?receta={}'.format(receta)
            return redirect(url)
        if 'ver_examen' in request.POST:
            orden = request.POST.get('ver_examen')
            print(f'Numero de receta en ver orden: {orden}')
            url = reverse('orden_examen') + '?orden={}'.format(orden)
            return redirect(url)
        if 'ver_ficha_medica' in request.POST:
            ID_Ficha_Medica = request.POST.get('ver_ficha_medica')
            print(ID_Ficha_Medica)
            url = reverse('ver_ficha_medica') + '?ID_Ficha_Medica={}'.format(ID_Ficha_Medica)
            return redirect(url)
        
    else:   
        nom_pac = request.GET.get('nom_pac')  # Obtiene el valor de la variable 'nom_pac' de la solicitud GET
        print(f'Nom paciente: {nom_pac}')
        if Paciente.objects.filter(Nombre_Paciente = nom_pac).exists():
            rut_pac = Paciente.objects.get(Nombre_Paciente = nom_pac).Rut  # Obtiene el Rut del paciente correspondiente al nombre obtenido en la solicitud GET
        else:
            rut_pac = request.GET.get('rut')
        # Si existe una ficha médica asociada al paciente
        if Ficha_Medica.objects.filter(RUT_Pac = rut_pac).exists():
            Ficha_Med_Pac = Ficha_Medica.objects.get(RUT_Pac = rut_pac)  # Obtiene la ficha médica asociada al paciente
            # Si existen citas médicas asociadas al paciente
            if Ficha_Cita.objects.filter(RUT_Pac = rut_pac).exists():
                Citas_medicas = Ficha_Cita.objects.filter(RUT_Pac = rut_pac)  # Obtiene las citas médicas asociadas al paciente
                contexto = {'Ficha_Med_Pac':Ficha_Med_Pac, 'QSCitasMedicas':Citas_medicas}  # Crea un diccionario con la información de la ficha médica y las citas médicas
                return render(request,"Especialistas/ficha_medica.html", contexto)  # Renderiza la plantilla HTML 'ficha_medica.html' con el contexto creado
            else:
                print("Ficha Cita no existe")  # Si no existen citas médicas asociadas al paciente, imprime un mensaje de error en la consola
                contexto = {'Ficha_Med_Pac':Ficha_Med_Pac,'texto_FMP':'No hay atenciones anteriores para '+nom_pac+'.'}  # Crea un diccionario con la información de la ficha médica y un mensaje de error
                return render(request,"Especialistas/ficha_medica.html", contexto)  # Renderiza la plantilla HTML 'ficha_medica.html' con el contexto creado
        else:
            print("Ficha medica no existe")
            contexto = {'texto':'No hay ficha médica registrada para '+nom_pac+'.'}
            return render(request, "Especialistas/ficha_medica.html", contexto)

def filtro_ficha_medica(request):
    nom_pac = request.GET.get('nom_pac')  # Obtiene el valor de la variable 'nom_pac' de la solicitud GET
    print(f'Nom paciente: {nom_pac}')
    
    if request.method =='POST':
        if 'ver_cita_medica' in request.POST:
            ID_Ficha_Cita = request.POST.get('ver_cita_medica')
            print(ID_Ficha_Cita)
            url = reverse('ver_cita_medica') + '?ID_Ficha_Cita={}&nombre_pac={}'.format(ID_Ficha_Cita,nom_pac)
            return redirect(url)
        if 'ver_ficha_medica' in request.POST:
            ID_Ficha_Medica = request.POST.get('ver_ficha_medica')
            url = reverse('ver_ficha_medica') + '?ID_Ficha_Medica={}'.format(ID_Ficha_Medica)
            return redirect(url)
        if 'ver_receta' in request.POST:
            receta = request.POST.get('ver_receta')
            print(f'Numero de receta en ver receta: {receta}')
            url = reverse('receta_medica') + '?receta={}'.format(receta)
            return redirect(url)
        if 'ver_examen' in request.POST:
            orden = request.POST.get('ver_examen')
            print(f'Numero de receta en ver orden: {orden}')
            url = reverse('orden_examen') + '?orden={}'.format(orden)
            return redirect(url)
        
    if Paciente.objects.filter(Nombre_Paciente = nom_pac).exists():
        rut_pac = Paciente.objects.get(Nombre_Paciente = nom_pac).Rut  # Obtiene el Rut del paciente correspondiente al nombre obtenido en la solicitud GET
    else:
        rut_pac = request.GET.get('rut')
    # Si existe una ficha médica asociada al paciente
    if Ficha_Medica.objects.filter(RUT_Pac = rut_pac).exists():
        Ficha_Med_Pac = Ficha_Medica.objects.get(RUT_Pac = rut_pac)  # Obtiene la ficha médica asociada al paciente
        # Si existen citas médicas asociadas al paciente
        if Ficha_Cita.objects.filter(RUT_Pac = rut_pac).exists():
            Citas_medicas = Ficha_Cita.objects.filter(RUT_Pac = rut_pac)  # Obtiene las citas médicas asociadas al paciente
            contexto = {'Ficha_Med_Pac':Ficha_Med_Pac, 'QSCitasMedicas':Citas_medicas}  # Crea un diccionario con la información de la ficha médica y las citas médicas
            return render(request,"Especialistas/ver_ficha.html", contexto)  # Renderiza la plantilla HTML 'ver_ficha.html' con el contexto creado
        else:
            print("Ficha Cita no existe")  # Si no existen citas médicas asociadas al paciente, imprime un mensaje de error en la consola
            contexto = {'Ficha_Med_Pac':Ficha_Med_Pac,'texto_FMP':'No hay atenciones anteriores para '+nom_pac+'.'}  # Crea un diccionario con la información de la ficha médica y un mensaje de error
            return render(request,"Especialistas/ver_ficha.html", contexto)  # Renderiza la plantilla HTML 'ver_ficha.html' con el contexto creado
    else:
        print("Ficha medica no existe")
        contexto = {'texto':'No hay ficha médica registrada para '+nom_pac+'.'}
        return render(request, "Especialistas/ver_ficha.html", contexto)

#TODO AGREGAR TRASPASAR VALORES A LA NUEVA VISTA DE RECETA MEDICA Y ORDENES EXAMENES
def agregar_cita_medica(request):
    id_fecha = request.GET.get('id_fecha')
    id_ficha = request.GET.get('id_ficha')
    id_cita = request.GET.get('id_cita')
    nom_pac = request.GET.get('nom_pac')
    Nombre_Com_Pac = request.GET.get('Nombre_Com_Pac')
    diagnostico = request.GET.get('diagnostico')

    print(f'Valores de los get id_fecha: {id_fecha}')
    print(f'Valores de los get id_ficha: {id_ficha}')
    print(f'Valores de los get id_cita: {id_cita}')
    print(f'Valores de los get nom_pac: {nom_pac}')
    print(f'Valores de los get Nombre_Com_Pac: {Nombre_Com_Pac}')
    print(f'Valores de los get diagnostico: {diagnostico}')
    if id_ficha is not None:
        if 'ver_receta' in request.POST:
            values = request.POST.get('ver_receta')
            print(values)
            datos_orden = values.split(',')
            print(datos_orden)
            receta = datos_orden[0]
            ficha = datos_orden[1]
            url = reverse('receta_medica') + '?receta={}&Ficha_Medica_Pac={}'.format(receta,ficha)
            return redirect(url)
        if 'ver_examen' in request.POST:
            values = request.POST.get('ver_examen')
            datos_orden = values.split(',')
            print(values)
            print(datos_orden)
            orden = datos_orden[0]
            ficha = datos_orden[1]
            url = reverse('orden_examen') + '?orden={}&Ficha_Medica_Pac={}'.format(orden,ficha)
            return redirect(url)
        if 'Receta' in request.POST:
            print(f'Receta agregar_cita_medica if POST')
            Nombre_Com_Pac = request.POST.get('Nombre_Com_Pac')
            url =  reverse('receta_medica') + '?nom_pac={}&id_fecha={}&id_ficha={}&diagnostico={}'.format(nom_pac,id_fecha,id_ficha,diagnostico)
            return redirect(url)
        if 'Examen' in request.POST:
            print(f'Examen agregar_cita_medica if POST')
            Nombre_Com_Pac = request.POST.get('Nombre_Com_Pac')
            print(f'Nombre_Com_Pac{Nombre_Com_Pac}')
            print(f'nom_pac{nom_pac}')
            url =  reverse('orden_examen') + '?nom_pac={}&id_fecha={}&id_ficha={}&diagnostico={}&id_cita={}'.format(nom_pac,id_fecha,id_ficha, diagnostico,id_cita)
            return redirect(url)
        if 'finalizar_atencion' in request.POST:
            print('Estoy aqui')
            if Cita.objects.filter(ID_Cita = id_fecha).exists():
                print('Entre aqui')
                Cita.objects.filter(ID_Cita = id_fecha).delete()
            else:
                CitaSinUsuario.objects.filter(ID_Cita = id_fecha).delete()
            return redirect('index')
        
        if 'ver_ficha_medica' in request.POST:
            ID_Ficha_Medica = request.POST.get('ver_ficha_medica')
            print(f'id_ficha is not None: if  id de la ficha: {ID_Ficha_Medica}')
            url = reverse('ver_ficha_medica') + '?ID_Ficha_Medica={}'.format(ID_Ficha_Medica)
            return redirect(url)

        Cita_Medica = Ficha_Cita.objects.get(ID_Ficha_Cita=id_ficha)
        Ficha_Medica_Pac = Cita_Medica.Ficha_Medica_Pac
        RUT_Pac = Cita_Medica.RUT_Pac
        Nombre_Com_Pac = Cita_Medica.Nombre_Com_Pac
        Nombre_Com_Esp = Cita_Medica.Nombre_Com_Esp
        Fecha_Cita = Cita_Medica.Fecha_Cita
        Diagnostico_Cita = Cita_Medica.Diagnostico_Cita
        validar_receta = Cita_Medica.Receta
        validar_orden = Cita_Medica.Examene
        print(f'Validar receta: {validar_receta}')
        datos_form = {'Ficha_Medica_Pac':Ficha_Medica_Pac,'Ficha_Medica_Pac':Ficha_Medica_Pac, 'RUT_Pac':RUT_Pac,
                    'Nombre_Com_Pac':Nombre_Com_Pac, 'Fecha_Cita':Fecha_Cita, 'Nombre_Com_Esp':Nombre_Com_Esp,
                    'Diagnostico_Cita':Diagnostico_Cita}
        formulario = FormCitaMedica(initial=datos_form)
        formulario.fields['Diagnostico_Cita'].widget.attrs['readonly'] = True
        contexto = {'FormCitaMedica':formulario, 'validar_receta':validar_receta, 'validar_orden':validar_orden, 'Ficha_Medica_Pac':Ficha_Medica_Pac}
        return render(request, "Especialistas/agregar_cita_medica.html", contexto)
    else:
        if request.method == 'POST':
            form_Post = FormCitaMedica(data=request.POST)
            if 'ver_ficha_medica' in request.POST:
                print('Ahora llegue al verfichamedica ')
                ID_Ficha_Medica = request.POST.get('ver_ficha_medica')
                print(f'id_ficha is not None: else  id de la ficha: {ID_Ficha_Medica}')
                url = reverse('ver_ficha_medica') + '?ID_Ficha_Medica={}&id_ficha={}'.format(ID_Ficha_Medica,id_ficha)
                return redirect(url)
            if form_Post.is_valid():
                print('Primero estoy pasando por el save')
                atencion = form_Post.save()
                messages.success(request, "Diagnostico médica agregada con éxito")
                id_ficha = atencion.ID_Ficha_Cita
                diagnostico = atencion.Diagnostico_Cita
            if 'Receta' in request.POST:   
                print(f'Receta agregar_cita_medica else POST')
                url =  reverse('receta_medica') + '?nom_pac={}&id_fecha={}&id_ficha={}&diagnostico={}'.format(Nombre_Com_Pac,id_fecha,id_ficha,diagnostico)
                return redirect(url)
            if 'Examen' in request.POST:
                print(f'Examen agregar_cita_medica else POST')
                url =  reverse('orden_examen') + '?nom_pac={}&id_fecha={}&id_ficha={}&diagnostico={}&id_cita={}'.format(Nombre_Com_Pac,id_fecha,id_ficha, diagnostico,id_cita)
                return redirect(url)
            if 'finalizar_atencion' in request.POST:
                print('Estoy aqui')
                if Cita.objects.filter(ID_Cita = id_fecha).exists():
                    print('Entre aqui')
                    Cita.objects.filter(ID_Cita = id_fecha).delete()
                else:
                    CitaSinUsuario.objects.filter(ID_Cita = id_fecha).delete()
                return redirect('index')
            

        
        Ficha_Medica_Pac = request.GET.get('Ficha_Medica_Pac')
        print(f'Ficha_Medica_Pac: {Ficha_Medica_Pac}')
        RUT_Pac = request.GET.get('RUT_Pac')
        Nombre_Com_Pac = request.GET.get('Nombre_Com_Pac')
        Usuario = User.objects.get(username = request.user.username)
        Nombre_Com_Esp = Especialista.objects.get(Usuario_E = Usuario)
        Fecha_Cita = date.today()
        datos_form = {'Ficha_Medica_Pac':Ficha_Medica_Pac, 'RUT_Pac':RUT_Pac, 'Nombre_Com_Pac':Nombre_Com_Pac, 'Fecha_Cita':Fecha_Cita, 'Nombre_Com_Esp':Nombre_Com_Esp}
        formulario = FormCitaMedica(initial=datos_form)
        contexto = {'FormCitaMedica':formulario, 'Ficha_Medica_Pac':Ficha_Medica_Pac}
        return render(request, "Especialistas/agregar_cita_medica.html", contexto)

def ver_receta_medica(request):
    print('GET DE RECETA MEDICA')
    nom_pac = request.GET.get('nom_pac')
    id_fecha = request.GET.get('id_fecha')
    id_ficha = request.GET.get('id_ficha')
    receta = request.GET.get('receta')
    print(f'receta {receta}')
    diagnostico = request.GET.get('diagnostico')
    if receta is not None:
        print('ESTOY DENTROOOO')
        rec = Receta.objects.get(Numero_receta = receta)
        esp_rec = rec.Especialista_receta
        rut_esp_rec = rec.Rut_esp_receta
        espialidad_rec = rec.Especialidad_receta
        nom_pac_rec = rec.Nompre_paciente_receta
        rut_pac_rec = rec.Rut_pac_receta
        edad_rec = rec.Edad_pac_receta
        direccion_rec = rec.Direccion_pac_receta
        diagnostico_rec = rec.Diagnostico_rec
        descripcion_rec = rec.Descripcion_receta
        data = {"Especialista_receta":esp_rec, "Especialidad_receta":espialidad_rec, "Rut_esp_receta":rut_esp_rec, 
            "Nompre_pac_receta":nom_pac_rec, "Rut_pac_receta":rut_pac_rec, "Edad_pac_receta":edad_rec, "Direccion_pac_receta":direccion_rec,
            "Diagnostico_pac_receta":diagnostico_rec,"Descripcion_receta":descripcion_rec}    
        form_ver_receta = FormReceta(initial = data)
        context = {'form_ver_receta':form_ver_receta}
        return render(request, "Especialistas/receta_medica.html",context)
    else:
        paciente = Paciente.objects.get(Nombre_Paciente= nom_pac)
        rut_pac = paciente.Rut
        hoy = date.today()
        edad = hoy.year - paciente.Fecha_de_nacimiento_P.year
        direccion = paciente.Direccion_P
        user = request.user

        especialista = Especialista.objects.get(Usuario_E= user)
        rut_esp = especialista.Rut

        #Espeacialidad
        dia = hoy.strftime('%A').replace('Monday','lun').replace('Tuesday','mar').replace('Wednesday','mie').replace('Thursday','jue').replace('Friday','vie').replace('Saturday','sab').replace('Sunday','dom')
        if dia in especialista.Dia_Esp_P:
            esp = especialista.Especialidad_P
        else:
            esp = especialista.Especialidad_S

        data = {"Especialista_receta":especialista, "Especialidad_receta":esp, "Rut_esp_receta":rut_esp, 'Diagnostico_pac_receta':diagnostico,
                "Nompre_pac_receta":nom_pac, "Rut_pac_receta":rut_pac, "Edad_pac_receta":edad, "Direccion_pac_receta":direccion}    
        
        form_receta = FormReceta(initial = data)
        context = {'form_receta':form_receta}
        print('ESPERANDO EL POST')
        if request.method == "POST":
            form_rec_com = FormReceta(data = request.POST)
            print('POST')
            if form_rec_com.is_valid():
                # redireccion_valor_o = request.POST.get('redireccionar_o')
                # receta = form_rec_com.save()
                # Ficha_Cita.objects.filter(ID_Ficha_Cita = id_ficha).update(Receta = receta)
                # messages.success(request, "Cita médica agregada con éxito")
                # url =  reverse('orden_examen') + '?nom_pac={}&id_fecha={}&diagnostico={}&id_ficha={}'.format(form_rec_com.cleaned_data['Nompre_pac_receta'],id_fecha,receta.Diagnostico_rec,id_ficha)
                # if redireccion_valor_o == "1":
                    # print('Estoy entrando aqui :D')
                    # receta = form_rec_com.save()
                    # Ficha_Cita.objects.filter(ID_Ficha_Cita = id_ficha).update(Receta = receta)
                    # messages.success(request, "Cita médica agregada con éxito")
                    # url =  reverse('orden_examen') + '?nom_pac={}&id_fecha={}&diagnostico={}&id_ficha={}'.format(form_rec_com.cleaned_data['Nompre_pac_receta'],id_fecha,receta.Diagnostico_rec,id_ficha)
                    # return redirect(url)
                
                receta = form_rec_com.save()
                Ficha_Cita.objects.filter(ID_Ficha_Cita = id_ficha).update(Receta = receta)
                messages.success(request, "Cita médica agregada con éxito")
                url = reverse('agregar_cita_medica') + '?nom_pac={}&id_fecha={}&id_ficha={}&diagnostico={}'.format(nom_pac,id_fecha,id_ficha,diagnostico)
                return redirect(url)
            
    return render(request, "Especialistas/receta_medica.html",context)

#TODO EL TIPO DE PREVISION DEBE SER EL DEL QUE SE ASIGNO EN LA CITA
def ver_orden_examen(request):
    nom_pac = request.GET.get('nom_pac')
    id_fecha = request.GET.get('id_fecha')
    diagnostico = request.GET.get('diagnostico')
    id_ficha = request.GET.get('id_ficha')
    id_cita = request.GET.get('id_cita')

   
    orden = request.GET.get('orden')
    if orden is not None:
        print(f'orden examen dentro del if {orden}')
        examen = Examene.objects.get(Numero_orden_examen = orden)
        nom_pac_orden = examen.Nombre_pac_orden
        rut_pac_orden = examen.Rut_pac_orden
        edad_pac_orden = examen.Edad_pac_orden
        fecha_pac_orden = examen.Fecha_nac_pac_orden
        prevision_orden = examen.Prevision_pac_orden
        servicio_orden = examen.Servicio_pac_orden
        diagnostico_orden = examen.Diagnostico_orden
        nombre_med_orden = examen.Nombre_Medico_orden
        rut_med_orden = examen.Rut_Medico_orden
        examenes_orden = examen.Examenes.split(',')
        print(examenes_orden)
        data = {'nombre_pac':nom_pac_orden, 'rut_pac':rut_pac_orden, 'edad_pac':edad_pac_orden, 'Fecha_Cita':fecha_pac_orden, 'nombre_medico':nombre_med_orden,
            'rut_medico':rut_med_orden, 'diagnostico':diagnostico_orden, 'servicio': servicio_orden, 'prevision':prevision_orden}
        form_ver_examenes = FormExamenes(initial=data)
        context = {'form_ver_examenes':form_ver_examenes, 'examenes_orden':examenes_orden}
    else:
        if Cita.objects.filter(ID_Cita =id_fecha).exists():
            print('Si existe loco')
            prevision = Cita.objects.get(ID_Cita = id_fecha).Metodo_Pago_Cita
        else:
            print('No existe naa')
            prevision = CitaSinUsuario.objects.get(ID_Cita = id_fecha).Metodo_Pago_Cita
        # metodo = CitaSinUsuario.objects.get(ID_Cita = id_fecha).Metodo_Pago_Cita

        pac = Paciente.objects.get(Nombre_Paciente=nom_pac)
        rut_pac = pac.Rut
        edad = date.today().year - pac.Fecha_de_nacimiento_P.year 
        fecha_nac = pac.Fecha_de_nacimiento_P
        user = request.user
        especialista = Especialista.objects.get(Usuario_E= user)
        rut_esp = especialista.Rut
        data = {'nombre_pac':nom_pac, 'rut_pac':rut_pac, 'edad_pac':edad, 'Fecha_Cita':fecha_nac, 'nombre_medico':especialista,
                'rut_medico':rut_esp, 'prevision':prevision, 'diagnostico':diagnostico}
        formExamenes = FormExamenes(initial=data)
        examenes_field = formExamenes['examenes']
        examenes_widget = examenes_field.field.widget
        context = {'formExamenes': formExamenes, 'examenes_field': examenes_field, 'examenes_widget': examenes_widget}
    
    if request.method =='POST':
        form_com = FormExamenes(data = request.POST)
        print(form_com)
        print(form_com.is_valid())
        if form_com.is_valid():
            #Obtengo la cadena de texto y le aplico split para almacenarla sin formato lista
            texto = form_com.cleaned_data['examenes']
            print(type(texto))

            examen = form_com.save()
            Ficha_Cita.objects.filter(ID_Ficha_Cita = id_ficha).update(Examene = examen)
            messages.success(request, "Orden de examenes registrada")
            url = reverse('agregar_cita_medica') + '?nom_pac={}&id_fecha={}&id_ficha={}&diagnostico={}'.format(nom_pac,id_fecha,id_ficha,diagnostico)
            return redirect(url)
    print(f'CONTEXTO: {context}')
    return render(request, "Especialistas/orden_examen.html", context)


def ver_cita_medica(request):
    ID_Ficha_Cita = request.GET.get('ID_Ficha_Cita')
    Cita_Medica = Ficha_Cita.objects.get(ID_Ficha_Cita=ID_Ficha_Cita)
    Ficha_Medica_Pac = Cita_Medica.Ficha_Medica_Pac
    RUT_Pac = Cita_Medica.RUT_Pac
    Nombre_Com_Pac = Cita_Medica.Nombre_Com_Pac
    Nombre_Com_Esp = Cita_Medica.Nombre_Com_Esp
    Fecha_Cita = Cita_Medica.Fecha_Cita
    Diagnostico_Cita = Cita_Medica.Diagnostico_Cita
    datos_form = {'Ficha_Medica_Pac':Ficha_Medica_Pac,'Ficha_Medica_Pac':Ficha_Medica_Pac, 'RUT_Pac':RUT_Pac,
                  'Nombre_Com_Pac':Nombre_Com_Pac, 'Fecha_Cita':Fecha_Cita, 'Nombre_Com_Esp':Nombre_Com_Esp,
                  'Diagnostico_Cita':Diagnostico_Cita}
    formulario = FormCitaMedica(initial=datos_form)
    formulario.fields['Diagnostico_Cita'].widget.attrs['readonly'] = True
    contexto = {'FormCitaMedica':formulario}
    return render(request, 'Especialistas/ver_cita_medica.html', contexto)

def form_ficha_medica(request):

    nombre_pac = request.GET.get('nombre_pac')
    rut = request.GET.get('rut')
    id_fecha = request.GET.get('id_fecha')
    print(f'Nombre del paciente{nombre_pac}')
    print(f'Fecha{nombre_pac}')
    if nombre_pac =='None':
        url = reverse('perfil') + '?rut={}&nombre_pac={}&id_fecha={}'.format(rut,nombre_pac,id_fecha)
        return redirect(url)
    else:
        print('Estoy en el else')
    paciente = Paciente.objects.get(Nombre_Paciente = nombre_pac)

    print("Si, soy yo")
    RUT_Pac = paciente.Rut
    Nombre_Com_Pac = paciente.Nombre_Paciente
    Direccion_Pac = paciente.Direccion_P
    Telefono_Pac = paciente.Telefono_P

    datos_form = {'RUT_Pac':RUT_Pac,'Nombre_Com_Pac':Nombre_Com_Pac, 'Direccion_Pac':Direccion_Pac, 'Telefono_Pac':Telefono_Pac}

    formulario = {'formFichaMedica':FormFichaMedica(initial = datos_form )}
    
    if request.method == 'POST':
        formulario_post =  FormFichaMedica(data=request.POST)
        if formulario_post.is_valid():
            RUT_Pac = formulario_post.cleaned_data['RUT_Pac']
            Nombre_Com_Pac = formulario_post.cleaned_data['Nombre_Com_Pac']
            Direccion_Pac = formulario_post.cleaned_data['Direccion_Pac']
            Telefono_Pac = formulario_post.cleaned_data['Telefono_Pac']
            Sis_Sal_Pac = formulario_post.cleaned_data['Sis_Sal_Pac']           
            Grupo_Sanguineo = formulario_post.cleaned_data['Grupo_Sanguineo']
            Al_Antibioticos = formulario_post.cleaned_data['Al_Antibioticos']
            Antibioticos_TI = formulario_post.cleaned_data['Antibioticos_TI']
            Al_Medicamentos = formulario_post.cleaned_data['Al_Medicamentos']
            Medicamentos_TI = formulario_post.cleaned_data['Medicamentos_TI']
            Al_Alimentos = formulario_post.cleaned_data['Al_Alimentos']
            Alimentos_TI = formulario_post.cleaned_data['Alimentos_TI']
            Al_Ani_Ins = formulario_post.cleaned_data['Al_Ani_Ins']
            Ani_Ins_TI = formulario_post.cleaned_data['Ani_Ins_TI']
            Enf_Cronic = formulario_post.cleaned_data['Enf_Cronic']
            Enf_Cronic_TI = formulario_post.cleaned_data['Enf_Cronic_TI']
            Observaciones_Ficha = formulario_post.cleaned_data['Observaciones_Ficha']
            Cont_Fichas_Med = Ficha_Medica.objects.all().count()
            ID_Ficha_Medica = Cont_Fichas_Med+1
            Ficha_Medica.objects.create(ID_Ficha_Medica=ID_Ficha_Medica, RUT_Pac=RUT_Pac ,Nombre_Com_Pac=Nombre_Com_Pac, Direccion_Pac=Direccion_Pac,Telefono_Pac=Telefono_Pac,
                                        Sis_Sal_Pac=Sis_Sal_Pac, Grupo_Sanguineo=Grupo_Sanguineo, Al_Antibioticos=Al_Antibioticos, Antibioticos_TI=Antibioticos_TI, Al_Medicamentos=Al_Medicamentos,
                                        Medicamentos_TI=Medicamentos_TI, Al_Alimentos=Al_Alimentos, Alimentos_TI=Alimentos_TI, Al_Ani_Ins=Al_Ani_Ins, Ani_Ins_TI=Ani_Ins_TI,
                                        Enf_Cronic=Enf_Cronic,  Enf_Cronic_TI=Enf_Cronic_TI, Observaciones_Ficha=Observaciones_Ficha)
            messages.success(request, "Ficha Médica creada con éxito")
            url = reverse('ficha_medica') + '?nom_pac={}&id_fecha={}'.format(formulario_post.cleaned_data['Nombre_Com_Pac'],id_fecha)
            return redirect(url)
        else:
            print("No es valido")
    return render(request, 'Especialistas/form_Ficha_Medica.html', formulario)

def ver_ficha_medica(request):
    ID_Ficha_Medica = request.GET.get('ID_Ficha_Medica')
    Ficha_Med = Ficha_Medica.objects.get(ID_Ficha_Medica=ID_Ficha_Medica)
    RUT_Pac = Ficha_Med.RUT_Pac
    Nombre_Com_Pac = Ficha_Med.Nombre_Com_Pac
    Direccion_Pac = Ficha_Med.Direccion_Pac
    Telefono_Pac = Ficha_Med.Telefono_Pac
    Sis_Sal_Pac = Ficha_Med.Sis_Sal_Pac
    Grupo_Sanguineo = Ficha_Med.Grupo_Sanguineo
    Al_Antibioticos = Ficha_Med.Al_Antibioticos
    Antibioticos_TI = Ficha_Med.Antibioticos_TI
    Al_Medicamentos = Ficha_Med.Al_Medicamentos
    Medicamentos_TI = Ficha_Med.Medicamentos_TI
    Al_Alimentos = Ficha_Med.Al_Alimentos
    Alimentos_TI = Ficha_Med.Alimentos_TI
    Al_Ani_Ins = Ficha_Med.Al_Ani_Ins
    Ani_Ins_TI = Ficha_Med.Ani_Ins_TI
    Enf_Cronic = Ficha_Med.Enf_Cronic
    Enf_Cronic_TI = Ficha_Med.Enf_Cronic_TI
    Observaciones_Ficha = Ficha_Med.Observaciones_Ficha
    datos_form =  {
        'RUT_Pac': RUT_Pac,
        'Nombre_Com_Pac': Nombre_Com_Pac,
        'Direccion_Pac': Direccion_Pac,
        'Telefono_Pac': Telefono_Pac,
        'Sis_Sal_Pac': Sis_Sal_Pac,
        'Grupo_Sanguineo': Grupo_Sanguineo,
        'Al_Antibioticos': Al_Antibioticos,
        'Antibioticos_TI': Antibioticos_TI,
        'Al_Medicamentos': Al_Medicamentos,
        'Medicamentos_TI': Medicamentos_TI,
        'Al_Alimentos': Al_Alimentos,
        'Alimentos_TI': Alimentos_TI,
        'Al_Ani_Ins': Al_Ani_Ins,
        'Ani_Ins_TI': Ani_Ins_TI,
        'Enf_Cronic': Enf_Cronic,
        'Enf_Cronic_TI': Enf_Cronic_TI,
        'Observaciones_Ficha' : Observaciones_Ficha,
        }
    formulario = FormFichaMedica(initial=datos_form)
    formulario.fields['RUT_Pac'].widget.attrs['readonly'] = True
    formulario.fields['Nombre_Com_Pac'].widget.attrs['readonly'] = True
    formulario.fields['Direccion_Pac'].widget.attrs['readonly'] = True
    formulario.fields['Telefono_Pac'].widget.attrs['readonly'] = True
    formulario.fields['Sis_Sal_Pac'].widget.attrs['disabled'] = True
    formulario.fields['Grupo_Sanguineo'].widget.attrs['disabled'] = True
    formulario.fields['Al_Antibioticos'].widget.attrs['disabled'] = True
    formulario.fields['Antibioticos_TI'].widget.attrs['readonly'] = True
    formulario.fields['Al_Medicamentos'].widget.attrs['disabled'] = True
    formulario.fields['Medicamentos_TI'].widget.attrs['readonly'] = True
    formulario.fields['Al_Alimentos'].widget.attrs['disabled'] = True
    formulario.fields['Alimentos_TI'].widget.attrs['readonly'] = True
    formulario.fields['Al_Ani_Ins'].widget.attrs['disabled'] = True
    formulario.fields['Ani_Ins_TI'].widget.attrs['readonly'] = True
    formulario.fields['Enf_Cronic'].widget.attrs['disabled'] = True
    formulario.fields['Enf_Cronic_TI'].widget.attrs['readonly'] = True
    formulario.fields['Observaciones_Ficha'].widget.attrs['readonly'] = True
    contexto = {'formFichaMedica':formulario}

    return render(request, 'Especialistas/ver_ficha_medica.html', contexto)

def pacientes_fichas_medicas(request):
    if request.method == 'POST':
        print("Manolo Print")
        if 'doc_pac' in request.POST:
            # Si se ha solicitado la ficha médica de un paciente, obtener el nombre del paciente y redirigir a la página de ficha médica
            nom_pac = request.POST.get('doc_pac')
            url = reverse('filtro_ficha_medica') + '?nom_pac={}'.format(nom_pac)
            return redirect(url)
        elif 'buscar-btn' in request.POST:
            print("Manolo buscar-btn")
            rut = request.POST.get('buscar-input')
            Pacientes = Paciente.objects.filter(Rut__icontains=rut)
    else:
        print("Manolo Else")
        Pacientes = Paciente.objects.all()
    contexto = {'Pacientes':Pacientes}
    return render(request, "Especialistas/pacientes_fichas_medicas.html", contexto)

#Views Operadores
def select_destinatario(request):
    global destinatario
    todos_Especialistas = Especialista.objects.all()

    contexto = {
        'especialistas_filtrados': todos_Especialistas,
    }
    print(f'Valor de contexto: {contexto}')
    if request.method=='POST':
        filtro = request.POST.get('chat_btn')
        print(f'Valor de filtro: {filtro}')
        if filtro:
            print(f'Valor de filtro dentro del If: {filtro}')
            todos_Especialistas = todos_Especialistas.filter(Nombre_completo_E__icontains=filtro)
            print(f'Valor de todos_Especialistas: {todos_Especialistas}')

        destinatario = todos_Especialistas[0].Nombre_completo_E
        print("destinatario")
        print(destinatario)
        return redirect('chat')

    return render(request, "General/select_Destinatario.html", contexto)

def chatsito(request):
    print('ANTES DEL REMITENTE')
    remitente = User.objects.filter(username=request.user.username)[0].username
    print('ANTES DE DESTINATARIO')
    destinatario_E = Especialista.objects.get(Nombre_completo_E=destinatario)
    print('ANTES DE DESTINATARIO')
    print(remitente)
    print(destinatario_E)
    mensajes = Mensaje.objects.filter(Nombre_Remitente=remitente, Nombre_Destinatario=destinatario) | Mensaje.objects.filter(Nombre_Remitente=destinatario, Nombre_Destinatario=remitente)
    print('DESPUES DE DESTINATARIO')
    mensajes = mensajes.order_by('fecha')
    formmensaje = FormMensaje()
    contexto = {'remitente': remitente, 'destinatario': destinatario, 'mensajes': mensajes, 'formmensaje': formmensaje}

    if request.method == 'POST':
        print('DENTRO DEL IF')
        return render(request, 'General/chat.html', contexto)
        
    return render(request, 'General/chat.html', contexto)
    
def listadias(lista,diap,dias):
    for x in diap:
        lista.append(x)

    for x in dias:
        lista.append(x)

    return lista

def operador_funciones(request):
    return render(request, 'Operador/funciones_operador.html')

def operador_lista_agenda(request):
    lista_especialista = Especialista.objects.all()
    context = {'lista_especialista': lista_especialista}
    if request.method == 'POST':
        especialista_select = request.POST.get('consultar')
        print(especialista_select)
        url = reverse('calendario_especialista')+'?especialista_select={}'.format(especialista_select)
        return redirect(url)
    return render(request, 'Operador/Consultar_Agenda/operador_listar_especialista.html',context)

def operador_lista_agenda_dos(request):
    lista_especialista = Especialista.objects.all()
    context = {'lista_especialista': lista_especialista}
    if request.method == 'POST':
        especialista_select = request.POST.get('consultar')
        print(especialista_select)
        url = reverse('agenda_citas_medico')+'?especialista_select={}'.format(especialista_select)
        return redirect(url)
    return render(request, 'Operador/Consultar_Agenda/operador_listar_especialista_dos.html',context)

def operador_agenda_medica(request):
    fecha = date.today()
    id_especialista = request.GET.get('especialista_select')
    Especialista_Cont = Especialista.objects.get(ID_Especialista=id_especialista)
    nom_medico = Especialista_Cont.Nombre_completo_E.split(' ')
    nom_medico = nom_medico[0]+ ' ' + nom_medico[-2]
    cita_con_usuario = Cita.objects.filter(ID_Especialista = id_especialista, Fecha_Cita=fecha)
    cita_sin_usuario = CitaSinUsuario.objects.filter(ID_Especialista = id_especialista, Fecha_Cita=fecha)
    hay_cita_con_usuario = cita_con_usuario.exists()
    hay_cita_sin_usuario = cita_sin_usuario.exists()
    lista_agenda=[]
    lista_sin=[]
    if cita_sin_usuario.exists():
        for cita_sin in cita_sin_usuario:
            rut_cita = cita_sin.Rut_Paciente
            cita_sin.Confirmacion_Cita_Operador
            print(f'rut {rut_cita}')
            paciente = Paciente.objects.get(Rut = rut_cita)
            nombre_com = paciente.Nombre_Paciente
            nombre = nombre_com.split()
            nombre_pac = nombre[0]
            apellido_pac = " ".join(nombre[-2:-1])
            telefono = cita_sin.Telefono_Contacto
            edad = date.today().year - paciente.Fecha_de_nacimiento_P.year
            lista_sin.append({'cita_sin':cita_sin, 'paciente':paciente,"nombre_pac":nombre_pac,"apellido_pac":apellido_pac, "rut_cita":rut_cita, "edad":edad, "nombre_com":nombre_com})
    if cita_con_usuario.exists():
        for cita in cita_con_usuario:
            paciente = Paciente.objects.get(Usuario_P = cita.ID_Cliente)
            nombre_com = paciente.Nombre_Paciente
            nombre = nombre_com.split()
            nombre_pac = nombre[0]
            apellido_pac = " ".join(nombre[-2:-1])
            rut_cita = paciente.Rut
            edad = date.today().year - paciente.Fecha_de_nacimiento_P.year
            lista_agenda.append({'cita':cita, 'paciente':paciente,"nombre_pac":nombre_pac,"apellido_pac":apellido_pac, "rut_cita":rut_cita, "edad":edad, "nombre_com":nombre_com})
    context = {'Especialista_Cont':Especialista_Cont, 'nom_medico':nom_medico, 'lista_sin':lista_sin,
                'lista_agenda':lista_agenda, 'hay_cita_con_usuario':hay_cita_con_usuario, 'hay_cita_sin_usuario':hay_cita_sin_usuario,
                'cita_con_usuario':cita_con_usuario, 'cita_sin_usuario':cita_sin_usuario}
    
    if request.method == 'POST':
        id_cita = request.POST.get('cita_seleccionada')
        print(f'valor id_cita{id_cita}')
        if id_cita is None:
            id_cita = request.POST.get('cita_hidden')
            print(f'valor id_cita None {id_cita}')
        id_cita = id_cita.replace("de ","").replace("a las ","")
        id_cita = id_cita.replace('Enero','January').replace('Febrero','February').replace('Marzo','March').replace('Abril','April').replace('Mayo','May').replace('Junio','June').replace('Julio','July').replace('Agosto','August').replace('Septiembre','September').replace('Octubre','October').replace('Noviembre','November').replace('Diciembre','December')
        print(f'Cual es la cita {id_cita}')
  
        id_cita = datetime.strptime(id_cita, "%d %B %Y %H:%M")
                                 
        if Cita.objects.filter(ID_Cita = id_cita).exists():
            cita_confirmada = Cita.objects.get(ID_Cita = id_cita)
            cita_confirmada.Confirmacion_Cita_Operador = True
            nom_pac= cita_confirmada.ID_Cliente
            
            print(f'nom_pac{nom_pac}')
            cita_confirmada.save()
            messages.success(request, "Paciente confirmado.")

            id_cobro = Cobro.objects.all().count()+1
            rut = Paciente.objects.get(Usuario_P = nom_pac).Rut
            esp = cita_confirmada.ID_Especialista
            especialista = Especialista.objects.get(Nombre_completo_E = esp)

            #Obtener especialidad
            hoy = date.today()
            #Remplaso el dia en ingles por el valor que le indicamos en el modelo.
            hoy = hoy.strftime('%A').replace('Monday','lun').replace('Tuesday','mar').replace('Wednesday','mie').replace('Thursday','jue').replace('Friday','vie').replace('Saturday','sab').replace('Sunday','dom')

            #Cobro de especialidades
            cobro_especialidad = CobrosEspecialistas.objects.get(ID_Especialista = especialista)

            #Valida si el dia se encuentra en alguna de de las listas de dias de la especialidad y el cobro de ella
            if hoy in especialista.Dia_Esp_P:
                especialidad = especialista.Especialidad_P
                cobro_atencion = cobro_especialidad.Monto_Esp_P
                print(f'Valor de hoy {hoy}')
            else:
                especialidad = especialista.Especialidad_S
                cobro_atencion = cobro_especialidad.Monto_Esp_S
                print(f'Valor de hoy {hoy} dentro del else')


            print(f'Especialista encontrado :{especialista}')
            print(f'Rut del paciente: {rut}')
            metodo = cita_confirmada.Metodo_Pago_Cita

            cobro_cita =  Cobro.objects.create(ID_Cobro = id_cobro, Rut_Pac_Cobro = rut, Especialista_Cobro=especialista,
                                               Especialidad_Cobro = especialidad, Monto = cobro_atencion, Metodo = metodo, Estado_cobro='Por pagar')
            
            id_cobro = cobro_cita.ID_Cobro

            redireccion_confirmar = request.POST.get('redireccion_confirmar')
            print(f'Valor redirect: {redireccion_confirmar}')
            if redireccion_confirmar == "1":
                print('redireccion_confirmar if')
                url = reverse('operador_pagar')+"?id_cobro={}&rut={}&metodo={}".format(id_cobro, rut, metodo)
                return redirect(url)
            else:
                print('redireccion_confirmar else')
                url = reverse('agenda_citas_medico')+ "?especialista_select={}".format(id_especialista)
                return redirect(url) 
        else:
            print('Estoy antes del cita confirmada')
            cita_confirmada = CitaSinUsuario.objects.get(ID_Cita = id_cita)
            print(cita_confirmada.Confirmacion_Cita_Operador)
            cita_confirmada.Confirmacion_Cita_Operador = True
            print(cita_confirmada.Confirmacion_Cita_Operador)
            rut_pac = cita_confirmada.Rut_Paciente
            cita_confirmada.save()
            messages.success(request, "Paciente confirmado.")
            if Paciente.objects.filter(Rut=rut_pac).exists():
                url = reverse('agenda_citas_medico')+ "?especialista_select={}".format(id_especialista)
                return redirect(url)
            else:
                url = reverse('perfil')+ "?rut={}&id_cita={}".format(rut_pac,id_cita)
                return redirect(url)
    return render(request, 'Operador/Consultar_Agenda/operador_agenda_especialista.html', context)


def operador_calendario_especialista(request):
    id_especialista = request.GET.get('especialista_select')
    print(id_especialista)
    dias_especialista = Especialista.objects.filter(ID_Especialista = id_especialista)
    semana = []
    semana = list(dias_especialista[0].Dia_Esp_P) + list(dias_especialista[0].Dia_Esp_S)
    dias_es = ','.join(semana).replace('lun','Lunes').replace('mar','Martes').replace('mie','Miercoles').replace('jue','Jueves').replace('vie','Viernes').replace('sab','Sabado').replace('dom','Domingo')
    dias_en = ','.join(semana).replace('lun','Monday').replace('mar','Tuesday').replace('mie','Wednesday').replace('jue','Thursday').replace('vie','Friday').replace('sab','Saturday').replace('dom','Sunday')
    print(dias_en)
    fecha_ope = dias_trabaja_especialista(dias_en)
    calendario_especialista = {
        'formDate': DateForm(),
        'fechas': fecha_ope
    }
    if request.method == 'POST':
        fecha = DateForm(request.POST)
        if fecha.is_valid():
            fecha = fecha.cleaned_data['date']
            dia_seleccionado = calendar.day_name[fecha.weekday()]
            dia_seleccionado = dia_seleccionado.replace('Monday','lun').replace('Tuesday','mar').replace('Wednesday','mie').replace('Thursday','jue').replace('Friday','vie').replace('Saturday','sab').replace('Sunday','dom')

            if fecha in fecha_ope:
                dias_str_p = ','.join(dias_especialista[0].Dia_Esp_P)
                lista, lista_reserva, especialidad = dias_minutos_especialidad(dia_seleccionado, dias_str_p, dias_especialista, fecha, id_especialista)
                url = reverse('operador_horas_esp')+'?lista={}&lista_reserva={}&id_especialista={}&especialidad={}&fecha={}'.format(lista,lista_reserva,id_especialista,especialidad,fecha)
                return redirect(url)
                #return render(request, 'Operador/operador_horas_especialista.html', lista)
            else:
                messages.error(request, "Ingrese una fecha en los dias: "+str(dias_es).replace('[','').replace(']','').replace("'","")+".")
                return render(request,'Operador/Consultar_Agenda/operador_calendario_especialista.html', calendario_especialista)
    return render(request, 'Operador/Consultar_Agenda/operador_calendario_especialista.html', calendario_especialista)

def operador_horas_especialista(request):
    id_especialista = request.GET.get('id_especialista')
    especialidad = request.GET.get('especialidad')
    fecha = request.GET.get('fecha')
    list_horas = request.GET.get('lista').replace("'","").replace("[","").replace("]","").split(', ')
    list_Citas_Reservadas = request.GET.get('lista_reserva').replace("'","").replace("[","").replace("]","").split(', ')
    listavalores = {"list_horas":list_horas,"list_Citas_Reservadas": list_Citas_Reservadas, "especialidad" : especialidad}

    if request.method == 'POST':
        valor = request.POST.get('hora_agendar')
        url = reverse('agendar_citas_paciente')+'?valor={}&id_especialista={}&fecha={}'.format(valor,id_especialista,fecha)
        return redirect(url)

    return render(request, 'Operador/Consultar_Agenda/operador_horas_especialista.html', listavalores)

def operador_agendar_cita(request):

    id_especialista = request.GET.get('id_especialista')
    valor = request.GET.get('valor')
    fecha = request.GET.get('fecha')
    print(fecha)
    print(f'Valores del URL {id_especialista} {valor}')
    form_sin_user = FormPacienteSinUser

    context = {"form_sin_user":form_sin_user}

    if request.method == 'POST':
        rut = request.POST.get('rut_pac')
        email = request.POST.get('email_pac')
        telefono = request.POST.get('telefono_pac')
        metodo = request.POST.get('metodo_pago')
        esp = Especialista.objects.filter(ID_Especialista = id_especialista)
        fecha_id = str(fecha)+str(' '+valor)
        CitaSinUsuario.objects.create(ID_Cita=fecha_id,Fecha_Cita=fecha, Hora_Cita=valor, Rut_Paciente=rut, ID_Especialista=esp[0], Metodo_Pago_Cita = metodo)
        print(f'Datos {rut} {email} {telefono} {esp}')
        context = {'valor':valor , 'fecha':fecha}
        messages.success(request, "Hora creada con éxito")
        url = reverse('perfil') + '?rut={}&telefono={}'.format(rut,telefono)
        return redirect(url)
    return render(request, 'Operador/Consultar_Agenda/operador_agendar_cita.html', context)

def operador_modificar_cita(request):
    consulta_rut  = ConsultarRut()
    context = {"consulta_rut":consulta_rut}
    citas_usuarios = None
    citas_sin_usuario = None
    if request.method == "POST":
        if 'conf_delet_cit' in request.POST:
            ID_Cita = request.POST.get('conf_delet_cit').split(' ')
            print(ID_Cita)
            Ndia = ID_Cita[0]
            print(type(Ndia))
            print(f'Wena:{Ndia}')
            #ID_Cita = ' '.join(ID_Cita)
            Mes = ID_Cita[2].replace('Enero','01').replace('Febrero','02').replace('Marzo','03').replace('Abril','04').replace('Mayo','05').replace('Junio','06').replace('Julio','07').replace('Agosto','08').replace('Septiembre','09').replace('Octubre','10').replace('Noviembre','11').replace('Diciembre','12')
            Anno = ID_Cita[4]
            Hora = ID_Cita[7]
            ID_Cita = Ndia+'/'+Mes+'/'+Anno+' '+Hora
            ID_Cita = datetime.strptime(ID_Cita,'%d/%m/%Y %H:%M')
            print(type(ID_Cita))
            print(f'{ID_Cita}')
            if Cita.objects.filter(ID_Cita = ID_Cita).exists():
                Cita.objects.filter(ID_Cita = ID_Cita).delete()
                messages.success(request, "Cita eliminada con exito")
                return render(request, 'Operador/Modificar_Cita/operador_modificar_cita.html')
            else:
                holaaa = CitaSinUsuario.objects.filter(ID_Cita = ID_Cita)
                holaaa.delete()
                messages.success(request, "Cita eliminada con exito")
                return render(request, 'Operador/Modificar_Cita/operador_modificar_cita.html')
            
        if 'seleccion' in request.POST:
            print('INICIO DE SELECCION ESTOY AQUI')
            ID_Cita = request.POST.get('seleccion')
            ID_Cita = request.POST.get('seleccion').split(' ')
            print(ID_Cita)
            Ndia = ID_Cita[0]
            print(type(Ndia))
            print(f'Wena:{Ndia}')
            #ID_Cita = ' '.join(ID_Cita)
            Mes = ID_Cita[2].replace('Enero','01').replace('Febrero','02').replace('Marzo','03').replace('Abril','04').replace('Mayo','05').replace('Junio','06').replace('Julio','07').replace('Agosto','08').replace('Septiembre','09').replace('Octubre','10').replace('Noviembre','11').replace('Diciembre','12')
            Anno = ID_Cita[4]
            Hora = ID_Cita[7]
            ID_Cita = Ndia+'/'+Mes+'/'+Anno+' '+Hora
            ID_Cita = datetime.strptime(ID_Cita,'%d/%m/%Y %H:%M')
            print(ID_Cita)
            print('ANTES DEL IF AQUI')
            if Cita.objects.filter(ID_Cita = ID_Cita).exists():
                print('DENTRO DEL IF AQUI')
                cita_seleccionada = Cita.objects.filter(ID_Cita = ID_Cita)
                id_seleccion = ID_Cita
                fecha_seleccion = cita_seleccionada[0].Fecha_Cita
                hora_seleccion = cita_seleccionada[0].Hora_Cita
                seleccion = {"id_seleccion":id_seleccion, "fecha_seleccion":fecha_seleccion, "hora_seleccion":hora_seleccion}
                url = reverse('modificar_cita_seleccionada') + '?id_seleccion={}&fecha_seleccion={}&hora_seleccion={}'.format(id_seleccion,fecha_seleccion,hora_seleccion)
                print(type(id_seleccion))
                print(type(fecha_seleccion))
                print(type(hora_seleccion))
                print('ESTOY AQUI')
                return redirect(url)
            else:
                print('DENTRO DEL ELSE AQUI')
                cita_seleccionada = CitaSinUsuario.objects.filter(ID_Cita = ID_Cita)
                id_seleccion = ID_Cita
                print(f'VALOR DE ID_SELECCION {id_seleccion}')
                fecha_seleccion = cita_seleccionada[0].Fecha_Cita
                hora_seleccion = cita_seleccionada[0].Hora_Cita
                seleccion = {"id_seleccion":id_seleccion, "fecha_seleccion":fecha_seleccion, "hora_seleccion":hora_seleccion}
                print(type(id_seleccion))
                print(type(fecha_seleccion))
                print(type(hora_seleccion))
                url = reverse('modificar_cita_seleccionada') + '?id_seleccion={}&fecha_seleccion={}&hora_seleccion={}'.format(id_seleccion,fecha_seleccion,hora_seleccion)
                return redirect(url)
                
        valor = request.POST.get('rut')

        if Paciente.objects.filter(Rut = valor).exists():
            pacientes = Paciente.objects.get(Rut = valor)
            print(pacientes.Usuario_P)
            nom_pac =pacientes.Nombre_Paciente
            citas_usuarios = Cita.objects.filter(ID_Cliente = pacientes.Usuario_P)
            print(f'Citas con usuario  {citas_usuarios} ')
            if CitaSinUsuario.objects.filter(Rut_Paciente = valor).exists():
                citas_sin_usuario = CitaSinUsuario.objects.filter(Rut_Paciente = valor)
                print(f'Citas con usuario y sin {citas_usuarios} {citas_sin_usuario}')
            if Paciente.objects.filter(Rut = valor).exists() and len(citas_usuarios) == 0 and len(citas_sin_usuario) == 0:
                messages.error(request, "El rut ingresado no tiene ninguna cita agendada.")
                return render(request, 'Operador/Modificar_Cita/operador_modificar_cita.html')

        elif CitaSinUsuario.objects.filter(Rut_Paciente = valor).exists():
            citas_sin_usuario = CitaSinUsuario.objects.filter(Rut_Paciente = valor)
            print(f'Citas sin usuario {citas_sin_usuario}')

        elif CitaSinUsuario.objects.filter(Rut_Paciente = valor).exists() and Paciente.objects.filter(Rut = valor).exists() and citas_usuarios is None and citas_sin_usuario is None:

            messages.error(request, "El rut ingresado no tiene ninguna cita agendada.")
            return render(request, 'Operador/Modificar_Cita/operador_modificar_cita.html')
        else:
            messages.error(request, "El rut ingresado no figura en el sistema.")
            return render(request, 'Operador/Modificar_Cita/operador_modificar_cita.html')

        context = {'citas':citas_usuarios, 'citas_sin_usuario':citas_sin_usuario, 'nom_pac':nom_pac}

        return render (request, 'Operador/Modificar_Cita/operador_modificar_lista.html',context)
        
    return render(request, 'Operador/Modificar_Cita/operador_modificar_cita.html',context)

def operador_modificar_lista(request):
    hora_seleccion = request.GET.get('hora_seleccion')
    return render(request, 'Operador/Modificar_Cita/operador_modificar_lista.html', {"hora_seleccion":hora_seleccion})
    
def operador_modificar_seleccion(request):
    id_seleccions = request.GET.get('id_seleccion')
    fecha_seleccion = request.GET.get('fecha_seleccion')
    hora_seleccion = request.GET.get('hora_seleccion')

    #DIA
    fecha_seleccion = datetime.strptime(fecha_seleccion,'%Y-%m-%d')
    fecha_seleccion = fecha_seleccion.strftime('%A')
    fecha_seleccion = fecha_seleccion.replace('Monday','lun').replace('Tuesday','mar').replace('Wednesday','mie').replace('Thursday','jue').replace('Friday','vie').replace('Saturday','sab').replace('Sunday','dom')

    #DIAS ESPECIALISTA
    if Cita.objects.filter(ID_Cita=id_seleccions).exists():
        esp_cit = Cita.objects.filter(ID_Cita=id_seleccions)
    else:
        esp_cit = CitaSinUsuario.objects.filter(ID_Cita=id_seleccions)

    esp = Especialista.objects.filter(ID_Especialista = esp_cit[0].ID_Especialista.ID_Especialista)

    if fecha_seleccion in list(esp[0].Dia_Esp_P):
        semana = list(esp[0].Dia_Esp_P)
    else:
        semana = list(esp[0].Dia_Esp_S)

    dias_es = ','.join(semana).replace('lun','Lunes').replace('mar','Martes').replace('mie','Miercoles').replace('jue','Jueves').replace('vie','Viernes').replace('sab','Sabado').replace('dom','Domingo')

    dias_en = ','.join(semana).replace('lun','Monday').replace('mar','Tuesday').replace('mie','Wednesday').replace('jue','Thursday').replace('vie','Friday').replace('sab','Saturday').replace('dom','Sunday')

    fechas_trab = dias_trabaja_especialista(dias_en)
    calendario_especialista ={
        'formDate': DateForm(),
        'fechas': fechas_trab,
        "fecha_seleccion": fecha_seleccion,
        "hora_seleccion":hora_seleccion
    }
    #ESPECIALISTA 
    esp_filter = Especialista.objects.filter(ID_Especialista = esp_cit[0].ID_Especialista.ID_Especialista)

    #FECHA HABILITADAS
    
    if request.method =='POST':
        print(f'HOLAA {fechas_trab}')
        print(f'HOLAA {esp[0].ID_Especialista}')
        fecha = DateForm(request.POST)
        if fecha.is_valid():
            fecha = fecha.cleaned_data['date']
            if fecha in fechas_trab:
                dias_str_p = ','.join(esp_filter[0].Dia_Esp_P)
                lista, lista_reserva, especialidad = dias_minutos_especialidad(fecha_seleccion,dias_str_p,esp_filter,fecha,esp[0].ID_Especialista)
                print(f'Dentro del post {lista}')
                print(f'Dentro del post {lista_reserva}')
                print(f'Dentro del post {especialidad}')

                url = reverse('modificar_fecha')+'?lista={}&lista_reserva={}&esp={}&especialidad={}&fecha={}&id_seleccions={}&hora_seleccion={}'.format(lista, lista_reserva, esp, especialidad,fecha,id_seleccions,hora_seleccion)
                return redirect(url)
            
            messages.error(request, "Ingrese una fecha en los dias: "+dias_es+".")
            return render(request, 'Operador/Modificar_Cita/operador_modificar_seleccion.html',calendario_especialista)
        print(esp)
        print(esp_cit)
        print(fecha_seleccion)

    return render(request, 'Operador/Modificar_Cita/operador_modificar_seleccion.html',calendario_especialista)

def operador_modificar_fecha(request):
    hora_seleccion = request.GET.get('hora_seleccion')
    lista = request.GET.get('lista').replace("'","").replace("[","").replace("]","").split(', ')
    lista_reserva = request.GET.get('lista_reserva').replace("'","").replace("[","").replace("]","").split(', ')
    esp = request.GET.get('esp')
    especialidad = request.GET.get('especialidad')
    fecha = request.GET.get('fecha')
    id_seleccions = request.GET.get('id_seleccions')
    listareservas = {"lista":lista, "lista_reserva":lista_reserva,
    "especialidad":especialidad, "hora_seleccion":hora_seleccion}
    
    if Cita.objects.filter(ID_Cita=id_seleccions).exists():
        esp_cit = Cita.objects.get(ID_Cita=id_seleccions)
    else:
        esp_cit = CitaSinUsuario.objects.get(ID_Cita=id_seleccions)
    

    if request.method == 'POST':
        valor = request.POST.get('hora_agendar')
        esp_cit.Fecha_Cita = fecha
        esp_cit.Hora_Cita = valor
        esp_cit.save()

        context = {'valor':valor , 'fecha':fecha}
        messages.success(request,"Cita cambiada exitosamente.")
        return render(request, 'Clientes/cliente_Hora_creada.html', context)
        # url = reverse('index')
        # return redirect(url)

    return render(request, 'Operador/Modificar_Cita/operador_modificar_fecha.html',listareservas)

def operador_confirmacion(request):
    consulta_rut  = ConsultarRut()
    context = {"consulta_rut":consulta_rut}
    citas_usuarios = None
    citas_sin_usuario = None
    especialidad_ = None
    especialidad_sin = None

    hoy = date.today()
    dia_escrito = hoy.strftime('%A').replace('Monday','lun').replace('Tuesday','mar').replace('Wednesday','mie').replace('Thursday','jue').replace('Friday','vie').replace('Saturday','sab').replace('Sunday','dom')
    
    #TODO MEJORAR FILTRO DE ESPECIALIDAD
    if request.method == 'POST':
        print(dia_escrito)
        valor = request.POST.get('rut')
        # api_response = respuesta_api(request, valor)
        if  Paciente.objects.filter(Rut = valor).exists():
            paciente = Paciente.objects.get(Rut = valor)
            pac_usuario = paciente.Usuario_P
            print(paciente)
            print(pac_usuario)
            
            if Cita.objects.filter(ID_Cliente = pac_usuario, Fecha_Cita = hoy).exists():
                print('entre al if cita')
                citas_usuarios = Cita.objects.filter(ID_Cliente = pac_usuario, Fecha_Cita = hoy)
                especialista_con = Especialista.objects.get(ID_Especialista = citas_usuarios[0].ID_Especialista.ID_Especialista)
                if dia_escrito in especialista_con.Dia_Esp_P:
                    especialidad_ = especialista_con.Especialidad_P
                else:
                    especialidad_ = especialista_con.Especialidad_S

            print(CitaSinUsuario.objects.filter(Rut_Paciente = valor).exists())
            if CitaSinUsuario.objects.filter(Rut_Paciente = valor).exists():
                citas_sin_usuario = CitaSinUsuario.objects.filter(Rut_Paciente = valor, Fecha_Cita = hoy)
                
                especialista = Especialista.objects.get(ID_Especialista = citas_sin_usuario[0].ID_Especialista.ID_Especialista)
                if dia_escrito in especialista.Dia_Esp_P:
                    especialidad_sin = especialista.Especialidad_P
                else:
                    especialidad_sin = especialista.Especialidad_S
            print(citas_usuarios)
            print(citas_sin_usuario)
            print(Paciente.objects.filter(Rut = valor).exists() and citas_usuarios is None and citas_sin_usuario is None)
            if Paciente.objects.filter(Rut = valor).exists() and citas_usuarios is None and citas_sin_usuario is None:
                messages.error(request, "El rut ingresado no tiene ninguna cita agendada.")
                return render(request, 'Operador/Confirmacion/operador_confirmar_paciente.html')
        else:

            if request.method == 'POST':
                print('Estoy en el post de seleccion')
                cita = request.POST.get('cita_hidden')
                print(cita)
                print(type(cita))
                cita = cita.replace("de ","").replace("a las ","")
                cita = cita.replace('Enero','January').replace('Febrero','February').replace('Marzo','March').replace('Abril','April').replace('Mayo','May').replace('Junio','June').replace('Julio','July').replace('Agosto','August').replace('Septiembre','September').replace('Octubre','October').replace('Noviembre','November').replace('Diciembre','December')
                print(f'Cual es la cita {cita}')
                cita = datetime.strptime(cita, "%d %B %Y %H:%M")
                print(f'Cita replace {cita}')
                if Cita.objects.filter(ID_Cita = cita).exists():
                    cita_confirmada = Cita.objects.get(ID_Cita = cita)
                    print(f'Verificando {cita_confirmada}')
                    print(cita_confirmada.Confirmacion_Cita_Operador)
                    cita_confirmada.Confirmacion_Cita_Operador = True
                    print(f'Verificando cambio de {cita_confirmada}')
                    print(cita_confirmada.Confirmacion_Cita_Operador)
                    nom_pac= cita_confirmada.ID_Cliente
                    cita_confirmada.save()
                    messages.success(request, "Paciente confirmado.")
                    id_cobro = Cobro.objects.all().count()+1
                    rut = Paciente.objects.get(Usuario_P = nom_pac).Rut
                    esp = cita_confirmada.ID_Especialista
                    especialista = Especialista.objects.get(Nombre_completo_E = esp)

                    #Obtener especialidad
                    hoy = date.today()
                    #Remplaso el dia en ingles por el valor que le indicamos en el modelo.
                    hoy = hoy.strftime('%A').replace('Monday','lun').replace('Tuesday','mar').replace('Wednesday','mie').replace('Thursday','jue').replace('Friday','vie').replace('Saturday','sab').replace('Sunday','dom')

                    #Cobro de especialidades
                    cobro_especialidad = CobrosEspecialistas.objects.get(ID_Especialista = especialista)

                    #Valida si el dia se encuentra en alguna de de las listas de dias de la especialidad y el cobro de ella
                    if hoy in especialista.Dia_Esp_P:
                        especialidad = especialista.Especialidad_P
                        cobro_atencion = cobro_especialidad.Monto_Esp_P
                        print(f'Valor de hoy {hoy}')
                    else:
                        especialidad = especialista.Especialidad_S
                        cobro_atencion = cobro_especialidad.Monto_Esp_S
                        print(f'Valor de hoy {hoy} dentro del else')


                    print(f'Especialista encontrado :{especialista}')
                    print(f'Rut del paciente: {rut}')
                    metodo = cita_confirmada.Metodo_Pago_Cita

                    cobro_cita =  Cobro.objects.create(ID_Cobro = id_cobro, Rut_Pac_Cobro = rut, Especialista_Cobro=especialista,
                                                    Especialidad_Cobro = especialidad, Monto = cobro_atencion, Metodo = metodo, Estado_cobro='Por pagar')
                    
                    id_cobro = cobro_cita.ID_Cobro

                    redireccion_confirmar = request.POST.get('redireccion_confirmar')
                    print(f'Valor redirect: {redireccion_confirmar}')
                    if redireccion_confirmar == "1":
                        print('redireccion_confirmar if')
                        url = reverse('operador_pagar')+"?id_cobro={}&rut={}&metodo={}".format(id_cobro, rut, metodo)
                        return redirect(url)
                    else:
                        print('redireccion_confirmar else')
                        url = reverse('confirmacion')
                        return redirect(url) 
                    return redirect('confirmacion')
                else:
                    cita_confirmada = CitaSinUsuario.objects.get(ID_Cita = cita)
                    cita_confirmada.Confirmacion_Cita_Operador = True
                    cita_confirmada.save()
                    messages.success(request, "Paciente confirmado.")
                    id_cobro = Cobro.objects.all().count()+1
                    rut = Paciente.objects.get(Usuario_P = nom_pac).Rut
                    esp = cita_confirmada.ID_Especialista
                    especialista = Especialista.objects.get(Nombre_completo_E = esp)

                    #Obtener especialidad
                    hoy = date.today()
                    #Remplaso el dia en ingles por el valor que le indicamos en el modelo.
                    hoy = hoy.strftime('%A').replace('Monday','lun').replace('Tuesday','mar').replace('Wednesday','mie').replace('Thursday','jue').replace('Friday','vie').replace('Saturday','sab').replace('Sunday','dom')

                    #Cobro de especialidades
                    cobro_especialidad = CobrosEspecialistas.objects.get(ID_Especialista = especialista)

                    #Valida si el dia se encuentra en alguna de de las listas de dias de la especialidad y el cobro de ella
                    if hoy in especialista.Dia_Esp_P:
                        especialidad = especialista.Especialidad_P
                        cobro_atencion = cobro_especialidad.Monto_Esp_P
                        print(f'Valor de hoy {hoy}')
                    else:
                        especialidad = especialista.Especialidad_S
                        cobro_atencion = cobro_especialidad.Monto_Esp_S
                        print(f'Valor de hoy {hoy} dentro del else')


                    print(f'Especialista encontrado :{especialista}')
                    print(f'Rut del paciente: {rut}')
                    metodo = cita_confirmada.Metodo_Pago_Cita

                    cobro_cita =  Cobro.objects.create(ID_Cobro = id_cobro, Rut_Pac_Cobro = rut, Especialista_Cobro=especialista,
                                                    Especialidad_Cobro = especialidad, Monto = cobro_atencion, Metodo = metodo, Estado_cobro='Por pagar')
                    
                    id_cobro = cobro_cita.ID_Cobro

                    redireccion_confirmar = request.POST.get('redireccion_confirmar')
                    print(f'Valor redirect: {redireccion_confirmar}')
                    if redireccion_confirmar == "1":
                        print('redireccion_confirmar if')
                        url = reverse('operador_pagar')+"?id_cobro={}&rut={}&metodo={}".format(id_cobro, rut, metodo)
                        return redirect(url)
                    else:
                        print('redireccion_confirmar else')
                        url = reverse('confirmacion')
                        return redirect(url)
                    return redirect('confirmacion')
            messages.error(request, "El rut ingresado no figura en el sistema.")
            return render(request, 'Operador/Confirmacion/operador_confirmar_paciente.html', context)
        # if Paciente.objects.filter(Rut = valor).exists():
        #     pacientes = Paciente.objects.get(Rut = valor)
        #     citas_usuarios = Cita.objects.filter(ID_Cliente = pacientes.Usuario_P, Fecha_Cita = hoy)
        #     print(citas_usuarios)
        #     especialista_con = Especialista.objects.get(ID_Especialista = citas_usuarios[0].ID_Especialista.ID_Especialista)
        #     print(especialista_con)

        #     if dia_escrito in especialista_con.Dia_Esp_P:
        #         especialidad_ = especialista_con.Especialidad_P
        #     else:
        #         especialidad_ = especialista_con.Especialidad_S
    
        #     print(f'Citas con usuario  {citas_usuarios} ')
        #     print(f'Especialidad con usuario: {especialidad_}')

        #     if CitaSinUsuario.objects.filter(Rut_Paciente = valor).exists():
        #         citas_sin_usuario = CitaSinUsuario.objects.filter(Rut_Paciente = valor, Fecha_Cita = hoy)
        #         especialista = Especialista.objects.get(ID_Especialista = citas_sin_usuario[0].ID_Especialista.ID_Especialista)
            
        #         print(especialista)
        #         if dia_escrito in especialista.Dia_Esp_P:
        #             especialidad_sin = especialista.Especialidad_P
        #         else:
        #             especialidad_sin = especialista.Especialidad_S

        #         print(f'Citas con usuario y sin {citas_usuarios} {citas_sin_usuario}')
        #         print(f'Especialidad sin usuario dentro del if con usuario: {especialidad_sin}')

        #     if Paciente.objects.filter(Rut = valor).exists() and len(citas_usuarios) == 0:
        #         messages.error(request, "El rut ingresado no tiene ninguna cita agendada.")
        #         return render(request, 'Operador/Confirmacion/operador_confirmar_paciente.html')

        # elif CitaSinUsuario.objects.filter(Rut_Paciente = valor).exists():
        #     citas_sin_usuario = CitaSinUsuario.objects.filter(Rut_Paciente = valor, Fecha_Cita = hoy)
        #     especialista = Especialista.objects.get(ID_Especialista = citas_sin_usuario[0].ID_Especialista.ID_Especialista)
            
        #     print(f'Especialista {especialista}')

        #     if dia_escrito in especialista.Dia_Esp_P:
        #         especialidad_sin = especialista.Especialidad_P
        #     else:
        #         especialidad_sin = especialista.Especialidad_S

        #     print(f'Citas sin usuario {citas_sin_usuario}')
        #     print(f'Especialidad con usuario: {especialidad_sin}')
        
        
        # elif CitaSinUsuario.objects.filter(Rut_Paciente = valor).exists() and Paciente.objects.filter(Rut = valor).exists() and citas_usuarios is None and citas_sin_usuario is None:
        #     messages.error(request, "El rut ingresado no tiene ninguna cita agendada.")
        #     return render(request, 'Operador/Confirmacion/operador_confirmar_paciente.html')
        

        #TODO ARREGLAR LOGICA
        # else:
        #     if 'seleccion' in request.POST:
        #         print('Estoy en el post de seleccion')
        #         cita = request.POST.get('seleccion')
        #         print(type(cita))
        #         cita = cita.replace("de ","").replace("a las ","")
        #         cita = cita.replace('Enero','January').replace('Febrero','February').replace('Marzo','March').replace('Abril','April').replace('Mayo','May').replace('Junio','June').replace('Julio','July').replace('Agosto','August').replace('Septiembre','September').replace('Octubre','October').replace('Noviembre','November').replace('Diciembre','December')
        #         print(f'Cual es la cita {cita}')
        #         cita = datetime.strptime(cita, "%d %B %Y %H:%M")
        #         print(f'Cita replace {cita}')

        #         if Cita.objects.filter(ID_Cita = cita).exists():
        #             cita_confirmada = Cita.objects.get(ID_Cita = cita)
        #             cita_confirmada.Confirmacion_Cita_Operador = True
        #             cita_confirmada.save()
        #             messages.success(request, "Paciente confirmado.")
        #             return redirect('confirmacion')
        #         else:
        #             cita_confirmada = CitaSinUsuario.objects.get(ID_Cita = cita)
        #             cita_confirmada.Confirmacion_Cita_Operador = True
        #             cita_confirmada.save()
        #             messages.success(request, "Paciente confirmado.")
        #             return redirect('confirmacion')
                
        #     messages.error(request, "No se encontraron citas con el rut ingresado.")  
        #     return render(request, 'Operador/Confirmacion/operador_confirmar_paciente.html', context)

        # context = {'citas':citas_usuarios, 'citas_sin_usuario':citas_sin_usuario}
        # url = reverse('confirmacion_citas') + '?cita={}&citas_sin_usuario={}&valor={}'.format(citas_usuarios, citas_sin_usuario, valor)
        # return redirect(url)
        context = {'citas':citas_usuarios, 'citas_sin_usuario':citas_sin_usuario, 'especialidad_sin':especialidad_sin, 'especialidad_':especialidad_}
        
        return render(request, 'Operador/Confirmacion/operador_citas_paciente.html', context)


    return render(request, 'Operador/Confirmacion/operador_confirmar_paciente.html', context)
    

    #TODO Solicitar a cristian una api chilena que me permita traer los datos de chile
# def respuesta_api(request,rut):
#     url = f'https://api.libreapi.cl/rut/activities/?rut={rut}'
#     print(url)
    
#     response = requests.get(url)
    
#     print(response)
#     print(f"La respuesta tiene el código de estado {response.status_code}")
#     print(f"La respuesta tiene el siguiente contenido: {response.text}")
#     if response.ok:
#         print('Dentro del if')
#         data = response.json()
#         print(f'respuesta de json {data}')
#         return JsonResponse(data)
#     else:
#         print('Dentro del else')
#         return JsonResponse({'error': 'An error occurred while processing your request.'})

def operador_confirmacion_citas(request):
    # citas_usuarios = request.GET.get('citas_usuarios')
    # if citas_usuarios is None:
    #     citas_sin_usuario = request.GET.get('citas_sin_usuario').replace("'","").replace("[","").replace("]","").split(', ')
    # else:
    #     citas_usuarios = citas_usuarios.replace("'","").replace("[","").replace("]","").split(', ')
    #     citas_sin_usuario = request.GET.get('citas_sin_usuario').replace("'","").replace("[","").replace("]","").split(', ')
    
    # print(citas_usuarios)
    # print(citas_sin_usuario)
    # valor = request.GET.get('valor')

    # context = {'citas':citas_usuarios, 'citas_sin_usuario':citas_sin_usuario}
    
    return render(request, 'Operador/Confirmacion/operador_citas_paciente.html')

def operador_boleta(request):
    return render(request,'Operador/Pago/operador_boleta.html')

def operador_pago(request):
    if request.method == "POST":
        rut = request.POST.get('rut')
        #utilizo flag para validar si existe algun cobro para redirigir en caso de exista o no un cobro
        flag = Cobro.objects.filter(Rut_Pac_Cobro=rut)
        if flag:
            url = reverse('cobros_paciente')+"?rut={}".format(rut)
            return redirect(url)
        else:
            messages.error(request,'El rut ingresado no figura con cobros')
            return render(request,'Operador/Pago/operador_pago.html')
        
    return render(request,'Operador/Pago/operador_pago.html')

def operador_pago_cobros(request):
    rut = request.GET.get('rut')
    cobro = Cobro.objects.filter(Rut_Pac_Cobro = rut)

    print(rut)
    print(cobro)
    context = {"cobro":cobro}
    if request.method == 'POST':
        id_cobro = request.POST.get('id_cobro')
        if 'redirect_boleta' in request.POST:
            c = canvas.Canvas("prueba_boleta.pdf", pagesize=A4)
            hello(c)
            url = reverse('boleta')+"?id_cobro={}&rut={}".format(id_cobro,rut)
            return redirect(url)
        print(f'post de operador pagos {id_cobro}')
        url = reverse('operador_pagar')+"?id_cobro={}&rut={}".format(id_cobro,rut)
        return redirect(url)
    return render(request,'Operador/Pago/operador_pago_cobros.html',context)

def operador_pagar(request):
    rut = request.GET.get('rut')
    print(f'rut {rut}')
    id_cobro = request.GET.get('id_cobro')
    print(f'Id cobro {id_cobro}')
    # metodo = request.GET.get('metodo')
    # print(f'Metodo: {metodo}')
    cobro = Cobro.objects.get(ID_Cobro = id_cobro)
    esp_cob = cobro.Especialista_Cobro
    especialidad_cob = cobro.Especialidad_Cobro
    monto = cobro.Monto
    metodo = cobro.Metodo
    hoy = date.today()

    print(f'cobro {cobro}')
    id_boleta = Boleta.objects.all().count()+1
    form_pago = FormBoleta()
    form_pago.fields['Id_boleta'].initial = id_boleta
    form_pago.fields['Rut_boleta'].initial = rut
    form_pago.fields['Especialista_boleta'].initial = esp_cob
    form_pago.fields['Especialidad_boleta'].initial = especialidad_cob
    form_pago.fields['Monto_boleta_form'].initial = monto
    form_pago.fields['Fecha_emision_form'].initial = hoy
    form_pago.fields['Monto_efectivo'].initial = 0
    form_pago.fields['Arancel_form'].initial = 0
    form_pago.fields['Num_Doc'].initial = 0
    form_pago.fields['Vuelto_bol'].initial = 0
    form_pago.fields['Tipo_atencion_form'].initial = metodo

    context = {"cobro":cobro, "form_pago":form_pago}

    #TODO ARREGLAR EL TEMPLATE OPERADOR_PAGAR / NO OCULTA EL MONTO EN EFECTIVO

    if request.method == "POST":

        metodo_pago_boleta = request.POST.get('Metodo_pago_form')
        print('En el POST')    
        #Valido el metodo de pago primero
        if metodo_pago_boleta == 'Efectivo':
            monto_boleta = request.POST.get('Monto_boleta_form')
            monto_efectivo_boleta = request.POST.get('Monto_efectivo')
            atencion = request.POST.get('Tipo_atencion_form')
            print(f'Monto Boleta: {monto_boleta}')
            print(f'Monto Efectivo: {monto_efectivo_boleta}')
            print(atencion)
            if atencion !='Particular':
                print(f'estoy en atencion {atencion}')
                form_pago = FormBoleta(data=request.POST)

                print(form_pago.is_valid())
                if form_pago.is_valid():
                    form_pago.save()
                    cobro.Estado_cobro = 'Pagado'
                    cobro.save()
                    messages.success(request, "Operacion Exitosa")
                    url = reverse('cobros_paciente')+"?rut={}".format(rut)
                    return redirect(url) 
                
            elif monto_efectivo_boleta < monto_boleta:
                print('Dentro del if')
                messages.error(request, "El monto de efectivo debe ser superior al monto a pagar")
                return render(request, 'Operador/Pago/operador_pagar.html',context)
            else:
                form_pago = FormBoleta(data=request.POST)

                print(form_pago.is_valid())
                if form_pago.is_valid():
                    
                    form_pago.cleaned_data['Vuelto_bol'] = int(monto_efectivo_boleta) - int(monto_boleta)
                    form_pago.cleaned_data['Monto_efectivo'] = int(monto_efectivo_boleta)
                    form_pago.save()
                    cobro.Estado_cobro = 'Pagado'
                    cobro.save()
                    messages.success(request, "Operacion Exitosa")
                    url = reverse('cobros_paciente')+"?rut={}".format(rut)
                    return redirect(url) 
                

    return render(request,'Operador/Pago/operador_pagar.html',context)

def operador_pago_fonasa(request):
    if request.method == "POST":
        rut = request.POST.get('rut')
        url = reverse('cobros_paciente')+"?rut={}".format(rut)
        return redirect(url)
    return render(request,'Operador/Pago/operador_pago_particular.html')
