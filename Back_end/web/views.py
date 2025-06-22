from django.shortcuts import render, redirect
from conteudo.models import Genero, Filme
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View
from users.models import UserProfile
from django.db.models import Prefetch

def home(request):
    # Categorias pré-definidas para a página inicial.
    # Cada consulta é separada, mas são poucas e diretas, muito mais rápidas que as chamadas de API.
    categorias = [
        {
            'name': 'Lançamentos Recentes',
            'movie': Filme.objects.filter(ativo=True).order_by('-data_adicao')[:20]
        },
        {
            'name': 'Ação',
            'movie': Filme.objects.filter(ativo=True, generos__nome='Ação').order_by('-data_adicao')[:20]
        },
        {
            'name': 'Comédia',
            'movie': Filme.objects.filter(ativo=True, generos__nome='Comédia').order_by('-data_adicao')[:20]
        },
        {
            'name': 'Ficção Científica',
            'movie': Filme.objects.filter(ativo=True, generos__nome='Ficção Científica').order_by('-data_adicao')[:20]
        }
    ]
    # Filtra apenas as categorias que retornaram filmes para não exibir carrosséis vazios.
    categorias_com_filmes = []
    for cat in categorias:
        filmes = cat['movie']
        if filmes.exists():
            filmes_list = [
                {
                    'poster_url': getattr(filme, 'imagem_poster_url', ''),
                    'title': getattr(filme, 'titulo', ''),
                    'overview': getattr(filme, 'sinopse', ''),
                }
                for filme in filmes
            ]
            if filmes_list:
                categorias_com_filmes.append({
                    'name': cat['name'],
                    'movie': filmes_list
                })
    print(categorias_com_filmes)  # Para depuração, pode ser removido depois
    return render(request, 'web/home.html', {'categorias': categorias_com_filmes})

class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'web/login.html')

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Buscar o nome do perfil principal do usuário
            user_profile = UserProfile.objects.filter(user=user).first()
            nome_perfil = user_profile.nome_perfil if user_profile else user.email
            messages.success(request, f'Bem-vindo de volta, {nome_perfil}!')
            return redirect('web_home')
        else:
            messages.error(request, 'Credenciais inválidas. Por favor, tente novamente.')
            return redirect('web_login')


class LogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('web_home')


class SignupView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'web/signup.html')

    def post(self, request, *args, **kwargs):
        username = request.POST.get('email')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        nome_perfil = request.POST.get('nome_perfil')

        if not all([email, password, first_name, last_name, nome_perfil]):
            messages.error(request, 'Todos os campos são obrigatórios.')
            return redirect('web_signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Este email já está em uso.')
            return redirect('web_signup')

        try:
            # Cria o usuário
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            # Cria o perfil do usuário
            UserProfile.objects.create(user=user, nome_perfil=nome_perfil)

            # Faz o login
            login(request, user)
            messages.success(request, 'Sua conta foi criada com sucesso! Bem-vindo!')
            return redirect('web_home')
        except Exception as e:
            messages.error(request, f'Ocorreu um erro inesperado durante o cadastro: {e}')
            return redirect('web_signup')


def filmes(request):
    # Otimização para buscar todos os gêneros e seus filmes de forma eficiente.
    # Usa Prefetch para evitar o problema de N+1 queries, resultando em apenas 2 consultas ao banco.
    prefetch_filmes_ativos = Prefetch(
        'filmes',
        queryset=Filme.objects.filter(ativo=True).order_by('-data_adicao'),
        to_attr='filmes_ativos'  # Atributo customizado para guardar os filmes pré-buscados
    )

    generos_com_filmes = Genero.objects.prefetch_related(prefetch_filmes_ativos).filter(filmes__ativo=True).distinct()

    # Monta a estrutura de dados que o template espera
    categorias = []
    for genero in generos_com_filmes:
        # Acessa os filmes do atributo customizado 'filmes_ativos'
        if hasattr(genero, 'filmes_ativos') and genero.filmes_ativos:
            filmes_list = [
                {
                    'poster_url': getattr(filme, 'imagem_poster_url', ''),
                    'title': getattr(filme, 'titulo', ''),
                    'overview': getattr(filme, 'sinopse', ''),
                }
                for filme in genero.filmes_ativos
            ]
            if filmes_list:
                categorias.append({
                    'name': genero.nome,
                    'movie': filmes_list
                })

    # A view 'filmes' reutiliza o template 'home.html', então a estrutura de dados deve ser a mesma.
    return render(request, 'web/home.html', {'categorias': categorias})
