from django.core.management.base import BaseCommand
from users.models import CustomUser
from subscriptions.models import PlanoAssinatura, AssinaturaUsuario
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Popula o banco com assinaturas de exemplo.'

    def handle(self, *args, **options):
        user = CustomUser.objects.filter(is_superuser=False).first()
        plano = PlanoAssinatura.objects.first()
        if not user or not plano:
            self.stdout.write(self.style.WARNING('Usuário ou plano não encontrado.'))
            return
        inicio = timezone.now()
        fim = inicio + timedelta(days=30)
        AssinaturaUsuario.objects.get_or_create(
            usuario=user,
            plano=plano,
            data_inicio=inicio,
            data_fim_periodo_corrente=fim,
            status_assinatura='ATIVA'
        )
        self.stdout.write(self.style.SUCCESS('Assinatura de exemplo criada com sucesso!'))
