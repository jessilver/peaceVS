from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import FavoritoFilme, FavoritoSerie
from .serializers import FavoritoFilmeSerializer, FavoritoSerieSerializer

# Create your views here.

class FavoritoFilmeViewSet(viewsets.ModelViewSet):
    serializer_class = FavoritoFilmeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FavoritoFilme.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FavoritoSerieViewSet(viewsets.ModelViewSet):
    serializer_class = FavoritoSerieSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FavoritoSerie.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
