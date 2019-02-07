import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class SettingsService {
  api_url:string = 'http://localhost:5000';

  constructor() { }
}
