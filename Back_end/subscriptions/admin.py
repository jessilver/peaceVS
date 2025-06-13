from django.contrib import admin
from .models import PlanoAssinatura, AssinaturaUsuario

@admin.register(PlanoAssinatura)
class PlanoAssinaturaAdmin(admin.ModelAdmin):
    list_display = ('nome_plano', 'preco_mensal', 'qualidade_video_permitida', 'numero_telas_simultaneas', 'ativo')
    search_fields = ('nome_plano',)
    list_filter = ('qualidade_video_permitida', 'ativo')
    prepopulated_fields = {"slug": ("nome_plano",)}

@admin.register(AssinaturaUsuario)
class AssinaturaUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'plano', 'status_assinatura', 'data_inicio', 'data_fim_periodo_corrente')
    search_fields = ('usuario__email', 'plano__nome_plano')
    list_filter = ('status_assinatura',)
