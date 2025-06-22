from jessilver_django_seed.seeders.BaseSeeder import BaseSeeder
from interactions.models import ItemListaInteresse
from users.models import UserProfile
from conteudo.models import Filme

class ItemListaInteresseSeeder(BaseSeeder):
    @property
    def seeder_name(self):
        return 'ItemListaInteresseSeeder'

    def seed(self):
        profile = UserProfile.objects.first()
        filme = Filme.objects.first()

        if not profile:
            self.error('Perfil de usuário não encontrado.')
            return
        
        if not filme:
            self.error('Filme não encontrado. Rode o seeder de filme antes.')
            return
        
        item, created = ItemListaInteresse.objects.get_or_create(
            perfil_usuario=profile,
            content_type_id=7,  # Ajuste conforme seu ambiente
            object_id=filme.id
        )
        if created:
            self.success('Item de lista de interesse criado')
        else:
            self.error('Item de lista de interesse já existe')
