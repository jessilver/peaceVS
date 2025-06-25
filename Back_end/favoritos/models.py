from django.db import models
from django.conf import settings
from conteudo.models import Filme, Serie

class FavoritoFilme(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favoritos_filmes')
    filme = models.ForeignKey(Filme, on_delete=models.CASCADE, related_name='favoritado_por')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'filme')
        verbose_name = 'Favorito Filme'
        verbose_name_plural = 'Favoritos Filmes'

class FavoritoSerie(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favoritos_series')
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, related_name='favoritado_por')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'serie')
        verbose_name = 'Favorito Série'
        verbose_name_plural = 'Favoritos Séries'
