from jessilver_django_seed.seeders.BaseSeeder import BaseSeeder
from media.models import Pessoa

class PessoaSeeder(BaseSeeder):
    @property
    def seeder_name(self):
        return 'PessoaSeeder'

    def seed(self):
        pessoa, created = Pessoa.objects.get_or_create(
            nome_completo='Ator Exemplo',
            slug='ator-exemplo'
        )
        if created:
            self.succes('Pessoa Ator Exemplo criada')
        else:
            self.error('Pessoa Ator Exemplo já existe')
