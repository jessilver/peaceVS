from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import PlanoAssinatura, AssinaturaUsuario
from .serializers import PlanoAssinaturaSerializer, AssinaturaUsuarioSerializer

# Create your views here.

class PlanoAssinaturaViewSet(viewsets.ModelViewSet):
    queryset = PlanoAssinatura.objects.all()
    serializer_class = PlanoAssinaturaSerializer
    permission_classes = [AllowAny]

class AssinaturaUsuarioViewSet(viewsets.ModelViewSet):
    queryset = AssinaturaUsuario.objects.all()
    serializer_class = AssinaturaUsuarioSerializer
