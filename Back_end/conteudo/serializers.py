from rest_framework import serializers
from .models import Filme, Serie, Temporada, Episodio, Genero, Pessoa, CreditoMidia

class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genero
        fields = ['id', 'nome', 'slug']

class FilmeSerializer(serializers.ModelSerializer):
    generos = GeneroSerializer(many=True, read_only=True)
    class Meta:
        model = Filme
        fields = '__all__'

class SerieSerializer(serializers.ModelSerializer):
    generos = GeneroSerializer(many=True, read_only=True)
    class Meta:
        model = Serie
        fields = '__all__'

class TemporadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temporada
        fields = '__all__'

class EpisodioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episodio
        fields = '__all__'

class PessoaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pessoa
        fields = '__all__'

class CreditoMidiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditoMidia
        fields = '__all__'
