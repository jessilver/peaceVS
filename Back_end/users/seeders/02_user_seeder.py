from jessilver_django_seed.seeders.BaseSeeder import BaseSeeder
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.contrib.auth.models import Group

class SuperUserSeeder(BaseSeeder):
    @property
    def seeder_name(self):
        return 'SuperUserSeeder'

    def seed(self):
        User = get_user_model()
        # Superuser
        if not User.objects.filter(email='superuser@peacevs.com').exists():
            user = User.objects.create_superuser(
                email='superuser@peacevs.com',
                password='123456789',
                is_active=True,
                last_login=now(),
                date_joined=now(),
                first_name='Super',
                last_name='User'
            )
            self.succes('Superuser criado com sucesso')
        else:
            self.error('Superuser já existe')

class AdminGroupUserSeeder(BaseSeeder):
    @property
    def seeder_name(self):
        return 'AdminGroupUserSeeder'

    def seed(self):
        User = get_user_model()
        # Usuário admin (não superuser)
        if not User.objects.filter(email='admin-group@peacevs.com').exists():
            user = User.objects.create_user(
                email='admin-group@peacevs.com',
                password='123456789',
                is_active=True,
                last_login=now(),
                date_joined=now(),
                first_name='AdminGroup',
                last_name='PeaceVS'
            )
            group = Group.objects.get(name='Administrador')
            user.groups.add(group)
            self.succes('Usuário admin de grupo criado e adicionado ao grupo Administrador')
        else:
            self.error('Usuário admin de grupo já existe')

class ModeratorUserSeeder(BaseSeeder):
    @property
    def seeder_name(self):
        return 'ModeratorUserSeeder'

    def seed(self):
        User = get_user_model()
        # Usuário moderador
        if not User.objects.filter(email='moderator@peacevs.com').exists():
            user = User.objects.create_user(
                email='moderator@peacevs.com',
                password='123456789',
                is_active=True,
                last_login=now(),
                date_joined=now(),
                first_name='Moderator',
                last_name='PeaceVS'
            )
            group = Group.objects.get(name='Moderador')
            user.groups.add(group)
            self.succes('Usuário moderador criado e adicionado ao grupo Moderador')
        else:
            self.error('Usuário moderador já existe')

class SupportUserSeeder(BaseSeeder):
    @property
    def seeder_name(self):
        return 'SupportUserSeeder'

    def seed(self):
        User = get_user_model()
        # Usuário suporte
        if not User.objects.filter(email='support@peacevs.com').exists():
            user = User.objects.create_user(
                email='support@peacevs.com',
                password='123456789',
                is_active=True,
                last_login=now(),
                date_joined=now(),
                first_name='Support',
                last_name='PeaceVS'
            )
            group = Group.objects.get(name='Suporte')
            user.groups.add(group)
            self.succes('Usuário suporte criado e adicionado ao grupo Suporte')
        else:
            self.error('Usuário suporte já existe')

class NormalUserSeeder(BaseSeeder):
    @property
    def seeder_name(self):
        return 'NormalUserSeeder'

    def seed(self):
        User = get_user_model()
        # Usuário comum
        if not User.objects.filter(email='user@peacevs.com').exists():
            user = User.objects.create_user(
                email='user@peacevs.com',
                password='123456789',
                is_active=True,
                last_login=now(),
                date_joined=now(),
                first_name='User',
                last_name='PeaceVS'
            )
            group = Group.objects.get(name='Usuario')
            user.groups.add(group)
            self.succes('Usuário comum criado e adicionado ao grupo Usuario')
        else:
            self.error('Usuário comum já existe')