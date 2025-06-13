from django.shortcuts import render
from rest_framework import viewsets
from .models import Filme, Serie, Temporada, Episodio, Genero, Pessoa, CreditoMidia
from .serializers import FilmeSerializer, SerieSerializer, TemporadaSerializer, EpisodioSerializer, GeneroSerializer, PessoaSerializer, CreditoMidiaSerializer

# Create your views here.

class FilmeViewSet(viewsets.ModelViewSet):
    queryset = Filme.objects.all()
    serializer_class = FilmeSerializer

class SerieViewSet(viewsets.ModelViewSet):
    queryset = Serie.objects.all()
    serializer_class = SerieSerializer

class TemporadaViewSet(viewsets.ModelViewSet):
    queryset = Temporada.objects.all()
    serializer_class = TemporadaSerializer

class EpisodioViewSet(viewsets.ModelViewSet):
    queryset = Episodio.objects.all()
    serializer_class = EpisodioSerializer

class GeneroViewSet(viewsets.ModelViewSet):
    queryset = Genero.objects.all()
    serializer_class = GeneroSerializer

class PessoaViewSet(viewsets.ModelViewSet):
    queryset = Pessoa.objects.all()
    serializer_class = PessoaSerializer

class CreditoMidiaViewSet(viewsets.ModelViewSet):
    queryset = CreditoMidia.objects.all()
    serializer_class = CreditoMidiaSerializer
