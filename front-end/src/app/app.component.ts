import { Component, OnInit } from '@angular/core';
import { AuthService } from './auth/auth.service';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatCardModule } from '@angular/material';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.sass']
})
export class AppComponent implements OnInit {
  brand = 'Todo';
  constructor (private authservice: AuthService) {}

  ngOnInit () {
    if(window.localStorage.getItem('username')) {
      this.authservice.isLoggedIn(window.localStorage.getItem('username'))
        .subscribe();
    }
  }

  logOut () {
    this.authservice.logOut();
    window.localStorage.removeItem('username');
  }
}
