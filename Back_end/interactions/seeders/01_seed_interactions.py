from jessilver_django_seed.seeders.BaseSeeder import BaseSeeder
from users.models import CustomUser
from media.models import Filme, Serie, Episodio
from interactions.models import ItemListaInteresse, HistoricoVisualizacao, Avaliacao

class SampleInteractionsSeeder(BaseSeeder):
    @property
    def seeder_name(self):
        return 'SampleInteractionsSeeder'

    def seed(self):
        user = CustomUser.objects.filter(is_superuser=False).first()
        if not user:
            self.warn('Nenhum usuário comum encontrado para criar interações.')
            return
        profile = user.profiles.first()
        filme = Filme.objects.first()
        serie = Serie.objects.first()
        episodio = Episodio.objects.first()
        # Lista de interesse
        if filme:
            ItemListaInteresse.objects.get_or_create(perfil_usuario=profile, content_type_id=7, object_id=filme.id)  # Ajuste o content_type_id conforme seu ambiente
        # Histórico
        if filme:
            HistoricoVisualizacao.objects.get_or_create(perfil_usuario=profile, filme=filme, progresso_segundos=60, concluido=False)
        if episodio:
            HistoricoVisualizacao.objects.get_or_create(perfil_usuario=profile, episodio=episodio, progresso_segundos=120, concluido=True)
        # Avaliação
        if filme:
            Avaliacao.objects.get_or_create(perfil_usuario=profile, filme=filme, nota=5, comentario_texto='Ótimo filme!')
        if serie:
            Avaliacao.objects.get_or_create(perfil_usuario=profile, serie=serie, nota=4, comentario_texto='Boa série!')
        self.succes('Interações de exemplo criadas com sucesso!')
