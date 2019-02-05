import { Component, OnInit } from '@angular/core';
import { LoginService } from '../auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.sass']
})
export class LoginComponent implements OnInit {
  logged_in = false;

  constructor() { }

  ngOnInit() {
  }

  onSubmit () {

  }
}
