import { Component, AfterViewInit } from '@angular/core';

import { fromEvent } from 'rxjs';
import { ajax } from 'rxjs/ajax';
import { map, filter, debounceTime, distinctUntilChanged, switchMap } from 'rxjs/operators';
// import { Rx, keydown } from 'rx-dom';

import { AuthService } from '../auth.service';
import { SettingsService } from '../../settings.service';

interface Message {
  message: string;
}

/*type HTMLElementEvent<T extends HTMLElement> = Event & {
  target: T;
  // probably you might want to add the currentTarget as well
  // currentTarget: T;
}*/

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.sass']
})
export class RegisterComponent implements AfterViewInit {
  username: string;
  password: string;
  hide: boolean = true;
  message: string;
  showForm: boolean = true;
  submittable: boolean = true;

  constructor(private authservice: AuthService, private settings: SettingsService) { }

  ngAfterViewInit() {
    const input = document.getElementById('username');

    const source = fromEvent(input, 'input');

    const typeahead = source.pipe(
      map((e: KeyboardEvent) => { return (<HTMLInputElement>e.target).value }),
      filter( (text:string) => text.length > 2),
      debounceTime(10),
      distinctUntilChanged(),
      switchMap((string, index) => {
        return ajax(
          {
            url: this.settings.api_url + '/username-available/' + string,
            responseType: 'json'
          }
        )
      })
    );

    typeahead.subscribe( (data) => {
      this.submittable = (data.response.message == 'username available') ? true : false;
    });

  }

  onSubmit () {
    this.authservice.register(this.username, this.password)
      .subscribe( (data:string) => {
        this.message = data;
        if (this.message == 'success') {
          this.showForm = false;
        }
    });
  }
}
