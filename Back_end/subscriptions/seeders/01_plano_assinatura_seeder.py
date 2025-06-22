from jessilver_django_seed.seeders.BaseSeeder import BaseSeeder
from subscriptions.models import PlanoAssinatura

class PlanoAssinaturaSeeder(BaseSeeder):
    @property
    def seeder_name(self):
        return 'PlanoAssinaturaSeeder'

    def seed(self):
        plano, created = PlanoAssinatura.objects.get_or_create(
            nome_plano='Básico',
            slug='basico',
            preco_mensal=19.90,
            qualidade_video_permitida='HD',
            numero_telas_simultaneas=2,
            ativo=True
        )
        if created:
            self.success('Plano Básico criado')
        else:
            self.error('Plano Básico já existe')

        # Plano Padrão
        plano, created = PlanoAssinatura.objects.get_or_create(
            nome_plano='Padrão',
            slug='padrao',
            preco_mensal=29.90,
            qualidade_video_permitida='Full HD',
            numero_telas_simultaneas=4,
            ativo=True
        )
        if created:
            self.success('Plano Padrão criado')
        else:
            self.error('Plano Padrão já existe')

        # Plano Premium
        plano, created = PlanoAssinatura.objects.get_or_create(
            nome_plano='Premium',
            slug='premium',
            preco_mensal=49.90,
            qualidade_video_permitida='Ultra HD',
            numero_telas_simultaneas=6,
            ativo=True
        )
        if created:
            self.success('Plano Premium criado')
        else:
            self.error('Plano Premium já existe')
