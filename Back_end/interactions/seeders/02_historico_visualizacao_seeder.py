from jessilver_django_seed.seeders.BaseSeeder import BaseSeeder
from interactions.models import HistoricoVisualizacao
from users.models import UserProfile
from conteudo.models import Filme

class HistoricoVisualizacaoSeeder(BaseSeeder):
    @property
    def seeder_name(self):
        return 'HistoricoVisualizacaoSeeder'

    def seed(self):
        profile = UserProfile.objects.first()
        filme = Filme.objects.first()
        if not profile or not filme:
            self.error('Perfil de usuário ou filme não encontrado.')
            return
        historico, created = HistoricoVisualizacao.objects.get_or_create(
            perfil_usuario=profile,
            filme=filme,
            progresso_segundos=120,
            concluido=False
        )
        if created:
            self.succes('Histórico de visualização criado')
        else:
            self.error('Histórico de visualização já existe')
