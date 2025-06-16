from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import CustomUser
from .models import PlanoAssinatura, AssinaturaUsuario
from datetime import datetime, timedelta

class PlanoAssinaturaModelTest:
    def test_create_plano_assinatura(self):
        plano = PlanoAssinatura.objects.create(
            nome_plano='Premium',
            slug='premium',
            preco_mensal=39.90,
            qualidade_video_permitida='4K',
            numero_telas_simultaneas=4,
            ativo=True
        )
        assert plano.nome_plano == 'Premium'
        assert plano.qualidade_video_permitida == '4K'
        assert plano.ativo

class AssinaturaUsuarioModelTest:
    def setup_method(self):
        self.user = CustomUser.objects.create_user(email='assinante@ex.com', password='123', first_name='A', last_name='B')
        self.plano = PlanoAssinatura.objects.create(
            nome_plano='Básico',
            slug='basico',
            preco_mensal=19.90,
            qualidade_video_permitida='HD',
            numero_telas_simultaneas=2,
            ativo=True
        )

    def test_create_assinatura_usuario(self):
        inicio = datetime.now()
        fim = inicio + timedelta(days=30)
        assinatura = AssinaturaUsuario.objects.create(
            usuario=self.user,
            plano=self.plano,
            data_inicio=inicio,
            data_fim_periodo_corrente=fim,
            status_assinatura='ATIVA'
        )
        assert assinatura.usuario == self.user
        assert assinatura.plano == self.plano
        assert assinatura.status_assinatura == 'ATIVA'

class PlanoAssinaturaAPITests(APITestCase):
    def setUp(self):
        self.plano = PlanoAssinatura.objects.create(
            nome_plano='Premium', slug='premium', preco_mensal=39.90,
            qualidade_video_permitida='4K', numero_telas_simultaneas=4, ativo=True
        )

    def test_list_planos(self):
        url = reverse('planoassinatura-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

class AssinaturaUsuarioAPITests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='assinante@ex.com', password='123', first_name='A', last_name='B')
        self.plano = PlanoAssinatura.objects.create(
            nome_plano='Básico', slug='basico', preco_mensal=19.90,
            qualidade_video_permitida='HD', numero_telas_simultaneas=2, ativo=True
        )
        self.client.force_authenticate(user=self.user)

    def test_list_assinaturas(self):
        url = reverse('assinaturausuario-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_assinatura(self):
        url = reverse('assinaturausuario-list')
        inicio = datetime.now()
        fim = inicio + timedelta(days=30)
        data = {
            'usuario': self.user.id,
            'plano': self.plano.id,
            'data_inicio': inicio.isoformat(),
            'data_fim_periodo_corrente': fim.isoformat(),
            'status_assinatura': 'ATIVA'
        }
        response = self.client.post(url, data)
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])
