from jessilver_django_seed.seeders.BaseSeeder import BaseSeeder
from subscriptions.models import AssinaturaUsuario, PlanoAssinatura
from users.models import CustomUser
from django.utils.timezone import now, timedelta
from django.contrib.auth.models import Group

class AssinaturaUsuarioSeeder(BaseSeeder):
    @property
    def seeder_name(self):
        return 'AssinaturaUsuarioSeeder'

    def seed(self):
        try:
            grupo_usuario = Group.objects.get(name='Usuario')
        except Group.DoesNotExist:
            self.error('Grupo "Usuario" não encontrado.')
            return
        
        user = CustomUser.objects.filter(groups=grupo_usuario).first()
        plano = PlanoAssinatura.objects.first()

        if not user or not plano:
            self.error('Usuário comum ou plano não encontrado.')
            return
        
        inicio = now()
        fim = inicio + timedelta(days=30)

        assinatura, created = AssinaturaUsuario.objects.get_or_create(
            usuario=user,
            plano=plano,
            data_inicio=inicio,
            data_fim_periodo_corrente=fim,
            status_assinatura='ATIVA'
        )
        if created:
            self.success('Assinatura criada')
        else:
            self.error('Assinatura já existe para este usuário')
