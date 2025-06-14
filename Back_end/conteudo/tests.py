from django.test import TestCase
from .models import Filme, Serie, Temporada, Episodio, Genero, Pessoa, CreditoMidia

class GeneroModelTest(TestCase):
    def test_create_genero(self):
        genero = Genero.objects.create(nome='Ação', slug='acao')
        self.assertEqual(genero.nome, 'Ação')
        self.assertEqual(genero.slug, 'acao')

class FilmeModelTest(TestCase):
    def test_create_filme(self):
        filme = Filme.objects.create(
            titulo='Filme Teste',
            sinopse='Sinopse',
            ano_lancamento=2020,
            duracao_minutos=120,
            arquivo_video_url='http://video.com/filme.mp4',
            slug='filme-teste',
            ativo=True
        )
        self.assertEqual(filme.titulo, 'Filme Teste')
        self.assertEqual(filme.ano_lancamento, 2020)
        self.assertTrue(filme.ativo)

class SerieModelTest(TestCase):
    def test_create_serie(self):
        serie = Serie.objects.create(
            titulo='Série Teste',
            sinopse='Sinopse',
            ano_lancamento=2021,
            status='EM_ANDAMENTO',
            slug='serie-teste',
            ativo=True
        )
        self.assertEqual(serie.titulo, 'Série Teste')
        self.assertEqual(serie.status, 'EM_ANDAMENTO')

class TemporadaModelTest(TestCase):
    def setUp(self):
        self.serie = Serie.objects.create(
            titulo='Série', sinopse='...', ano_lancamento=2021, slug='serie', ativo=True
        )
    def test_create_temporada(self):
        temporada = Temporada.objects.create(
            serie=self.serie, numero_temporada=1, titulo='T1', ano_lancamento=2021
        )
        self.assertEqual(temporada.serie, self.serie)
        self.assertEqual(temporada.numero_temporada, 1)

class EpisodioModelTest(TestCase):
    def setUp(self):
        self.serie = Serie.objects.create(
            titulo='Série', sinopse='...', ano_lancamento=2021, slug='serie', ativo=True
        )
        self.temporada = Temporada.objects.create(
            serie=self.serie, numero_temporada=1, titulo='T1', ano_lancamento=2021
        )
    def test_create_episodio(self):
        episodio = Episodio.objects.create(
            temporada=self.temporada, numero_episodio=1, titulo='Ep1', duracao_minutos=45, arquivo_video_url='http://video.com/ep1.mp4'
        )
        self.assertEqual(episodio.temporada, self.temporada)
        self.assertEqual(episodio.numero_episodio, 1)

class PessoaModelTest(TestCase):
    def test_create_pessoa(self):
        pessoa = Pessoa.objects.create(nome_completo='Ator Teste')
        self.assertEqual(pessoa.nome_completo, 'Ator Teste')

class CreditoMidiaModelTest(TestCase):
    def setUp(self):
        self.filme = Filme.objects.create(
            titulo='Filme', sinopse='...', ano_lancamento=2020, duracao_minutos=100, arquivo_video_url='http://video.com/f.mp4', slug='filme', ativo=True
        )
        self.pessoa = Pessoa.objects.create(nome_completo='Ator')
    def test_create_credito(self):
        credito = CreditoMidia.objects.create(
            pessoa=self.pessoa, filme=self.filme, tipo_credito='ATOR', ordem=1
        )
        self.assertEqual(credito.pessoa, self.pessoa)
        self.assertEqual(credito.filme, self.filme)
        self.assertEqual(credito.tipo_credito, 'ATOR')
