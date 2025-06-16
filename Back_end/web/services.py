from conteudo.models import Filme, Genero

def get_movies_by_category(genero_nome):
    genero = Genero.objects.filter(nome__iexact=genero_nome).first()
    if not genero:
        return []
    filmes = (
        Filme.objects.filter(generos=genero, ativo=True)
        .order_by('-data_adicao')[:20]
    )
    return [
        {
            'title': filme.titulo,
            'overview': filme.sinopse,
            'poster_url': filme.imagem_poster_url or 'https://via.placeholder.com/500x750.png?text=No+Image',
            'video_url': filme.arquivo_video_url,
        }
        for filme in filmes
    ]