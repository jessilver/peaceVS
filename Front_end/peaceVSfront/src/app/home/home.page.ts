import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonContent } from '@ionic/angular/standalone';
import { NavbarComponent } from '../navbar/navbar.component';
import { AuthService } from '../services/auth.service';
import { ConteudoService } from '../services/conteudo.service';
import { forkJoin } from 'rxjs';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
  imports: [CommonModule, IonContent, NavbarComponent],
})
export class HomePage implements OnInit {
  user: any = null;
  generos: string[] = [
    'Ação', 'Comédia', 'Terror', 'Romance', 'Ficção', 'Animação', 'Aventura'
  ];
  filmesPorGenero: { genero: string, filmes: any[] }[] = [];
  filmeSelecionado: any = null;

  constructor(private authService: AuthService, private conteudoService: ConteudoService) {}
  category_map = [
    'Populares',
    'Em Cartaz',
    'Melhores Avaliados',
    'Em Breve',
  ];
  
  ngOnInit() {
    this.authService.getCurrentUser().subscribe({
      next: (data) => this.user = data,
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
  }

  fecharDetalhes() {
    this.filmeSelecionado = null;
  }
}
