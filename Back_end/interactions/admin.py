from django.contrib import admin
from .models import ItemListaInteresse, HistoricoVisualizacao, Avaliacao

@admin.register(ItemListaInteresse)
class ItemListaInteresseAdmin(admin.ModelAdmin):
    list_display = ('perfil_usuario', 'conteudo_objeto', 'data_adicao')
    search_fields = ('perfil_usuario__nome_perfil',)
    list_filter = ('data_adicao',)

@admin.register(HistoricoVisualizacao)
class HistoricoVisualizacaoAdmin(admin.ModelAdmin):
    list_display = ('perfil_usuario', 'filme', 'episodio', 'progresso_segundos', 'concluido', 'ultima_visualizacao_em')
    search_fields = ('perfil_usuario__nome_perfil', 'filme__titulo', 'episodio__titulo')
    list_filter = ('concluido', 'ultima_visualizacao_em')

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('perfil_usuario', 'filme', 'serie', 'nota', 'data_avaliacao')
    search_fields = ('perfil_usuario__nome_perfil', 'filme__titulo', 'serie__titulo')
    list_filter = ('nota', 'data_avaliacao')
