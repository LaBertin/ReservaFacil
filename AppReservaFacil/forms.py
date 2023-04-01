from django import forms
from django.contrib.auth.forms import *
from django.contrib.auth.models import *
from django.contrib import messages
from .models import *

# Create your forms here.

class FormRegistrarUsuario(UserCreationForm):
    pass

class LoginUsuario(AuthenticationForm):
    pass

class DateForm(forms.Form):
    date = forms.DateTimeField(label="Fecha",
    widget=forms.SelectDateWidget
    )

        

