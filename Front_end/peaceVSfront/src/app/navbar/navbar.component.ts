import { Component, OnInit } from '@angular/core';
import { IonHeader, IonToolbar, IonTitle, IonButtons, IonButton, IonIcon, IonPopover, IonContent, IonList, IonItem } from '@ionic/angular/standalone';
import { personCircleOutline } from 'ionicons/icons';
import { addIcons } from 'ionicons';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss'],
  standalone: true,
  imports: [CommonModule, IonHeader, IonToolbar, IonTitle, IonButtons, IonButton, IonIcon, IonPopover, IonContent, IonList, IonItem],
})
export class NavbarComponent implements OnInit {
  isLoggedIn = false;

  constructor() {
    addIcons({ personCircleOutline });
  }

  ngOnInit() {}

  onLogin() {
    this.isLoggedIn = true;
    console.log('User logged in');
  }

  onLogout() {
    this.isLoggedIn = false;
    console.log('User logged out');
  }

  get isUserLoggedIn(): boolean {
    return this.isLoggedIn;
  }
}
