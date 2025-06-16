from django.shortcuts import render
from web.services import get_movies_by_category

def home(request):
    category_map = {
        'populares': 'Populares',
        'em_cartaz': 'Em Cartaz',
        'melhores_avaliados': 'Melhores Avaliados',
        'em_breve': 'Em Breve',
    }

    categorias = [
        {
            'name': 'Populares',
            'movie': get_movies_by_category(category_map['populares']),
        }, 
        {
            'name': 'Em Cartaz',
            'movie': get_movies_by_category(category_map['em_cartaz']),
        }, 
        {
            'name': 'Melhores Avaliados',
            'movie': get_movies_by_category(category_map['melhores_avaliados']),
        }, 
        {
            'name': 'Em Breve',
            'movie': get_movies_by_category(category_map['em_breve']),
        }
    ]

    return render(request, 'web/home.html', {'categorias': categorias})

def login(request):
    return render(request, 'web/login.html')

def signup(request):
    return render(request, 'web/signup.html')

# Create your views here.
