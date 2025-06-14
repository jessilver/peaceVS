from jessilver_django_seed.seeders.BaseSeeder import BaseSeeder
from conteudo.models import Filme, Genero
from django.utils.timezone import now

class FilmeSeeder(BaseSeeder):
    @property
    def seeder_name(self):
        return 'FilmeSeeder'

    def seed(self):
        genero = Genero.objects.first()
        if not genero:
            self.error('Nenhum gênero encontrado. Rode o seeder de gênero antes.')
            return
        filme, created = Filme.objects.get_or_create(
            titulo='Filme Exemplo',
            sinopse='Um filme de exemplo.',
            ano_lancamento=2024,
            duracao_minutos=120,
            arquivo_video_url='http://video.com/filme.mp4',
            slug='filme-exemplo',
            ativo=True
        )
        if created:
            filme.generos.add(genero)
            self.succes('Filme Exemplo criado')
        else:
            self.error('Filme Exemplo já existe')
