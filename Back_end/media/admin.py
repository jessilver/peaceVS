from django.contrib import admin
from .models import Filme, Serie, Temporada, Episodio, Genero, Pessoa, CreditoMidia

@admin.register(Filme)
class FilmeAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ano_lancamento', 'ativo')
    search_fields = ('titulo',)
    list_filter = ('ativo', 'ano_lancamento', 'classificacao_indicativa')
    prepopulated_fields = {"slug": ("titulo",)}

@admin.register(Serie)
class SerieAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ano_lancamento', 'status', 'ativo')
    search_fields = ('titulo',)
    list_filter = ('status', 'ativo', 'ano_lancamento', 'classificacao_indicativa')
    prepopulated_fields = {"slug": ("titulo",)}

@admin.register(Temporada)
class TemporadaAdmin(admin.ModelAdmin):
    list_display = ('serie', 'numero_temporada', 'titulo', 'ano_lancamento')
    search_fields = ('serie__titulo', 'titulo')
    list_filter = ('serie',)

@admin.register(Episodio)
class EpisodioAdmin(admin.ModelAdmin):
    list_display = ('temporada', 'numero_episodio', 'titulo', 'duracao_minutos')
    search_fields = ('titulo', 'temporada__serie__titulo')
    list_filter = ('temporada',)

@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ('nome', 'slug')
    search_fields = ('nome',)
    prepopulated_fields = {"slug": ("nome",)}

@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'data_nascimento')
    search_fields = ('nome_completo',)
    prepopulated_fields = {"slug": ("nome_completo",)}

@admin.register(CreditoMidia)
class CreditoMidiaAdmin(admin.ModelAdmin):
    list_display = ('pessoa', 'filme', 'serie', 'tipo_credito', 'personagem_nome', 'ordem')
    search_fields = ('pessoa__nome_completo', 'filme__titulo', 'serie__titulo', 'personagem_nome')
    list_filter = ('tipo_credito',)
