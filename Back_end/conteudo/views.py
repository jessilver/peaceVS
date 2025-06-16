from django.shortcuts import render
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Filme, Serie, Temporada, Episodio, Genero, Pessoa, CreditoMidia
from .serializers import FilmeSerializer, SerieSerializer, TemporadaSerializer, EpisodioSerializer, GeneroSerializer, PessoaSerializer, CreditoMidiaSerializer
from .permissions import ReadOnlyOrAuthenticated

# Create your views here.

class FilmeViewSet(viewsets.ModelViewSet):
    queryset = Filme.objects.all()
    serializer_class = FilmeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['generos']  # permite filtrar por ?generos=ID
    permission_classes = [ReadOnlyOrAuthenticated]

class SerieViewSet(viewsets.ModelViewSet):
    queryset = Serie.objects.all()
    serializer_class = SerieSerializer
    permission_classes = [ReadOnlyOrAuthenticated]

class TemporadaViewSet(viewsets.ModelViewSet):
    queryset = Temporada.objects.all()
    serializer_class = TemporadaSerializer
    permission_classes = [ReadOnlyOrAuthenticated]

class EpisodioViewSet(viewsets.ModelViewSet):
    queryset = Episodio.objects.all()
    serializer_class = EpisodioSerializer
    permission_classes = [ReadOnlyOrAuthenticated]

class GeneroViewSet(viewsets.ModelViewSet):
    queryset = Genero.objects.all()
    serializer_class = GeneroSerializer
    permission_classes = [ReadOnlyOrAuthenticated]

class PessoaViewSet(viewsets.ModelViewSet):
    queryset = Pessoa.objects.all()
    serializer_class = PessoaSerializer
    permission_classes = [ReadOnlyOrAuthenticated]

class CreditoMidiaViewSet(viewsets.ModelViewSet):
    queryset = CreditoMidia.objects.all()
    serializer_class = CreditoMidiaSerializer
    permission_classes = [ReadOnlyOrAuthenticated]
