from rest_framework import serializers
from .models import Solicitud

class SolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitud
        fields = ['id', 'estado', 'fecha','emailUser']