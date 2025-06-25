from rest_framework import serializers
from .models import FavoritoFilme, FavoritoSerie

class FavoritoFilmeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoritoFilme
        fields = ['id', 'user', 'filme', 'criado_em']

class FavoritoSerieSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoritoSerie
        fields = ['id', 'user', 'serie', 'criado_em']
