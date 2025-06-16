import { Component, OnInit } from '@angular/core';
import { IonContent, IonButton, IonList, IonItem, IonLabel, IonInput, IonRow, IonCol, IonCheckbox } from '@ionic/angular/standalone';
import { NavbarComponent } from '../navbar/navbar.component';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
  standalone: true,
  imports: [IonContent, IonButton, IonList, IonItem, IonLabel, IonInput, IonRow, IonCol, IonCheckbox, NavbarComponent],
})
export class LoginPage implements OnInit {

  constructor() { }

  ngOnInit() {
  }

}
