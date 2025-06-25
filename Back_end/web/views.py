from django.shortcuts import render, redirect
from conteudo.models import Genero, Filme
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
from users.models import CustomUser as User
from django.contrib import messages
from django.views import View
from users.models import UserProfile
from django.db.models import Prefetch
from favoritos.models import FavoritoFilme, FavoritoSerie
from conteudo.models import Serie
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
from django.utils.text import slugify
from django.db import transaction

def home(request):
    favoritos_ids = FavoritoFilme.objects.filter(user=request.user).values_list('filme_id', flat=True) if request.user.is_authenticated else []
    # Categorias pré-definidas para a página inicial.
    # Cada consulta é separada, mas são poucas e diretas, muito mais rápidas que as chamadas de API.
    categorias = [
        {
            'name': 'Favoritos',
            'movie': Filme.objects.filter(id__in=favoritos_ids).order_by('-data_adicao') if request.user.is_authenticated else None,
        },
        {
            'name': 'Lançamentos Recentes',
            'movie': Filme.objects.filter(ativo=True).order_by('-ano_lancamento')[:40]
        },
        {
            'name': 'Ação',
            'movie': Filme.objects.filter(ativo=True, generos__nome='Ação').order_by('-ano_lancamento')[:40]
        },
        {
            'name': 'Comédia',
            'movie': Filme.objects.filter(ativo=True, generos__nome='Comédia').order_by('-ano_lancamento')[:40]
        },
        {
            'name': 'Ficção Científica',
            'movie': Filme.objects.filter(ativo=True, generos__nome='Ficção Científica').order_by('-ano_lancamento')[:40]
        }
    ]
    # Filtra apenas as categorias que retornaram filmes para não exibir carrosséis vazios.
    categorias_com_filmes = []
    for cat in categorias:
        filmes = cat['movie']
        if filmes and filmes.exists():
            filmes_list = [
                {
                    'id': filme.id,
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
    return render(request, 'web/home.html', {'categorias': categorias_com_filmes, 'favoritos_ids': favoritos_ids})

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
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        nome_perfil = request.POST.get('nome_perfil')

        if not all([email, password, first_name, last_name, nome_perfil]):
            messages.error(request, 'Todos os campos são obrigatórios.')
            return redirect('web_signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este email já está em uso.')
            return redirect('web_signup')

        try:
            # Cria o usuário
            user = User.objects.create_user(email=email, password=password)
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
                    'id': filme.id,
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

class FavoritosView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        favoritos_filmes = FavoritoFilme.objects.filter(user=request.user).select_related('filme')
        favoritos_series = FavoritoSerie.objects.filter(user=request.user).select_related('serie')
        return render(request, 'web/favoritos.html', {
            'favoritos_filmes': favoritos_filmes,
            'favoritos_series': favoritos_series,
        })

class CriarFilmeView(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            'generos': Genero.objects.all(),
        }
        return render(request, 'web/criar_filme.html', context)

    def post(self, request):
        try:
            titulo = request.POST.get('titulo')
            sinopse = request.POST.get('sinopse')
            ano_lancamento = request.POST.get('ano_lancamento')
            imagem_poster_url = request.POST.get('imagem_poster_url')
            classificacao_indicativa = request.POST.get('classificacao_indicativa')
            slug = slugify(titulo)
            ativo = request.POST.get('ativo') == 'on'
            duracao_minutos = request.POST.get('duracao_minutos')
            arquivo_video_url = request.POST.get('arquivo_video_url')
            generos_ids = request.POST.getlist('generos')

            # Criação do filme
            filme = Filme.objects.create(
                titulo=titulo,
                sinopse=sinopse,
                ano_lancamento=ano_lancamento,
                imagem_poster_url=imagem_poster_url,
                classificacao_indicativa=classificacao_indicativa,
                slug=slug,
                ativo=ativo,
                duracao_minutos=duracao_minutos,
                arquivo_video_url=arquivo_video_url,
            )

            # Adiciona os gêneros ao filme
            filme.generos.set(generos_ids)

            messages.success(request, 'Filme criado com sucesso!')
            return redirect('web_home')
        except Exception as e:
            messages.error(request, f'Ocorreu um erro ao criar o filme: {e}')
            return redirect('web_criar_filme')
        
class EditarFilmeView(LoginRequiredMixin, View):
    def get(self, request, id):
        try:
            filme = Filme.objects.get(id=id)
            generos_selecionados = list(filme.generos.values_list('id', flat=True))
            context = {
                'filme': filme,
                'generos': Genero.objects.all(),
                'generos_selecionados': generos_selecionados,
            }
            return render(request, 'web/editar_filme.html', context)
        except Filme.DoesNotExist:
            messages.error(request, 'Filme não encontrado.')
            return redirect('web_filmes')          

    def post(self, request, id):
        try:
            with transaction.atomic():
                filme = Filme.objects.get(id=id)
                titulo = request.POST.get('titulo')
                sinopse = request.POST.get('sinopse')
                ano_lancamento = request.POST.get('ano_lancamento')
                imagem_poster_url = request.POST.get('imagem_poster_url')
                classificacao_indicativa = request.POST.get('classificacao_indicativa')
                ativo = request.POST.get('ativo') == 'on'
                duracao_minutos = request.POST.get('duracao_minutos')
                arquivo_video_url = request.POST.get('arquivo_video_url')
                generos_ids = request.POST.getlist('generos')

                # Atualiza os campos do filme
                filme.titulo = titulo
                filme.sinopse = sinopse
                filme.ano_lancamento = ano_lancamento
                filme.imagem_poster_url = imagem_poster_url
                filme.classificacao_indicativa = classificacao_indicativa
                filme.ativo = ativo
                filme.duracao_minutos = duracao_minutos
                filme.arquivo_video_url = arquivo_video_url

                # Salva as alterações
                filme.save()

                # Atualiza os gêneros do filme
                filme.generos.set(generos_ids)

            messages.success(request, 'Filme atualizado com sucesso!')
            return redirect('web_home')
        except Filme.DoesNotExist:
            messages.error(request, 'Filme não encontrado.')
            return redirect('web_filmes') 
        except Exception as e:
            messages.error(request, f'Ocorreu um erro ao atualizar o filme: {e}')
            return redirect('web_editar_filme', id=id)
        
def deletarFilme(request, id):
    try:
        filme = Filme.objects.get(id=id)
        filme.delete()
        messages.success(request, 'Filme deletado com sucesso!')
    except Filme.DoesNotExist:
        messages.error(request, 'Filme não encontrado.')
    except Exception as e:
        messages.error(request, f'Ocorreu um erro ao deletar o filme: {e}')
    return redirect('web_home')

def adicionarFavorito(request, id):
    if request.user.is_authenticated:
        FavoritoFilme.objects.get_or_create(user=request.user, filme_id=id)
        messages.success(request, 'Filme adicionado aos favoritos!')
    return redirect('web_home')

def removerFavorito(request, id):
    if request.user.is_authenticated:
        FavoritoFilme.objects.filter(user=request.user, filme_id=id).delete()
        messages.success(request, 'Filme removido dos favoritos!')
    return redirect('web_home')