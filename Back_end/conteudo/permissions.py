"""
As rotas de documentação da API (Swagger e Redoc) são públicas por padrão.
Veja em project/urls.py:

schema_view = get_schema_view(
    ...
    public=True,
    permission_classes=(permissions.AllowAny,),
)

Isso garante que qualquer usuário pode acessar /swagger/ e /redoc/.
"""

from rest_framework.permissions import BasePermission, SAFE_METHODS

class ReadOnlyOrAuthenticated(BasePermission):
    """
    Permite acesso de leitura (GET, HEAD, OPTIONS) a qualquer usuário,
    mas exige autenticação para métodos de escrita (POST, PUT, PATCH, DELETE).
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated
