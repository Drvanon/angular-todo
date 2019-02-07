import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
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
  message: string;

  constructor(private authservice: AuthService, private router: Router) { }

  ngOnInit() {
  }

  onSubmit () {
    // Assumes HTTPS connection for security
    this.authservice.doLogin(this.username, this.password)
      .subscribe( (data:string) => {
        this.message = data;
        if (data == 'success') {
          this.router.navigate(['/']);
        }
      });
  }
}
