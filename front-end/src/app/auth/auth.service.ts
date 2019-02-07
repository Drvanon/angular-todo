import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';

import { SettingsService } from '../settings.service';

export interface Message {
  message: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  message: string;

  constructor(private http: HttpClient, private settings: SettingsService) {}

  isLoggedIn() {
  }

  getLogin (username:string, password: string): Observable<Message> {
    return this.http.post<Message>(this.settings.api_url + '/login', {username, password});
  }

  doLogin (username: string, password: string) {
    this.getLogin(username, password)
      .subscribe(
        (data: Message) => {this.message = data.message; console.log(data);},
        error => {this.message = 'Something went wrong while sending your request.'; console.log(error);}
      )
  }
}
