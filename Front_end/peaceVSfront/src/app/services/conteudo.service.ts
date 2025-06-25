import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, Observer } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class ConteudoService {
  private apiBase = `${environment.apiUrl}/api/`;

  constructor(private http: HttpClient) {}

  // Filmes
  getFilmes(): Observable<any> {
    return this.http.get(this.apiBase + 'filmes/');
  }
  getFilme(id: number): Observable<any> {
    return this.http.get(this.apiBase + 'filmes/' + id + '/');
  }
  createFilme(data: any): Observable<any> {
    return this.http.post(this.apiBase + 'filmes/', data);
  }
  updateFilme(id: number, data: any): Observable<any> {
    return this.http.put(this.apiBase + 'filmes/' + id + '/', data);
  }
  deleteFilme(id: number): Observable<any> {
    return this.http.delete(this.apiBase + 'filmes/' + id + '/');
  }

  /**
   * Função utilitária para tratar filmes recebidos da API e padronizar estrutura
   */
  private tratarFilmes(filmes: any[]): any[] {
    return (filmes || []).map(filme => ({
      id: filme.id,
      title: filme.titulo,
      overview: filme.sinopse,
      poster_url: filme.imagem_poster_url || 'https://via.placeholder.com/500x750.png?text=No+Image',
      video_url: filme.arquivo_video_url,
    }));
  }

  /**
   * Busca filmes filtrando por gênero (id ou array de ids) e faz o tratamento dos dados para o frontend
   * @param generoId número | número[]
   */
  getFilmesPorGenero(generoId: number | number[]): Observable<any[]> {
    let param = Array.isArray(generoId) ? generoId.join(',') : generoId;
    return new Observable(observer => {
      this.http.get<any[]>(this.apiBase + 'filmes/', { params: { generos: param } }).subscribe({
        next: (filmes) => {
          observer.next(this.tratarFilmes(filmes));
          observer.complete();
        },
        error: err => observer.error(err)
      });
    });
  }

  /**
   * Busca filmes filtrando por nome do gênero (faz 2 requisições: busca id do gênero, depois busca filmes)
   * @param generoNome string
   */
  getFilmesPorNomeGenero(generoNome: string): Observable<any> {
    return new Observable((observer: Observer<any>) => {
      this.getGeneros().subscribe({
        next: generos => {
          const genero = generos.find((g: any) => g.nome.toLowerCase().includes(generoNome.toLowerCase()));
          if (!genero) {
            observer.next([]);
            observer.complete();
            return;
          }
          this.getFilmesPorGenero(genero.id).subscribe({
            next: filmes => {
              observer.next(filmes);
              observer.complete();
            },
            error: err => observer.error(err)
          });
        },
        error: err => observer.error(err)
      });
    });
  }

  // Séries
  getSeries(): Observable<any> {
    return this.http.get(this.apiBase + 'series/');
  }
  getSerie(id: number): Observable<any> {
    return this.http.get(this.apiBase + 'series/' + id + '/');
  }
  createSerie(data: any): Observable<any> {
    return this.http.post(this.apiBase + 'series/', data);
  }
  updateSerie(id: number, data: any): Observable<any> {
    return this.http.put(this.apiBase + 'series/' + id + '/', data);
  }
  deleteSerie(id: number): Observable<any> {
    return this.http.delete(this.apiBase + 'series/' + id + '/');
  }

  // Temporadas
  getTemporadas(): Observable<any> {
    return this.http.get(this.apiBase + 'temporadas/');
  }
  getTemporada(id: number): Observable<any> {
    return this.http.get(this.apiBase + 'temporadas/' + id + '/');
  }
  createTemporada(data: any): Observable<any> {
    return this.http.post(this.apiBase + 'temporadas/', data);
  }
  updateTemporada(id: number, data: any): Observable<any> {
    return this.http.put(this.apiBase + 'temporadas/' + id + '/', data);
  }
  deleteTemporada(id: number): Observable<any> {
    return this.http.delete(this.apiBase + 'temporadas/' + id + '/');
  }

  // Episódios
  getEpisodios(): Observable<any> {
    return this.http.get(this.apiBase + 'episodios/');
  }
  getEpisodio(id: number): Observable<any> {
    return this.http.get(this.apiBase + 'episodios/' + id + '/');
  }
  createEpisodio(data: any): Observable<any> {
    return this.http.post(this.apiBase + 'episodios/', data);
  }
  updateEpisodio(id: number, data: any): Observable<any> {
    return this.http.put(this.apiBase + 'episodios/' + id + '/', data);
  }
  deleteEpisodio(id: number): Observable<any> {
    return this.http.delete(this.apiBase + 'episodios/' + id + '/');
  }

  // Gêneros
  getGeneros(): Observable<any> {
    return this.http.get(this.apiBase + 'generos/');
  }
  getGenero(id: number): Observable<any> {
    return this.http.get(this.apiBase + 'generos/' + id + '/');
  }
  createGenero(data: any): Observable<any> {
    return this.http.post(this.apiBase + 'generos/', data);
  }
  updateGenero(id: number, data: any): Observable<any> {
    return this.http.put(this.apiBase + 'generos/' + id + '/', data);
  }
  deleteGenero(id: number): Observable<any> {
    return this.http.delete(this.apiBase + 'generos/' + id + '/');
  }

  // Pessoas
  getPessoas(): Observable<any> {
    return this.http.get(this.apiBase + 'pessoas/');
  }
  getPessoa(id: number): Observable<any> {
    return this.http.get(this.apiBase + 'pessoas/' + id + '/');
  }
  createPessoa(data: any): Observable<any> {
    return this.http.post(this.apiBase + 'pessoas/', data);
  }
  updatePessoa(id: number, data: any): Observable<any> {
    return this.http.put(this.apiBase + 'pessoas/' + id + '/', data);
  }
  deletePessoa(id: number): Observable<any> {
    return this.http.delete(this.apiBase + 'pessoas/' + id + '/');
  }

  // Créditos de mídia
  getCreditos(): Observable<any> {
    return this.http.get(this.apiBase + 'creditos/');
  }
  getCredito(id: number): Observable<any> {
    return this.http.get(this.apiBase + 'creditos/' + id + '/');
  }
  createCredito(data: any): Observable<any> {
    return this.http.post(this.apiBase + 'creditos/', data);
  }
  updateCredito(id: number, data: any): Observable<any> {
    return this.http.put(this.apiBase + 'creditos/' + id + '/', data);
  }
  deleteCredito(id: number): Observable<any> {
    return this.http.delete(this.apiBase + 'creditos/' + id + '/');
  }

  // Favoritos
  adicionarFilmeAosFavoritos(filmeId: number) {
    const token = localStorage.getItem('token');
    const headers = token ? new HttpHeaders({ Authorization: `Token ${token}` }) : undefined;
    return this.http.post(this.apiBase + 'favoritos-filmes/', { filme: filmeId }, { headers });
  }
  
  removerFilmeDosFavoritos(filmeId: number) {
    const token = localStorage.getItem('token');
    const headers = token ? new HttpHeaders({ Authorization: `Token ${token}` }) : undefined;
    return this.http.delete(this.apiBase + 'favoritos-filmes/' + filmeId + '/', { headers });
  }

  /**
   * Busca os filmes favoritos do usuário e faz o tratamento dos dados para o frontend
   * Agora retorna também o favoritoId (id do registro FavoritoFilme)
   */
  getFilmesFavoritos(): Observable<any[]> {
    const token = localStorage.getItem('token');
    const headers = token ? new HttpHeaders({ Authorization: `Token ${token}` }) : undefined;
    return new Observable(observer => {
      this.http.get<any[]>(this.apiBase + 'filmes-favoritos/', { headers }).subscribe({
        next: (favoritos) => {
          // favoritos: [{id, filme: {...}}]
          const filmesTratados = (favoritos || []).map(fav => ({
            favoritoId: fav.id,
            ...this.tratarFilmes([fav.filme])[0]
          }));
          observer.next(filmesTratados);
          observer.complete();
        },
        error: err => observer.error(err)
      });
    });
  }
}
