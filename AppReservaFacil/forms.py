from django import forms
from django.contrib.auth.forms import *
from django.contrib.auth.models import *
from django.contrib import messages
from .models import *
from django.core.exceptions import ValidationError
from django.forms.widgets import *
from datetime import date
from django.utils.safestring import mark_safe
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


today = date.today()
max = today.replace(today.year+ 1)
# Create your forms here.

DIAS_CHOICES=[('lun','Lunes'),('mar','Martes'),('mie','Miercoles'),('jue','Jueves'),('vie','Viernes'),('sab','Sabado'),('dom','Domingo')]
MINUTOS_CHOICES=[(None,'--------'),(15,'15 Minutos'),(30,'30 Minutos'),(45,'45 Minutos'),(60,'60 Minutos')]
SEXO_CHOICES=[('Femenino','Femenino'), ('Masculino','Masculino')]
TIPO_ATENCION = [('Particular','Particular'),('Fonasa','Fonasa'),('Isapre','Isapre'),('Convenio','Convenio'),('Otros','Otros')]

class FormEspecialidad(forms.Form):
    nombre_especialidad = forms.CharField(max_length=256)
    area_medica_f = forms.ModelChoiceField(queryset=Area_Medica.objects.all(), initial=0)

    def save(self):

        crearEsp = Especialidad.objects.create(
            Nombre_especialidad = self.cleaned_data['nombre_especialidad'],
            Area_Medica_F = self.cleaned_data['area_medica_f']
        )
        return crearEsp


class FormEspecialista(forms.Form):
    nom_com_especialista = forms.CharField(max_length=256)
    rut = forms.CharField(max_length=9)
    sexo = forms.ChoiceField(choices = ([('Femenino','Femenino'), ('Masculino','Masculino')]), required=True,initial=0)
    fecha_nac_especialista = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    direccion_especialista = forms.CharField(max_length=256)
    contacto_especialista = forms.CharField(max_length=9)
    ini_con_especialista = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    fin_con_especialista = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    Foto_E = forms.ImageField(required=False)
    especialidad_p = forms.ModelChoiceField(queryset=Especialidad.objects.all() ,initial=0)
    especialidad_s = forms.ModelChoiceField(queryset=Especialidad.objects.all() ,initial=0,required=False)
    dia_p = forms.CharField(widget=forms.CheckboxSelectMultiple(choices=DIAS_CHOICES, attrs={'class':'boton'}))
    dia_s = forms.CharField(required=False, widget=forms.CheckboxSelectMultiple(choices=DIAS_CHOICES, attrs={'class':'boton'}))
    Minutes_Esp_P_Lun = forms.ChoiceField(choices=MINUTOS_CHOICES, initial=0)
    Minutes_Esp_P_Mar = forms.ChoiceField(required=False, choices=MINUTOS_CHOICES, initial=0)
    Minutes_Esp_P_Mie = forms.ChoiceField(required=False, choices=MINUTOS_CHOICES, initial=0)
    Minutes_Esp_P_Jue = forms.ChoiceField(required=False, choices=MINUTOS_CHOICES, initial=0)
    Minutes_Esp_P_Vie = forms.ChoiceField(required=False, choices=MINUTOS_CHOICES, initial=0)
    Minutes_Esp_P_Sab = forms.ChoiceField(required=False, choices=MINUTOS_CHOICES, initial=0)
    Minutes_Esp_P_Dom = forms.ChoiceField(required=False, choices=MINUTOS_CHOICES, initial=0)
    Minutes_Esp_S_Lun = forms.ChoiceField(required=False, choices=MINUTOS_CHOICES, initial=0)
    Minutes_Esp_S_Mar = forms.ChoiceField(required=False, choices=MINUTOS_CHOICES, initial=0)
    Minutes_Esp_S_Mie = forms.ChoiceField(required=False, choices=MINUTOS_CHOICES, initial=0)
    Minutes_Esp_S_Jue = forms.ChoiceField(required=False, choices=MINUTOS_CHOICES, initial=0)
    Minutes_Esp_S_Vie = forms.ChoiceField(required=False, choices=MINUTOS_CHOICES, initial=0)
    Minutes_Esp_S_Sab = forms.ChoiceField(required=False, choices=MINUTOS_CHOICES, initial=0)
    Minutes_Esp_S_Dom = forms.ChoiceField(required=False, choices=MINUTOS_CHOICES, initial=0)
    
