from jessilver_django_seed.seeders.BaseSeeder import BaseSeeder
from conteudo.models import Temporada, Episodio

class EpisodioSeeder(BaseSeeder):
    @property
    def seeder_name(self):
        return 'EpisodioSeeder'

    def seed(self):
        return
        # temporada = Temporada.objects.first()
        # if not temporada:
        #     self.error('Nenhuma temporada encontrada. Rode o seeder de temporada antes.')
        #     return
        # episodio, created = Episodio.objects.get_or_create(
        #     temporada=temporada,
        #     numero_episodio=1,
        #     titulo='Episódio 1',
        #     duracao_minutos=45,
        #     arquivo_video_url='http://video.com/serie1t1e1.mp4'
        # )
        # if created:
        #     self.success('Episódio 1 criado')
        # else:
        #     self.error('Episódio 1 já existe')
