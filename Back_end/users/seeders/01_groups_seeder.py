from jessilver_django_seed.seeders.BaseSeeder import BaseSeeder
from django.contrib.auth.models import Group, Permission

class GroupsSeeder(BaseSeeder):
    @property
    def seeder_name(self):
        return 'GroupsSeeder'

    def seed(self):
        # Grupo: Administrador (acesso total)
        admin_group, admin_created = Group.objects.get_or_create(name='Administrador')
        admin_perms = Permission.objects.all()
        admin_group.permissions.set(admin_perms)

        # Grupo: Moderador (pode gerenciar conteúdo, mas não usuários/assinaturas)
        mod_group, mod_created = Group.objects.get_or_create(name='Moderador')
        mod_perms = Permission.objects.filter(
            content_type__app_label__in=['conteudo', 'interactions']
        )
        mod_group.permissions.set(mod_perms)

        # Grupo: Suporte (pode visualizar usuários e assinaturas, mas não editar)
        support_group, support_created = Group.objects.get_or_create(name='Suporte')
        support_perms = Permission.objects.filter(
            content_type__app_label__in=['users', 'subscriptions'],
            codename__startswith='view_'
        )
        support_group.permissions.set(support_perms)

        # Grupo: Usuario (permissões básicas, ex: visualizar próprio perfil)
        user_group, user_created = Group.objects.get_or_create(name='Usuario')
        user_perms = Permission.objects.filter(
            content_type__app_label='users',
            codename__startswith='view_'
        )
        user_group.permissions.set(user_perms)

        if not admin_created and not mod_created and not support_created and not user_created:
            self.error('Grupos de permissão já existem: Administrador, Moderador, Suporte, Usuário')
        else:
            self.success('Grupos de permissão criados e configurados: Administrador, Moderador, Suporte, Usuário')