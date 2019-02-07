import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';

import { SettingsService } from '../settings.service';

export interface Message {
  message: string;
}

export interface SessionRestore {
  username: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  loggedIn: boolean = false;
  username: string;

  constructor(private http: HttpClient, private settings: SettingsService) { }

  isLoggedIn (username:string) {
    return new Observable( (observer) => {
      this.http.get<Message>(this.settings.api_url + '/is-logged-in/' + username, {withCredentials: true})
      .subscribe( (data) => {
        if (data.message == 'user is logged in') {
          this.loggedIn = true;
          this.username = username;
        } else {
          this.loggedIn = false;
        }
      });
    });
  }

  postRegister (username:string, password: string): Observable<Message> {
    let options = { withCredentials: true };
    return this.http.post<Message>(this.settings.api_url + '/register', {username, password}, options);
  }

  register (username:string, password:string) {
    return new Observable( (observer) => {
      this.postRegister(username, password)
        .subscribe( (data) => {
          observer.next(data.message);
      });
    });
  }

  postLogin (username:string, password: string): Observable<Message> {
    let options = { withCredentials: true };
    return this.http.post<Message>(this.settings.api_url + '/login', {username, password}, options);
  }

  doLogin (username: string, password: string) {
    return new Observable((observer) => {
      this.postLogin(username, password)
        .subscribe( (data: Message) => {
          if (data.message == 'success') {
            this.loggedIn = true;
            this.username = username;
            window.localStorage.setItem('username', username);
          }

          observer.next(data.message);
          observer.complete();
        },
        httperror => {
          observer.error(httperror);
        }
      );
    });
  }

  logOut () {
    this.username = '';
    this.loggedIn = false;
    let options = { withCredentials: true };
    this.http.post(this.settings.api_url + '/logout', options).subscribe();
  }
}
