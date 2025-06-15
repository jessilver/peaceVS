"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authtoken.views import obtain_auth_token
from django.views.generic import RedirectView

from users.views import CustomUserViewSet, UserProfileViewSet, CustomObtainAuthToken, UserSignupView, CurrentUserView, ApiRootView
from conteudo.views import FilmeViewSet, SerieViewSet, TemporadaViewSet, EpisodioViewSet, GeneroViewSet, PessoaViewSet, CreditoMidiaViewSet
from interactions.views import ItemListaInteresseViewSet, HistoricoVisualizacaoViewSet, AvaliacaoViewSet
from subscriptions.views import PlanoAssinaturaViewSet, AssinaturaUsuarioViewSet

router = routers.DefaultRouter()
# Users
router.register(r'users', CustomUserViewSet)
router.register(r'profiles', UserProfileViewSet)
# Media
router.register(r'filmes', FilmeViewSet)
router.register(r'series', SerieViewSet)
router.register(r'temporadas', TemporadaViewSet)
router.register(r'episodios', EpisodioViewSet)
router.register(r'generos', GeneroViewSet)
router.register(r'pessoas', PessoaViewSet)
router.register(r'creditos', CreditoMidiaViewSet)
# Interactions
router.register(r'lista-interesse', ItemListaInteresseViewSet)
router.register(r'historico', HistoricoVisualizacaoViewSet)
router.register(r'avaliacoes', AvaliacaoViewSet)
# Subscriptions
router.register(r'planos', PlanoAssinaturaViewSet)
router.register(r'assinaturas', AssinaturaUsuarioViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="PeaceVS API",
        default_version='v1',
        description="Documentação interativa da API do PeaceVS",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', RedirectView.as_view(url='/web/', permanent=False)),
    path('web/', include('web.urls')),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/user/me/', CurrentUserView.as_view(), name='current_user'),  # Protegida
    path('api/token/', CustomObtainAuthToken.as_view(), name='api_token_auth'),  # Pública
    path('api/signup/', UserSignupView.as_view(), name='api_signup'),  # Pública
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
