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
