import { Component, OnInit } from '@angular/core';
import { IonHeader, IonToolbar, IonTitle, IonButtons, IonButton, IonIcon, IonPopover, IonContent, IonList, IonItem } from '@ionic/angular/standalone';
import { personCircleOutline } from 'ionicons/icons';
import { addIcons } from 'ionicons';
import { CommonModule } from '@angular/common';
import { AuthService } from '../services/auth.service';
import { Router, RouterModule } from '@angular/router';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss'],
  standalone: true,
  imports: [CommonModule, IonHeader, IonToolbar, IonTitle, IonButtons, IonButton, IonIcon, IonPopover, IonContent, IonList, IonItem, RouterModule],
})
export class NavbarComponent implements OnInit {
  isLoggedIn = false;

  constructor(private authService: AuthService, private router: Router) {
    addIcons({ personCircleOutline });
  }

  ngOnInit() {
    this.isLoggedIn = this.authService.isAuthenticated();
  }

  onLogin() {
    this.isLoggedIn = true;
    console.log('User logged in');
  }

  onLogout() {
    this.authService.logout();
    this.isLoggedIn = false;
    this.router.navigate(['/login']);
    console.log('User logged out');
  }

  get isUserLoggedIn(): boolean {
    return this.isLoggedIn;
  }
}
