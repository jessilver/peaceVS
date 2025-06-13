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
        # Atribui o grupo Administrador a todos os superusers
        superusers = User.objects.filter(is_superuser=True)
        for user in superusers:
            user.groups.add(admin_group)
        self.succes(f'Grupo Administrador atribuído a todos os superusuários.')
