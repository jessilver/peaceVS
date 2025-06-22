import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, Observer } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ConteudoService {
  private apiBase = 'http://192.168.1.140:8000/api/';

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
   * Busca filmes filtrando por gênero (id ou array de ids) e faz o tratamento dos dados para o frontend
   * @param generoId número | número[]
   */
  getFilmesPorGenero(generoId: number | number[]): Observable<any[]> {
    let param = Array.isArray(generoId) ? generoId.join(',') : generoId;
    return new Observable(observer => {
      this.http.get<any[]>(this.apiBase + 'filmes/', { params: { generos: param } }).subscribe({
        next: (filmes) => {
          const filmesTratados = (filmes || []).map(filme => ({
            title: filme.titulo,
            overview: filme.sinopse,
            poster_url: filme.imagem_poster_url || 'https://via.placeholder.com/500x750.png?text=No+Image',
            video_url: filme.arquivo_video_url,
          }));
          observer.next(filmesTratados);
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
}
