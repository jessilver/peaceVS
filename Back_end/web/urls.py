from django.urls import path, include
from . import views
from .views import LoginView, LogoutView, SignupView, FavoritosView, CriarFilmeView, EditarFilmeView

urlpatterns = [
    path('', views.home, name='web_home'),
    path('login/', LoginView.as_view(), name='web_login'),
    path('logout/', LogoutView.as_view(), name='web_logout'),
    path('signup/', SignupView.as_view(), name='web_signup'),
    path('filmes/', views.filmes, name='web_filmes'),
    path('favoritos/', FavoritosView.as_view(), name='web_favoritos'),
    path('criar_filme/', CriarFilmeView.as_view(), name='web_criar_filme'),
    path('editar_filme/<int:id>/', EditarFilmeView.as_view(), name='web_editar_filme'),
    path('deletar_filme/<int:id>/', views.deletarFilme, name='web_deletar_filme'),
    path('adicionar_favorito/<int:id>/', views.adicionarFavorito, name='adicionar_favorito'),
    path('remover_favorito/<int:id>/', views.removerFavorito, name='remover_favorito'),
]
