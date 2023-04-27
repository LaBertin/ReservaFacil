from django import forms
from django.contrib.auth.forms import *
from django.contrib.auth.models import *
from django.contrib import messages
from .models import *
from django.core.exceptions import ValidationError
from django.forms.widgets import *
from datetime import date


today = date.today()
max = today.replace(today.year+ 1)
# Create your forms here.

DIAS_CHOICES=[('lun','Lunes'),('mar','Martes'),('mie','Miercoles'),('jue','Jueves'),('vie','Viernes'),('sab','Sabado'),('dom','Domingo')]
MINUTOS_CHOICES=[(None,'--------'),(15,'15 Minutos'),(30,'30 Minutos'),(45,'45 Minutos'),(60,'60 Minutos')]
SEXO_CHOICES=[('Femenino','Femenino'), ('Masculino','Masculino')]


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

class FormPacienteSinUser(forms.Form):
    rut_pac = forms.CharField(max_length=9)
    email_pac = forms.EmailField(label='email')
    telefono_pac = forms.IntegerField()

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

class FormMensaje(forms.Form):
    texto = forms.CharField(max_length=256)

class FormFichaMedica(forms.Form):
    RUT_Pac = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),max_length=9, required=True)
    Nombre_Com_Pac = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),max_length = 256, required=True)
    Direccion_Pac = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),max_length=256, required=False)
    Telefono_Pac = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),max_length=9, required=False)
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

class FormCitaMedica(forms.Form):
    Ficha_Medica_Pac = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'form-control'}),max_length=9, required=True)
    Fecha_Cita = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'form-control'}), required=True)
    RUT_Pac = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'form-control'}),max_length=9, required=True)
    Nombre_Com_Pac = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'form-control'}),max_length = 256, required=True)
    Nombre_Com_Esp = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'form-control'}),max_length = 256, required=True)
    Diagnostico_Cita = forms.CharField(widget=forms.Textarea(attrs={'rows': 10  , 'cols': 120}), required=False)