class FormOperador(forms.Form):
    nom_com_operador = forms.CharField(max_length=256)
    rut = forms.CharField(max_length=9)
    sexo = forms.ChoiceField(choices = (SEXO_CHOICES), required=True,initial=0)
    email_o = forms.EmailField()
    fecha_nac_operador = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    direccion_operador = forms.CharField(max_length=256)
    contacto_operador = forms.CharField(max_length=9)
    fecha_ini_con_operador = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    fecha_fin_con_operador = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    foto_o = forms.ImageField(required = False)
    
class FormPaciente(forms.Form):
    nom_com_pac = forms.CharField(max_length=256)
    rut_pac = forms.CharField(max_length=9)
    sexo_pac = forms.ChoiceField(choices= SEXO_CHOICES, required = True, initial = 0)
    fecha_nac_pac = forms.DateField(widget=NumberInput(attrs={'type':'date'}))
    direccion_pac = forms.CharField(max_length=256)
    telefono_pac = forms.CharField(max_length=9)

    def save(self, usuario):  
        user = User.objects.get(username = usuario)
        grupo_Pacientes = Group.objects.get(name='Pacientes') 
        user.groups.add(grupo_Pacientes)
        Usuario_P = User.objects.get(username = usuario)
        PacienteM = Paciente.objects.create(  
            ID_Paciente = Paciente.objects.all().count()+1,
            Usuario_P = Usuario_P
            
        )
        return PacienteM  

class FormPacienteSinUser(forms.Form):
    rut_pac = forms.CharField(max_length=9)
    email_pac = forms.EmailField(label='email')
    telefono_pac = forms.IntegerField()
    metodo_pago = forms.ChoiceField(choices=TIPO_ATENCION)



class FormRegistrarUsuario(forms.Form):
    username = forms.CharField(label='username', min_length=5, max_length=150)  
    email = forms.EmailField(label='email')  
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)  
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    

    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        new = User.objects.filter(username = username)  
        if new.count() > 0:  
            raise ValidationError("Usuario ya existe")  
        return username  
  
    def email_clean(self):  
        email = self.cleaned_data['email'].lower()  
        new = User.objects.filter(email=email)  
        if new.count() > 0:  
            raise ValidationError("Correo ya usado")  
        return email  
  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Contraseñas no son iguales")  
        return password2  
  
    def save(self, commit = True):  
        user = User.objects.create_user(  
            self.cleaned_data['username'],  
            self.cleaned_data['email'],  
            self.cleaned_data['password1']  
        )  
        return user  
    
class FormRegistrarCobros(forms.Form):
    monto_esp_s = forms.IntegerField(required=False)
    monto_esp_p = forms.IntegerField(required=False)
    id_especialista = forms.CharField(max_length=256,required=True)

    def save(self):

        cobroreg = CobrosEspecialistas.objects.create(
            ID_Especialista = Especialista.objects.get(ID_Especialista = Especialista.objects.get(Nombre_completo_E = self.cleaned_data['id_especialista']).ID_Especialista),
        )
        return cobroreg

class DateInput(forms.DateInput):
    input_type = 'date'

class LoginUsuario(AuthenticationForm):
    pass

class DateForm(forms.Form):
    date = forms.DateField(
    widget=DateInput(attrs={"name":"somdate", "value":today, "min": today, "max":max})
    )

class ConsultarRut(forms.Form):
    rut_consulta = forms.CharField(max_length=9)    

