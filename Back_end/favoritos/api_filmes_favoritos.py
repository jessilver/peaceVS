from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import FavoritoFilme
from .serializers import FavoritoFilmeComFilmeSerializer

class FilmesFavoritosUsuarioList(generics.ListAPIView):
    serializer_class = FavoritoFilmeComFilmeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['filme__titulo', 'filme__sinopse']
    ordering_fields = ['filme__titulo', 'filme__ano_lancamento']

    def get_queryset(self):
        return FavoritoFilme.objects.filter(user=self.request.user)
