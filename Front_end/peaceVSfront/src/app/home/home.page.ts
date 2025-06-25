import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonContent, IonButton } from '@ionic/angular/standalone';
import { NavbarComponent } from '../navbar/navbar.component';
import { AuthService } from '../services/auth.service';
import { ConteudoService } from '../services/conteudo.service';
import { forkJoin } from 'rxjs';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
  imports: [CommonModule, IonContent, NavbarComponent, IonButton],
})
export class HomePage implements OnInit {
  user: any = null;
  generos: string[] = [
    'Ação', 'Comédia', 'Terror', 'Romance', 'Ficção', 'Animação', 'Aventura'
  ];
  filmesPorGenero: { genero: string, filmes: any[] }[] = [];
  filmeSelecionado: any = null;
  filmesFavoritos: any[] = [];
  filmeSelecionadoFavorito: boolean = false;

  constructor(private authService: AuthService, private conteudoService: ConteudoService) {}
  category_map = [
    'Populares',
    'Em Cartaz',
    'Melhores Avaliados',
    'Em Breve',
  ];
  
  ngOnInit() {
    this.authService.getCurrentUser().subscribe({
      next: (data) => {
        this.user = data;
        // Buscar favoritos se usuário logado
        this.conteudoService.getFilmesFavoritos().subscribe({
          next: (favoritos) => {
            this.filmesFavoritos = favoritos || [];
          },
          error: () => {
            this.filmesFavoritos = [];
          }
        });
      },
      error: (err) => this.user = null
    });
    // Buscar filmes para todos os gêneros
    const requests = this.generos.map(genero =>
      this.conteudoService.getFilmesPorNomeGenero(genero)
    );
    forkJoin(requests).subscribe({
      next: (resultados) => {
        this.filmesPorGenero = this.generos.map((genero, idx) => ({
          genero,
          filmes: resultados[idx] || []
        }));
      },
      error: () => {
        this.filmesPorGenero = [];
      }
    });
  }

  isAllEmpty(): boolean {
    return this.filmesPorGenero && this.filmesPorGenero.length > 0 && this.filmesPorGenero.every(g => g.filmes.length === 0);
  }

  selecionarFilme(filme: any) {
    this.filmeSelecionado = filme;
    // Verifica se o filme está nos favoritos
    this.filmeSelecionadoFavorito = this.filmesFavoritos.some(fav => fav.id === filme.id);
  }

  fecharDetalhes() {
    this.filmeSelecionado = null;
  }

  adicionarAosFavoritos(filme: any) {
    if (!filme || !filme.id) {
      alert('Filme inválido para favoritar.');
      return;
    }
    if (this.filmesFavoritos.some(fav => fav.id === filme.id)) {
      alert('Este filme já está nos seus favoritos!');
      return;
    }
    this.conteudoService.adicionarFilmeAosFavoritos(filme.id).subscribe({
      next: () => {
        alert('Filme adicionado aos favoritos!');
        // Atualiza a lista de favoritos após adicionar
        this.conteudoService.getFilmesFavoritos().subscribe({
          next: (favoritos) => {
            this.filmesFavoritos = favoritos || [];
          }
        });
      },
      error: (err) => {
        alert('Erro ao adicionar aos favoritos: ' + (err?.error?.detail || err.message));
      }
    });
  }

  removerDosFavoritos(filme: any) {
    if (!filme || !filme.favoritoId) return;
    this.conteudoService.removerFilmeDosFavoritos(filme.favoritoId).subscribe({
      next: () => {
        this.filmesFavoritos = this.filmesFavoritos.filter(fav => fav.favoritoId !== filme.favoritoId);
        this.fecharDetalhes();
        alert('Filme removido dos favoritos!');
      },
      error: (err) => {
        alert('Erro ao remover dos favoritos: ' + (err?.error?.detail || err.message));
      }
    });
  }
}
