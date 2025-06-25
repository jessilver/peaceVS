from jessilver_django_seed.seeders.BaseSeeder import BaseSeeder
from conteudo.models import Filme, Genero
from django.utils.text import slugify
import requests
import os

class FilmeSeeder(BaseSeeder):
    @property
    def seeder_name(self):
        return 'FilmeSeeder'

    def seed(self):
        api_key = os.getenv('TMDB_API_KEY')
        if not api_key:
            self.error('TMDB_API_KEY não definidas no ambiente.')
            return
        categorias = [
            ('Populares', 'popular'),
            ('Em Cartaz', 'now_playing'),
            ('Melhores Avaliados', 'top_rated'),
            ('Em Breve', 'upcoming'),
            ('Ação', 28),
            ('Aventura', 12),
            ('Animação', 16),
            ('Comédia', 35),
            ('Crime', 80),
            ('Drama', 18),
            ('Família', 10751),
            ('Fantasia', 14),
            ('História', 36),
            ('Terror', 27),
            ('Música', 10402),
            ('Mistério', 9648),
            ('Romance', 10749),
            ('Ficção científica', 878),
            ('Cinema TV', 10770),
            ('Thriller', 53),
            ('Guerra', 10752),
            ('Faroeste', 37),
        ]
        for nome_categoria, endpoint in categorias:
            genero_categoria = Genero.objects.filter(nome=nome_categoria).first()
            if not genero_categoria:
                self.error(f"Gênero '{nome_categoria}' não encontrado. Rode o seeder de gênero antes.")
                continue
            # Corrige a URL para gêneros TMDb
            if isinstance(endpoint, int):
                url = f'https://api.themoviedb.org/3/discover/movie?api_key={api_key}&language=pt-BR&page=1&with_genres={endpoint}'
            else:
                url = f'https://api.themoviedb.org/3/movie/{endpoint}?api_key={api_key}&language=pt-BR&page=1'
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                filmes = data.get('results', [])
                for movie in filmes:
                    # Ignora filmes que tenham o gênero Documentário (id 99)
                    if 99 in movie.get('genre_ids', []):
                        continue
                    titulo = movie.get('title')
                    sinopse = movie.get('overview') or ''
                    ano = int(movie.get('release_date', '2000')[:4]) if movie.get('release_date') else 2000
                    poster_path = movie.get('poster_path')
                    poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else ''
                    base_slug = slugify(titulo)
                    slug = base_slug
                    i = 2
                    while Filme.objects.filter(slug=slug).exists():
                        slug = f"{base_slug}-{i}"
                        i += 1
                    filme, created = Filme.objects.get_or_create(
                        titulo=titulo,
                        defaults={
                            'sinopse': sinopse,
                            'ano_lancamento': ano,
                            'imagem_poster_url': poster_url,
                            'duracao_minutos': 120,  # valor fictício
                            'arquivo_video_url': '',  # não disponível
                            'slug': slug,
                            'ativo': True
                        }
                    )
                    if created:
                        # Associa gêneros do TMDb
                        for genero_id in movie.get('genre_ids', []):
                            genero = Genero.objects.filter(id=genero_id).first()
                            if genero:
                                filme.generos.add(genero)
                        # Associa também ao gênero da categoria
                        filme.generos.add(genero_categoria)
                        self.success(f'Filme {titulo} criado e associado a {nome_categoria}')
                    else:
                        # Garante associação à categoria mesmo se já existir
                        filme.generos.add(genero_categoria)
                        self.error(f'Filme {titulo} já existe, mas foi associado a {nome_categoria}')
            except Exception as e:
                self.error(f'Erro ao buscar filmes do TMDb para {nome_categoria}: {e}')
