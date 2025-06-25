from django.urls import path
from . import views
from .views import LoginView, LogoutView, SignupView, FavoritosView

urlpatterns = [
    path('', views.home, name='web_home'),
    path('login/', LoginView.as_view(), name='web_login'),
    path('logout/', LogoutView.as_view(), name='web_logout'),
    path('signup/', SignupView.as_view(), name='web_signup'),
    path('filmes/', views.filmes, name='web_filmes'),
    path('favoritos/', FavoritosView.as_view(), name='web_favoritos'),
]
