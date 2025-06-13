from rest_framework import serializers
from .models import PlanoAssinatura, AssinaturaUsuario

class PlanoAssinaturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanoAssinatura
        fields = '__all__'

class AssinaturaUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssinaturaUsuario
        fields = '__all__'
