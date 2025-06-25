from rest_framework import serializers
from .models import FavoritoFilme, FavoritoSerie
from conteudo.serializers import FilmeSerializer

class FavoritoFilmeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoritoFilme
        fields = ['id', 'user', 'filme', 'criado_em']
        read_only_fields = ['user']

class FavoritoFilmeComFilmeSerializer(serializers.ModelSerializer):
    filme = FilmeSerializer()
    class Meta:
        model = FavoritoFilme
        fields = ['id', 'filme']

class FavoritoSerieSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoritoSerie
        fields = ['id', 'user', 'serie', 'criado_em']
        read_only_fields = ['user']
