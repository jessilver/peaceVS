from django.db import models
from django.utils.translation import gettext_lazy as _

# Modelo base abstrato para conteúdo de mídia
class ConteudoMidia(models.Model):
    titulo = models.CharField(max_length=255)
    sinopse = models.TextField()
    ano_lancamento = models.PositiveIntegerField()
    imagem_poster_url = models.URLField(max_length=500, blank=True, null=True)
    classificacao_indicativa = models.CharField(max_length=10, blank=True, null=True)
    data_adicao = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, max_length=255, help_text="Identificador único para URLs amigáveis", db_index=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['-data_adicao']

# Modelo Filme
class Filme(ConteudoMidia):
    duracao_minutos = models.PositiveIntegerField(help_text="Duração do filme em minutos")
    arquivo_video_url = models.URLField(max_length=1000, help_text="URL do arquivo de vídeo do filme")
    generos = models.ManyToManyField('Genero', related_name='filmes', blank=True)

    def __str__(self):
        return f"{self.titulo} ({self.ano_lancamento}) - Filme"

# Modelo Serie
class Serie(ConteudoMidia):
    STATUS_CHOICES = (
        ('EM_ANDAMENTO', 'Em Andamento'),
        ('FINALIZADA', 'Finalizada'),
        ('CANCELADA', 'Cancelada'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='EM_ANDAMENTO', blank=True, null=True)
    generos = models.ManyToManyField('Genero', related_name='series', blank=True)

    def __str__(self):
        return f"{self.titulo} ({self.ano_lancamento}) - Série"

# Modelo Temporada
class Temporada(models.Model):
    serie = models.ForeignKey('Serie', on_delete=models.CASCADE, related_name='temporadas')
    numero_temporada = models.PositiveIntegerField()
    titulo = models.CharField(max_length=255, blank=True, null=True)
    ano_lancamento = models.PositiveIntegerField(null=True, blank=True)
    imagem_poster_url = models.URLField(max_length=500, blank=True, null=True)

    class Meta:
        unique_together = ('serie', 'numero_temporada')
        ordering = ['serie', 'numero_temporada']

    def __str__(self):
        return f"{self.serie.titulo} - Temporada {self.numero_temporada}"

# Modelo Episodio
class Episodio(models.Model):
    temporada = models.ForeignKey('Temporada', on_delete=models.CASCADE, related_name='episodios')
    numero_episodio = models.PositiveIntegerField()
    titulo = models.CharField(max_length=255)
    sinopse = models.TextField(blank=True, null=True)
    duracao_minutos = models.PositiveIntegerField()
    arquivo_video_url = models.URLField(max_length=1000)
    data_lancamento_original = models.DateField(null=True, blank=True)
    imagem_thumbnail_url = models.URLField(max_length=500, blank=True, null=True)

    class Meta:
        unique_together = ('temporada', 'numero_episodio')
        ordering = ['temporada', 'numero_episodio']

    def __str__(self):
        return f"{self.temporada} - Ep. {self.numero_episodio}: {self.titulo}"

# Modelo Genero
class Genero(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, max_length=100, db_index=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome

# Modelo Pessoa
class Pessoa(models.Model):
    nome_completo = models.CharField(max_length=255)
    data_nascimento = models.DateField(null=True, blank=True)
    biografia = models.TextField(blank=True, null=True)
    foto_url = models.URLField(max_length=500, blank=True, null=True)
    slug = models.SlugField(unique=True, max_length=255, db_index=True)

    class Meta:
        verbose_name_plural = "Pessoas"
        ordering = ['nome_completo']

    def __str__(self):
        return self.nome_completo

# Modelo CreditoMidia
class CreditoMidia(models.Model):
    TIPO_CREDITO_CHOICES = (
        ('ATOR', 'Ator/Atriz'),
        ('DIRETOR', 'Diretor(a)'),
        ('ROTEIRISTA', 'Roteirista'),
        ('PRODUTOR', 'Produtor(a)'),
    )
    pessoa = models.ForeignKey('Pessoa', on_delete=models.CASCADE, related_name='creditos')
    filme = models.ForeignKey('Filme', on_delete=models.CASCADE, related_name='creditos_filme', null=True, blank=True)
    serie = models.ForeignKey('Serie', on_delete=models.CASCADE, related_name='creditos_serie', null=True, blank=True)
    tipo_credito = models.CharField(max_length=50, choices=TIPO_CREDITO_CHOICES)
    personagem_nome = models.CharField(max_length=150, blank=True, null=True)
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordem', 'pessoa__nome_completo']

    def __str__(self):
        content_object = self.filme if self.filme else self.serie
        return f"{self.pessoa} como {self.get_tipo_credito_display()} em {content_object}"

    @property
    def conteudo_objeto(self):
        return self.filme if self.filme else self.serie
