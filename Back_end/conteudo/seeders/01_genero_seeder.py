from jessilver_django_seed.seeders.BaseSeeder import BaseSeeder
from conteudo.models import Genero
import requests
import os

class GeneroSeeder(BaseSeeder):
    @property
    def seeder_name(self):
        return 'GeneroSeeder'

    def seed(self):
        api_key = os.getenv('TMDB_API_KEY')
        if not api_key:
            self.error('TMDB_API_KEY não definida no ambiente.')
            return
        url = f'https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=pt-BR'
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            generos = data.get('genres', [])
            # Gêneros/categorias extras para carrosséis
            categorias_extras = [
                {'name': 'Populares'},
                {'name': 'Em Cartaz'},
                {'name': 'Melhores Avaliados'},
                {'name': 'Em Breve'},
            ]
            for genero in generos + categorias_extras:
                nome = genero['name']
                slug = nome.lower().replace(' ', '-').replace('ç', 'c').replace('ã', 'a').replace('é', 'e')
                obj, created = Genero.objects.get_or_create(nome=nome, slug=slug)
                if created:
                    self.succes(f'Genero {nome} criado')
                else:
                    self.error(f'Genero {nome} já existe')
        except Exception as e:
            self.error(f'Erro ao buscar gêneros do TMDb: {e}')
