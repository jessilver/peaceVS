from jessilver_django_seed.seeders.BaseSeeder import BaseSeeder
from conteudo.models import Serie, Temporada

class TemporadaSeeder(BaseSeeder):
    @property
    def seeder_name(self):
        return 'TemporadaSeeder'

    def seed(self):
        return
        # serie = Serie.objects.first()
        # if not serie:
        #     self.error('Nenhuma série encontrada. Rode o seeder de série antes.')
        #     return
        # temporada, created = Temporada.objects.get_or_create(
        #     serie=serie,
        #     numero_temporada=1,
        #     titulo='Temporada 1',
        #     ano_lancamento=2024
        # )
        # if created:
        #     self.success('Temporada 1 criada')
        # else:
        #     self.error('Temporada 1 já existe')