class AgendarForm(forms.Form):
    area_medica_a = forms.ModelChoiceField(queryset=Area_Medica.objects.all())
    especialidad_a = forms.ModelChoiceField(queryset=Especialidad.objects.none())
    metodo_pago = forms.ChoiceField(choices=TIPO_ATENCION)

class FormMensaje(forms.Form):
    texto = forms.CharField(max_length=256)

class FormFichaMedica(forms.Form):
    RUT_Pac =  forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'form-control'}),max_length=9, required=True)
    Nombre_Com_Pac = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'form-control'}),max_length = 256, required=True)
    Direccion_Pac = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'form-control'}),max_length=256, required=False)
    Telefono_Pac = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'form-control'}),max_length=9, required=False)
    Sis_Sal_Pac = forms.ChoiceField(choices = SISTEMA_SALUD, required=False, initial = 'SegCom')
    Grupo_Sanguineo = forms.ChoiceField(choices=GRUPO_SANGUINEO, required=False, initial = 'Amas')
    Al_Antibioticos = forms.BooleanField(required=False)
    Antibioticos_TI = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length = 256, required=False)
    Al_Medicamentos = forms.BooleanField(required=False)
    Medicamentos_TI = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length = 256, required=False)
    Al_Alimentos = forms.BooleanField(required=False)
    Alimentos_TI = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length = 256, required=False)
    Al_Ani_Ins = forms.BooleanField(required=False)
    Ani_Ins_TI = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length = 256, required=False)
    Enf_Cronic = forms.BooleanField(required=False)
    Enf_Cronic_TI = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length = 256, required=False)
    Observaciones_Ficha = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 150}), required=False)

class FormReceta(forms.Form):
    Especialista_receta = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'form-control'}))
    Especialidad_receta = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'form-control'}))
    Rut_esp_receta = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'form-control'}),max_length = 9, required=True)
    Nompre_pac_receta = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'form-control'}),max_length = 256, required=True)
    Rut_pac_receta = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'form-control'}),max_length = 9, required=True)
    Edad_pac_receta = forms.IntegerField(widget=forms.NumberInput (attrs={'readonly': 'readonly','class': 'form-control'}))
    Direccion_pac_receta = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'form-control'}),max_length = 256, required=True)
    Diagnostico_pac_receta = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),max_length = 80, required=True)
    Descripcion_receta = forms.CharField(widget=forms.Textarea(attrs={'rows': 10  , 'cols': 120}),required=True)

    # CitaMedica = Ficha_Cita.objects.create(  
    #         ID_Ficha_Cita = Ficha_Cita.objects.all().count()+1,
    #         Fecha_Cita = self.cleaned_data['Fecha_Cita'],
    #         Ficha_Medica_Pac = Ficha_Medica.objects.get(ID_Ficha_Medica=self.cleaned_data['Ficha_Medica_Pac']) ,
    #         RUT_Pac = self.cleaned_data['RUT_Pac'],
    #         Nombre_Com_Pac = Paciente.objects.get(Nombre_Paciente=self.cleaned_data['Nombre_Com_Pac']),
    #         Nombre_Com_Esp = Especialista.objects.get(Nombre_completo_E=self.cleaned_data['Nombre_Com_Esp']),
    #         Diagnostico_Cita = self.cleaned_data['Diagnostico_Cita'],


    def save(self):
        esp = Especialista.objects.get(Nombre_completo_E =  self.cleaned_data['Especialista_receta'])
        
        especi = Especialidad.objects.get(Nombre_especialidad = self.cleaned_data['Especialidad_receta'])
        
        RecetaMedica = Receta.objects.create(
            Numero_receta = Receta.objects.all().count()+1,
            Especialista_receta = esp,
            Especialidad_receta = especi,
            Rut_esp_receta = self.cleaned_data['Rut_esp_receta'],
            Nompre_paciente_receta = self.cleaned_data['Nompre_pac_receta'],
            Rut_pac_receta = self.cleaned_data['Rut_pac_receta'],
            Edad_pac_receta = self.cleaned_data['Edad_pac_receta'],
            Direccion_pac_receta = self.cleaned_data['Direccion_pac_receta'],
            Diagnostico_rec = self.cleaned_data['Diagnostico_pac_receta'],
            Descripcion_receta =self.cleaned_data['Descripcion_receta']
        )
        return RecetaMedica
    

