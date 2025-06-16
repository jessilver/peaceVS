from django.shortcuts import render
from web.services import get_movies_by_category
from conteudo.models import Genero

def home(request):
    category_map = {
        'Populares',
        'Em Cartaz',
        'Melhores Avaliados',
        'Em Breve',
    }

    categorias = []

    for name in category_map:
        categorias.append({
            'name': name,
            'movie': get_movies_by_category(name),
        })

    return render(request, 'web/home.html', {'categorias': categorias})

def login(request):
    return render(request, 'web/login.html')

def signup(request):
    return render(request, 'web/signup.html')

def filmes(request):
    category_map = Genero.objects.values_list('nome', flat=True)

    categorias = []

    for name in category_map:
        categorias.append({
            'name': name,
            'movie': get_movies_by_category(name),
        })

    return render(request, 'web/home.html', {'categorias': categorias})
