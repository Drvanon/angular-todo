import { Component, OnInit } from '@angular/core';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.sass']
})
export class LoginComponent implements OnInit {
  logged_in: boolean = false;
  username: string;
  password: string;
  hide: boolean = true;

  constructor(private authservice: AuthService) { }

  ngOnInit() {
  }

  onSubmit () {
    // Assumes HTTPS connection for security
    this.authservice.doLogin(this.username, this.password);
  }
}