class FormExamenes(forms.Form):
    nombre_pac = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'input border-0 border-bottom'}),max_length=256, required=True)
    rut_pac = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'input border-0 border-bottom'}),max_length=9, required=True)
    edad_pac = forms.IntegerField(widget=forms.NumberInput (attrs={'readonly': 'readonly','class': 'input border-0 border-bottom'}))
    Fecha_Cita = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'input border-0 border-bottom'}), required=True)
    prevision = forms.CharField(widget=forms.Select(choices=TIPO_ATENCION, attrs={'class': 'input border-0 border-bottom'}),max_length = 80, required=True)
    servicio = forms.CharField(widget=forms.TextInput(attrs={'class': 'input border-0 border-bottom'}),max_length = 80, required=True)
    diagnostico = forms.CharField(widget=forms.TextInput(attrs={'class': 'input border-0 border-bottom'}),max_length = 80, required=True)
    nombre_medico = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'input border-0 border-bottom'}),max_length=256, required=True)
    rut_medico = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'input border-0 border-bottom'}),max_length=9, required=True)
    examenes = forms.CharField(widget=forms.CheckboxSelectMultiple(choices=EXAMENES, attrs={'class':'boton'}))
    # examenes = forms.MultipleChoiceField(widget=forms.TextInput(attrs={'class': 'input border-0 border-bottom'}))

    def save(self):
        OrdenExamenes = Examene.objects.create(
            Numero_orden_examen = Examene.objects.all().count()+1,
            Nombre_pac_orden = self.cleaned_data['nombre_pac'],
            Rut_pac_orden = self.cleaned_data['rut_pac'],
            Edad_pac_orden = self.cleaned_data['edad_pac'],
            Fecha_nac_pac_orden = self.cleaned_data['Fecha_Cita'],
            Prevision_pac_orden = self.cleaned_data['prevision'],
            Servicio_pac_orden = self.cleaned_data['servicio'],
            Diagnostico_orden = self.cleaned_data['diagnostico'],
            Nombre_Medico_orden = self.cleaned_data['nombre_medico'],
            Rut_Medico_orden = self.cleaned_data['rut_medico'],
            Examenes = self.cleaned_data['examenes'].replace("'","").strip('][').split(', ')
        )
        return OrdenExamenes



class FormCitaMedica(forms.Form):
    Ficha_Medica_Pac = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'form-control'}),max_length=9, required=True)
    Fecha_Cita = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'form-control'}), required=True)
    RUT_Pac = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'form-control'}),max_length=9, required=True)
    Nombre_Com_Pac = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'form-control'}),max_length = 256, required=True)
    Nombre_Com_Esp = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'form-control'}),max_length = 256, required=True)
    Diagnostico_Cita = forms.CharField(widget=forms.Textarea(attrs={'rows': 10  , 'cols': 120}), required=False)

    def save(self):
        CitaMedica = Ficha_Cita.objects.create(  
            ID_Ficha_Cita = Ficha_Cita.objects.all().count()+1,
            Fecha_Cita = self.cleaned_data['Fecha_Cita'],
            Ficha_Medica_Pac = Ficha_Medica.objects.get(ID_Ficha_Medica=self.cleaned_data['Ficha_Medica_Pac']) ,
            RUT_Pac = self.cleaned_data['RUT_Pac'],
            Nombre_Com_Pac = Paciente.objects.get(Nombre_Paciente=self.cleaned_data['Nombre_Com_Pac']),
            Nombre_Com_Esp = Especialista.objects.get(Nombre_completo_E=self.cleaned_data['Nombre_Com_Esp']),
            Diagnostico_Cita = self.cleaned_data['Diagnostico_Cita'],
        )

        return CitaMedica  
    
    def update(self, cita_id):
        cita_medica = Ficha_Cita.objects.get(ID_Ficha_Cita = cita_id)
        cita_medica.Fecha_Cita = self.cleaned_data['Fecha_Cita']
        cita_medica.Ficha_Medica_Pac = Ficha_Medica.objects.get(ID_Ficha_Medica=self.cleaned_data['Ficha_Medica_Pac'])
        cita_medica.RUT_Pac = self.cleaned_data['RUT_Pac']
        cita_medica.Nombre_Com_Pac = Paciente.objects.get(Nombre_Paciente=self.cleaned_data['Nombre_Com_Pac'])
        cita_medica.Nombre_Com_Esp = Especialista.objects.get(Nombre_completo_E=self.cleaned_data['Nombre_Com_Esp'])
        cita_medica.Diagnostico_Cita = self.cleaned_data['Diagnostico_Cita']
        cita_medica.save()
        return cita_medica
        

