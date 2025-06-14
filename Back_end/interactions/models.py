from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class ItemListaInteresse(models.Model):
    perfil_usuario = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, related_name='itens_lista_interesse')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    conteudo_objeto = GenericForeignKey('content_type', 'object_id')
    data_adicao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('perfil_usuario', 'content_type', 'object_id')
        ordering = ['-data_adicao']

    def __str__(self):
        return f"{self.conteudo_objeto} na lista de {self.perfil_usuario.nome_perfil}"

class HistoricoVisualizacao(models.Model):
    perfil_usuario = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, related_name='historico_visualizacao')
    filme = models.ForeignKey('conteudo.Filme', on_delete=models.CASCADE, null=True, blank=True, related_name='visualizacoes_historico')
    episodio = models.ForeignKey('conteudo.Episodio', on_delete=models.CASCADE, null=True, blank=True, related_name='visualizacoes_historico')
    progresso_segundos = models.PositiveIntegerField(default=0)
    ultima_visualizacao_em = models.DateTimeField(auto_now=True)
    concluido = models.BooleanField(default=False)
    data_inicio_visualizacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-ultima_visualizacao_em']
        verbose_name = "Histórico de Visualização"
        verbose_name_plural = "Históricos de Visualização"

    def __str__(self):
        content_watched = self.filme if self.filme else self.episodio
        status = "Concluído" if self.concluido else f"Progresso: {self.progresso_segundos}s"
        return f"{self.perfil_usuario.nome_perfil} - {content_watched} ({status})"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.filme and self.episodio:
            raise ValidationError("Um histórico de visualização não pode ser para um filme E um episódio simultaneamente.")
        if not self.filme and not self.episodio:
            raise ValidationError("Um histórico de visualização deve ser associado a um filme OU a um episódio.")

    @property
    def conteudo_visualizado(self):
        return self.filme if self.filme else self.episodio

class Avaliacao(models.Model):
    NOTA_CHOICES = [(i, str(i)) for i in range(1, 6)]
    perfil_usuario = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, related_name='avaliacoes_feitas')
    filme = models.ForeignKey('conteudo.Filme', on_delete=models.CASCADE, null=True, blank=True, related_name='avaliacoes_recebidas')
    serie = models.ForeignKey('conteudo.Serie', on_delete=models.CASCADE, null=True, blank=True, related_name='avaliacoes_recebidas')
    nota = models.PositiveSmallIntegerField(choices=NOTA_CHOICES)
    comentario_texto = models.TextField(blank=True, null=True)
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_avaliacao']
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"

    def __str__(self):
        content_rated = self.filme if self.filme else self.serie
        return f"Avaliação de {self.perfil_usuario.nome_perfil} para {content_rated}: {self.nota} estrelas"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.filme and self.serie:
            raise ValidationError("Uma avaliação não pode ser para um filme E uma série simultaneamente.")
        if not self.filme and not self.serie:
            raise ValidationError("Uma avaliação deve ser associada a um filme OU a uma série.")

    @property
    def conteudo_avaliado(self):
        return self.filme if self.filme else self.serie
