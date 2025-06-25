from jessilver_django_seed.seeders.BaseSeeder import BaseSeeder
from conteudo.models import Serie, Genero, Temporada, Episodio
import requests
import os
from django.utils.text import slugify

class SerieSeeder(BaseSeeder):
    @property
    def seeder_name(self):
        return 'SerieSeeder'

    def seed(self):
        api_key = os.getenv('TMDB_API_KEY')
        if not api_key:
            self.error('TMDB_API_KEY não definida no ambiente.')
            return
        categorias = [
            ('Populares', 'popular'),
            ('No Ar', 'on_the_air'),
            ('Melhores Avaliadas', 'top_rated'),
            ('Hoje', 'airing_today'),
        ]
        for nome_categoria, endpoint in categorias:
            genero_categoria = Genero.objects.filter(nome=nome_categoria).first()
            if not genero_categoria:
                self.error(f"Gênero '{nome_categoria}' não encontrado. Rode o seeder de gênero antes.")
                continue
            url = f'https://api.themoviedb.org/3/tv/{endpoint}?api_key={api_key}&language=pt-BR&page=1'
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                series = data.get('results', [])
                for serie_data in series:
                    titulo = serie_data.get('name')
                    if not titulo:
                        continue
                    base_slug = slugify(titulo)
                    slug = base_slug
                    i = 2
                    while Serie.objects.filter(slug=slug).exists():
                        slug = f"{base_slug}-{i}"
                        i += 1
                    serie, created = Serie.objects.get_or_create(
                        titulo=titulo,
                        defaults={
                            'sinopse': serie_data.get('overview') or '',
                            'ano_lancamento': int(serie_data.get('first_air_date', '2000')[:4]) if serie_data.get('first_air_date') else 2000,
                            'status': 'EM_ANDAMENTO',
                            'slug': slug,
                            'ativo': True,
                            'imagem_poster_url': f"https://image.tmdb.org/t/p/w500{serie_data.get('poster_path')}" if serie_data.get('poster_path') else ''
                        }
                    )
                    if created:
                        # Associa gêneros do TMDb
                        for genero_id in serie_data.get('genre_ids', []):
                            genero = Genero.objects.filter(id=genero_id).first()
                            if genero:
                                serie.generos.add(genero)
                        # Associa também ao gênero da categoria
                        if genero_categoria:
                            serie.generos.add(genero_categoria)
                        self.success(f'Série {titulo} criada e associada a {nome_categoria}')
                    else:
                        # Garante associação à categoria mesmo se já existir
                        if genero_categoria:
                            serie.generos.add(genero_categoria)
                        self.error(f'Série {titulo} já existe, mas foi associada a {nome_categoria}')

                    # --- Temporadas e Episódios ---
                    tmdb_id = serie_data.get('id')
                    if tmdb_id:
                        url_temporadas = f'https://api.themoviedb.org/3/tv/{tmdb_id}?api_key={api_key}&language=pt-BR'
                        try:
                            resp_temp = requests.get(url_temporadas)
                            resp_temp.raise_for_status()
                            detalhes_serie = resp_temp.json()
                            for temp in detalhes_serie.get('seasons', []):
                                numero_temporada = temp.get('season_number')
                                nome_temporada = temp.get('name')
                                sinopse_temporada = temp.get('overview') or ''
                                ano_temp = int(temp.get('air_date', '2000')[:4]) if temp.get('air_date') else ano
                                poster_temp = temp.get('poster_path')
                                poster_url_temp = f"https://image.tmdb.org/t/p/w500{poster_temp}" if poster_temp else ''
                                temporada, temp_created = Temporada.objects.get_or_create(
                                    serie=serie,
                                    numero_temporada=numero_temporada,
                                    defaults={
                                        'titulo': nome_temporada,
                                        'ano_lancamento': ano_temp,
                                        'imagem_poster_url': poster_url_temp
                                    }
                                )
                                # Episódios
                                url_episodios = f'https://api.themoviedb.org/3/tv/{tmdb_id}/season/{numero_temporada}?api_key={api_key}&language=pt-BR'
                                try:
                                    resp_epi = requests.get(url_episodios)
                                    resp_epi.raise_for_status()
                                    dados_temp = resp_epi.json()
                                    for ep in dados_temp.get('episodes', []):
                                        numero_episodio = ep.get('episode_number')
                                        titulo_ep = ep.get('name')
                                        sinopse_ep = ep.get('overview') or ''
                                        ano_ep = int(ep.get('air_date', '2000')[:4]) if ep.get('air_date') else ano_temp
                                        poster_ep = ep.get('still_path')
                                        poster_url_ep = f"https://image.tmdb.org/t/p/w500{poster_ep}" if poster_ep else ''
                                        Episodio.objects.get_or_create(
                                            temporada=temporada,
                                            numero_episodio=numero_episodio,
                                            defaults={
                                                'titulo': titulo_ep,
                                                'sinopse': sinopse_ep,
                                                'data_lancamento_original': ep.get('air_date') if ep.get('air_date') else None,
                                                'imagem_thumbnail_url': poster_url_ep,
                                                'duracao_minutos': 45,  # valor fictício padrão
                                                'arquivo_video_url': ''  # não disponível
                                            }
                                        )
                                except Exception as e:
                                    self.error(f'Erro ao buscar episódios da temporada {numero_temporada} da série {titulo}: {e}')
                        except Exception as e:
                            self.error(f'Erro ao buscar temporadas da série {titulo}: {e}')
            except Exception as e:
                self.error(f'Erro ao buscar séries do TMDb para {nome_categoria}: {e}')
