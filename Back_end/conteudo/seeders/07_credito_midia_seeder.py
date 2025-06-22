from jessilver_django_seed.seeders.BaseSeeder import BaseSeeder
from conteudo.models import CreditoMidia, Pessoa, Filme

class CreditoMidiaSeeder(BaseSeeder):
    @property
    def seeder_name(self):
        return 'CreditoMidiaSeeder'

    def seed(self):
        pessoa = Pessoa.objects.first()
        filme = Filme.objects.first()
        if not pessoa or not filme:
            self.error('Pessoa ou filme não encontrado. Rode os seeders de pessoa e filme antes.')
            return
        credito, created = CreditoMidia.objects.get_or_create(
            pessoa=pessoa,
            filme=filme,
            tipo_credito='ATOR',
            ordem=1
        )
        if created:
            self.success('Crédito de mídia criado')
        else:
            self.error('Crédito de mídia já existe')
