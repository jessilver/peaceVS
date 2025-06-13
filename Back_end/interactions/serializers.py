from rest_framework import serializers
from .models import ItemListaInteresse, HistoricoVisualizacao, Avaliacao

class ItemListaInteresseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemListaInteresse
        fields = '__all__'

class HistoricoVisualizacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricoVisualizacao
        fields = '__all__'

class AvaliacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaliacao
        fields = '__all__'
