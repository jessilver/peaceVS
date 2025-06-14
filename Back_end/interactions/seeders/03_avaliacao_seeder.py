from jessilver_django_seed.seeders.BaseSeeder import BaseSeeder
from interactions.models import Avaliacao
from users.models import UserProfile
from conteudo.models import Filme

class AvaliacaoSeeder(BaseSeeder):
    @property
    def seeder_name(self):
        return 'AvaliacaoSeeder'

    def seed(self):
        profile = UserProfile.objects.first()
        filme = Filme.objects.first()
        if not profile or not filme:
            self.error('Perfil de usuário ou filme não encontrado.')
            return
        avaliacao, created = Avaliacao.objects.get_or_create(
            perfil_usuario=profile,
            filme=filme,
            nota=5,
            comentario_texto='Excelente filme!'
        )
        if created:
            self.succes('Avaliação criada')
        else:
            self.error('Avaliação já existe')
