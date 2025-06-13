from jessilver_django_seed.seeders.BaseSeeder import BaseSeeder
from media.models import Filme, Serie, Temporada, Episodio, Genero, Pessoa
from subscriptions.models import PlanoAssinatura
import random

class SampleDataSeeder(BaseSeeder):
    @property
    def seeder_name(self):
        return 'SampleDataSeeder'

    def seed(self):
        # Gêneros
        generos = ['Ação', 'Comédia', 'Drama', 'Ficção', 'Terror', 'Documentário']
        genero_objs = []
        for nome in generos:
            obj, _ = Genero.objects.get_or_create(nome=nome, slug=nome.lower())
            genero_objs.append(obj)

        # Pessoas
        atores = ['João Silva', 'Maria Souza', 'Carlos Lima', 'Ana Paula']
        pessoas = [Pessoa.objects.get_or_create(nome_completo=nome, slug=nome.lower().replace(' ', '-'))[0] for nome in atores]

        # Filmes
        for i in range(3):
            filme = Filme.objects.create(
                titulo=f'Filme Exemplo {i+1}',
                sinopse='Um filme de exemplo.',
                ano_lancamento=2020+i,
                duracao_minutos=100+i*10,
                arquivo_video_url=f'http://video.com/filme{i+1}.mp4',
                slug=f'filme-exemplo-{i+1}',
                ativo=True
            )
            filme.generos.set(random.sample(genero_objs, 2))

        # Séries, temporadas e episódios
        for i in range(2):
            serie = Serie.objects.create(
                titulo=f'Série Exemplo {i+1}',
                sinopse='Uma série de exemplo.',
                ano_lancamento=2021+i,
                status='EM_ANDAMENTO',
                slug=f'serie-exemplo-{i+1}',
                ativo=True
            )
            serie.generos.set(random.sample(genero_objs, 2))
            for t in range(1, 3):
                temporada = Temporada.objects.create(
                    serie=serie,
                    numero_temporada=t,
                    titulo=f'Temporada {t}',
                    ano_lancamento=2021+i
                )
                for e in range(1, 4):
                    Episodio.objects.create(
                        temporada=temporada,
                        numero_episodio=e,
                        titulo=f'Episódio {e}',
                        duracao_minutos=45,
                        arquivo_video_url=f'http://video.com/serie{i+1}t{t}e{e}.mp4'
                    )

        # Planos de assinatura
        planos = [
            {'nome_plano': 'Básico', 'slug': 'basico', 'preco_mensal': 19.90, 'qualidade_video_permitida': 'HD', 'numero_telas_simultaneas': 2},
            {'nome_plano': 'Premium', 'slug': 'premium', 'preco_mensal': 39.90, 'qualidade_video_permitida': '4K', 'numero_telas_simultaneas': 4},
        ]
        for plano in planos:
            PlanoAssinatura.objects.get_or_create(**plano)

        self.succes('Dados de exemplo criados com sucesso!')
