from django import forms
from django.contrib.auth.forms import *
from django.contrib.auth.models import *
from django.contrib import messages
from .models import *
from django.core.exceptions import ValidationError
from django.forms.widgets import *


# Create your forms here.

class FormEspecialista(forms.Form):
    nom_com_especialista = forms.CharField(max_length=256)
    rut = forms.CharField(max_length=9)
    sexo = forms.ChoiceField(choices = ([('Femenino','Femenino'), ('Masculino','Masculino')]), required=True,initial=0)
    fecha_nac_especialista = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    direccion_especialista = forms.CharField(max_length=256)
    contacto_especialista = forms.CharField(max_length=9 ,widget=NumberInput)
    especialidad_p = forms.ModelChoiceField(queryset=Especialidad.objects.all() ,initial=0)
    especialidad_s = forms.ModelChoiceField(queryset=Especialidad.objects.all() ,initial=0,required=False)
    especialidad_t = forms.ModelChoiceField(queryset=Especialidad.objects.all() ,initial=0,required=False)
    especialidad_c = forms.ModelChoiceField(queryset=Especialidad.objects.all() ,initial=0,required=False)

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

    

class LoginUsuario(AuthenticationForm):
    pass

class DateForm(forms.Form):
    date = forms.DateTimeField(label="Fecha",
    widget=forms.SelectDateWidget
    )

        

