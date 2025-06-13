from django.db import models
from django.conf import settings

# Create your models here.

class PlanoAssinatura(models.Model):
    QUALIDADE_VIDEO_CHOICES = (
        ('SD', 'Definição Padrão (SD)'),
        ('HD', 'Alta Definição (HD - 720p/1080p)'),
        ('4K', 'Ultra Alta Definição (4K+HDR)'),
    )
    nome_plano = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, max_length=100)
    descricao = models.TextField(blank=True, null=True)
    preco_mensal = models.DecimalField(max_digits=6, decimal_places=2)
    preco_anual = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    qualidade_video_permitida = models.CharField(max_length=20, choices=QUALIDADE_VIDEO_CHOICES, default='HD')
    numero_telas_simultaneas = models.PositiveSmallIntegerField(default=1)
    ativo = models.BooleanField(default=True)
    stripe_price_id_mensal = models.CharField(max_length=100, blank=True, null=True)
    stripe_price_id_anual = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['preco_mensal']
        verbose_name = "Plano de Assinatura"
        verbose_name_plural = "Planos de Assinatura"

    def __str__(self):
        return self.nome_plano

class AssinaturaUsuario(models.Model):
    STATUS_ASSINATURA_CHOICES = (
        ('ATIVA', 'Ativa'),
        ('CANCELADA', 'Cancelada'),
        ('PENDENTE_PAGAMENTO', 'Pendente Pagamento'),
        ('EXPIRADA', 'Expirada'),
        ('AVALIACAO_GRATUITA', 'Avaliação Gratuita'),
        ('INADIMPLENTE', 'Inadimplente'),
    )
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assinatura')
    plano = models.ForeignKey('PlanoAssinatura', on_delete=models.SET_NULL, null=True, blank=True, related_name='assinaturas_de_usuarios')
    stripe_subscription_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    stripe_customer_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    data_inicio = models.DateTimeField()
    data_fim_periodo_corrente = models.DateTimeField()
    status_assinatura = models.CharField(max_length=25, choices=STATUS_ASSINATURA_CHOICES, default='PENDENTE_PAGAMENTO', db_index=True)
    data_cancelamento = models.DateTimeField(null=True, blank=True)
    cancelada_no_fim_periodo = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Assinatura de Usuário"
        verbose_name_plural = "Assinaturas de Usuários"

    def __str__(self):
        return f"Assinatura de {self.usuario.email} - Plano: {self.plano.nome_plano if self.plano else 'Nenhum'} ({self.get_status_assinatura_display()})"

    @property
    def is_ativa(self):
        import django.utils.timezone
        return self.status_assinatura == 'ATIVA' and self.data_fim_periodo_corrente >= django.utils.timezone.now()
