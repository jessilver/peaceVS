import requests
from django.conf import settings

from conteudo.models import Filme, Genero

API_URL = getattr(settings, 'API_URL', 'http://localhost:8000/api/')

def get_movies_by_category(genero_nome):
    # Busca o id do gênero pela API
    genero_resp = requests.get(f"{API_URL}generos/", params={"search": genero_nome})
    if genero_resp.status_code != 200 or not genero_resp.json():
        return []
    genero_id = None
    for genero in genero_resp.json():
        if genero_nome.lower() in genero.get('nome', '').lower():
            genero_id = genero['id']
            break
    if not genero_id:
        return []
    # Busca filmes filtrando pelo id do gênero
    filmes_resp = requests.get(f"{API_URL}filmes/", params={"generos": genero_id})
    if filmes_resp.status_code != 200:
        return []
    filmes = filmes_resp.json()
    return [
        {
            'title': filme['titulo'],
            'overview': filme['sinopse'],
            'poster_url': filme.get('imagem_poster_url') or 'https://via.placeholder.com/500x750.png?text=No+Image',
            'video_url': filme['arquivo_video_url'],
        }
        for filme in filmes
    ]