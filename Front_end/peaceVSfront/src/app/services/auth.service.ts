import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private apiUrl = `${environment.apiUrl}/api/token/`;
  private userUrl = `${environment.apiUrl}/api/user/me/`;
  private loggedIn$ = new BehaviorSubject<boolean>(this.isAuthenticated());

  constructor(private http: HttpClient) {}

  login(email: string, password: string): Observable<any> {
    return this.http.post(this.apiUrl, { email, password });
  }

  setToken(token: string): void {
    localStorage.setItem('token', token);
    this.loggedIn$.next(true);
  }

  getToken(): string | null {
    return localStorage.getItem('token');
  }

  logout(): void {
    localStorage.removeItem('token');
    this.loggedIn$.next(false);
  }

  isAuthenticated(): boolean {
    return !!localStorage.getItem('token');
  }

  getCurrentUser(): Observable<any> {
    const token = this.getToken();
    const headers = new HttpHeaders({ Authorization: `Token ${token}` });
    return this.http.get(this.userUrl, { headers });
  }

  getLoggedInStatus() {
    return this.loggedIn$.asObservable();
  }
}
