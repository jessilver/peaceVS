from jessilver_django_seed.seeders.BaseSeeder import BaseSeeder
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

class UserPermissionsSeeder(BaseSeeder):
    @property
    def seeder_name(self):
        return 'UserPermissionsSeeder'

    def seed(self):
        User = get_user_model()
        admin_group = Group.objects.get(name='Administrador')
        moderador_group = Group.objects.get(name='Moderador')
        suporte_group = Group.objects.get(name='Suporte')
        user_group = Group.objects.get(name='Usuario')

        superusers = User.objects.filter(is_superuser=True)
        for user in superusers:
            user.groups.add(admin_group)
        self.succes(f'Grupo Administrador atribuído a todos os superusuários.')

        moderadores = User.objects.filter(groups__name='Moderador')
        for user in moderadores:
            user.groups.add(moderador_group)
        self.succes('Grupo Moderador atribuído a todos os usuários moderadores.')

        suportes = User.objects.filter(groups__name='Suporte')
        for user in suportes:
            user.groups.add(suporte_group)  
        self.succes('Grupo Suporte atribuído a todos os usuários de suporte.')
        

        normal_users = User.objects.filter(is_superuser=False)
        for user in normal_users:
            user.groups.add(user_group)
        self.succes('Grupo Usuário atribuído a todos os usuários comuns.')