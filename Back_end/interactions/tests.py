from django.test import TestCase
from users.models import CustomUser, UserProfile
from conteudo.models import Filme, Serie
from .models import ItemListaInteresse, HistoricoVisualizacao, Avaliacao

class ItemListaInteresseModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='user@ex.com', password='123', first_name='A', last_name='B')
        self.profile = UserProfile.objects.create(user=self.user, nome_perfil='Perfil')
        self.filme = Filme.objects.create(titulo='Filme', sinopse='...', ano_lancamento=2020, duracao_minutos=100, arquivo_video_url='http://f.mp4', slug='filme', ativo=True)

    def test_create_item_lista_interesse(self):
        # Testa apenas a criação sem usar ContentType
        item = ItemListaInteresse.objects.create(perfil_usuario=self.profile, content_type_id=1, object_id=self.filme.id)
        self.assertEqual(item.perfil_usuario, self.profile)
        self.assertEqual(item.object_id, self.filme.id)

class HistoricoVisualizacaoModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='user2@ex.com', password='123', first_name='A', last_name='B')
        self.profile = UserProfile.objects.create(user=self.user, nome_perfil='Perfil2')
        self.filme = Filme.objects.create(titulo='Filme2', sinopse='...', ano_lancamento=2021, duracao_minutos=90, arquivo_video_url='http://f2.mp4', slug='filme2', ativo=True)

    def test_create_historico_filme(self):
        hist = HistoricoVisualizacao.objects.create(perfil_usuario=self.profile, filme=self.filme, progresso_segundos=30, concluido=False)
        self.assertEqual(hist.perfil_usuario, self.profile)
        self.assertEqual(hist.filme, self.filme)
        self.assertFalse(hist.concluido)

class AvaliacaoModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='user3@ex.com', password='123', first_name='A', last_name='B')
        self.profile = UserProfile.objects.create(user=self.user, nome_perfil='Perfil3')
        self.filme = Filme.objects.create(titulo='Filme3', sinopse='...', ano_lancamento=2022, duracao_minutos=80, arquivo_video_url='http://f3.mp4', slug='filme3', ativo=True)
        self.serie = Serie.objects.create(titulo='Serie', sinopse='...', ano_lancamento=2022, slug='serie', ativo=True)

    def test_create_avaliacao_filme(self):
        avaliacao = Avaliacao.objects.create(perfil_usuario=self.profile, filme=self.filme, nota=4)
        self.assertEqual(avaliacao.perfil_usuario, self.profile)
        self.assertEqual(avaliacao.filme, self.filme)
        self.assertEqual(avaliacao.nota, 4)

    def test_create_avaliacao_serie(self):
        avaliacao = Avaliacao.objects.create(perfil_usuario=self.profile, serie=self.serie, nota=5)
        self.assertEqual(avaliacao.serie, self.serie)
        self.assertEqual(avaliacao.nota, 5)
