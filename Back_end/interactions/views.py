from django.shortcuts import render
from rest_framework import viewsets
from .models import ItemListaInteresse, HistoricoVisualizacao, Avaliacao
from .serializers import ItemListaInteresseSerializer, HistoricoVisualizacaoSerializer, AvaliacaoSerializer

# Create your views here.

class ItemListaInteresseViewSet(viewsets.ModelViewSet):
    queryset = ItemListaInteresse.objects.all()
    serializer_class = ItemListaInteresseSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()
        user = self.request.user
        return ItemListaInteresse.objects.filter(perfil_usuario__user=user)

class HistoricoVisualizacaoViewSet(viewsets.ModelViewSet):
    queryset = HistoricoVisualizacao.objects.all()
    serializer_class = HistoricoVisualizacaoSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()
        user = self.request.user
        return HistoricoVisualizacao.objects.filter(perfil_usuario__user=user)

class AvaliacaoViewSet(viewsets.ModelViewSet):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()
        user = self.request.user
        return Avaliacao.objects.filter(perfil_usuario__user=user)
