from jessilver_django_seed.seeders.BaseSeeder import BaseSeeder
from media.models import Genero

class GeneroSeeder(BaseSeeder):
    @property
    def seeder_name(self):
        return 'GeneroSeeder'

    def seed(self):
        generos = ['Ação', 'Comédia', 'Drama', 'Ficção', 'Terror', 'Documentário']
        for nome in generos:
            obj, created = Genero.objects.get_or_create(nome=nome, slug=nome.lower())
            if created:
                self.succes(f'Genero {nome} criado')
            else:
                self.error(f'Genero {nome} já existe')
