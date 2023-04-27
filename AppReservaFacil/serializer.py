from rest_framework import serializers
from .models import CitaSinUsuario

class CitaSinUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = CitaSinUsuario
        field = ('rut',)
