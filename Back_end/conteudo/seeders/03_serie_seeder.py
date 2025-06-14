from jessilver_django_seed.seeders.BaseSeeder import BaseSeeder
from conteudo.models import Serie, Genero

class SerieSeeder(BaseSeeder):
    @property
    def seeder_name(self):
        return 'SerieSeeder'

    def seed(self):
        genero = Genero.objects.first()
        if not genero:
            self.error('Nenhum gênero encontrado. Rode o seeder de gênero antes.')
            return
        serie, created = Serie.objects.get_or_create(
            titulo='Série Exemplo',
            sinopse='Uma série de exemplo.',
            ano_lancamento=2024,
            status='EM_ANDAMENTO',
            slug='serie-exemplo',
            ativo=True
        )
        if created:
            serie.generos.add(genero)
            self.succes('Série Exemplo criada')
        else:
            self.error('Série Exemplo já existe')