class FormBoleta(forms.Form):
    Id_boleta = forms.IntegerField(widget=forms.NumberInput (attrs={'readonly': 'readonly','class': 'form-control'}))
    Rut_boleta = forms.CharField(widget=forms.TextInput (attrs={'readonly': 'readonly','class': 'form-control'}))
    Especialista_boleta = forms.CharField(widget=forms.TextInput (attrs={'readonly': 'readonly','class': 'form-control'}))
    Especialidad_boleta = forms.CharField(widget=forms.TextInput (attrs={'readonly': 'readonly','class': 'form-control'}))
    Monto_boleta_form = forms.IntegerField(widget=forms.NumberInput (attrs={'readonly': 'readonly','class': 'form-control'}))
    Fecha_emision_form = forms.DateField(widget=forms.DateInput(attrs={'readonly': 'readonly', 'class': 'form-control'}))
    Metodo_pago_form = forms.ChoiceField(choices=METODO_PAGO)
    Monto_efectivo = forms.IntegerField()
    Tipo_atencion_form = forms.ChoiceField(choices=TIPO_ATENCION)
    Arancel_form = forms.DecimalField()
    Num_Doc = forms.IntegerField()
    Vuelto_bol = forms.IntegerField()

    def save(self):
        Nombre_especialista = self.cleaned_data['Especialista_boleta']
        Especialista_N = Especialista.objects.get(Nombre_completo_E=Nombre_especialista).ID_Especialista
        Nombre_especialidad = self.cleaned_data['Especialidad_boleta']
        Especialidad_N = Especialidad.objects.get(Nombre_especialidad=Nombre_especialidad).Codigo_especialidad
        print(f'dentro del save {Especialista_N}')
        print(type(Especialista_N))
        print(f'dentro del save {Especialidad_N}')
        print(type(Especialidad_N))
        BoletaServicio = Boleta.objects.create(
            ID_Boleta = self.cleaned_data['Id_boleta'],
            Rut_Pac_Boleta = self.cleaned_data['Rut_boleta'],
            Especialista_Boleta = Especialista.objects.get(ID_Especialista=Especialista_N),
            Especialidad_Boleta = Especialidad.objects.get(Codigo_especialidad=Especialidad_N),
            Monto_Boleta = self.cleaned_data['Monto_boleta_form'],
            Fecha_Emision = self.cleaned_data['Fecha_emision_form'],
            Metodo_Pago = self.cleaned_data['Metodo_pago_form'],
            Efectivo = self.cleaned_data['Monto_efectivo'],
            Vuelto = self.cleaned_data['Vuelto_bol'],
            Tipo_atencion = self.cleaned_data['Tipo_atencion_form'],
            Arancel = self.cleaned_data['Arancel_form'],
            Num_Documento = self.cleaned_data['Num_Doc']
        )
        return BoletaServicio