from jessilver_django_seed.seeders.BaseSeeder import BaseSeeder
from users.models import CustomUser, UserProfile
from django.contrib.auth.models import Group
from django.utils.timezone import now

class UserProfileUsuarioSeeder(BaseSeeder):
    @property
    def seeder_name(self):
        return 'UserProfileUsuarioSeeder'

    def seed(self):
        # Busca um usuário do grupo Usuário
        user = CustomUser.objects.filter(groups__name='Usuario').first()

        if not user:
            self.error('Nenhum usuário no grupo Usuario encontrado.')
            return
        
        if not UserProfile.objects.filter(user=user).exists():
            UserProfile.objects.create(
                user=user,
                nome_perfil='Perfil Usuário',
                avatar_url='',
                data_nascimento='2000-01-01',
                preferencias_linguagem='pt-BR',
                eh_perfil_infantil=False
            )
            self.succes('UserProfile criado para usuário do grupo Usuário')
        else:
            self.error('UserProfile já existe para este usuário')
