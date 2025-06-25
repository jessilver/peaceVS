import { Component } from '@angular/core';
import { IonContent, IonButton, IonList, IonItem, IonLabel, IonInput, IonRow, IonCol, IonCheckbox } from '@ionic/angular/standalone';
import { NavbarComponent } from '../navbar/navbar.component';
import { AuthService } from '../services/auth.service';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
  standalone: true,
  imports: [IonContent, IonButton, IonList, IonItem, IonLabel, IonInput, IonRow, IonCol, IonCheckbox, NavbarComponent, FormsModule],
})
export class LoginPage {
  email = '';
  password = '';
  errorMsg = '';

  constructor(private authService: AuthService, private router: Router) { }

  onLogin() {
    this.authService.login(this.email, this.password).subscribe({
      next: (res) => {
        if (res.token) {
          this.authService.setToken(res.token);
          this.router.navigateByUrl('/home', { skipLocationChange: false }).then(() => {
            window.location.reload();
          });
        }
      },
      error: () => {
        this.errorMsg = 'Email ou senha inválidos';
      }
    });
  }
}
