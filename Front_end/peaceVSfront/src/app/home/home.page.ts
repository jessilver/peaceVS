import { Component } from '@angular/core';
import { IonContent } from '@ionic/angular/standalone';
import { NavbarComponent } from '../navbar/navbar.component';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
  imports: [IonContent, NavbarComponent],
})
export class HomePage {
  constructor() {}
}
