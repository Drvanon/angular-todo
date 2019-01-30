import { Observable, of } from 'rxjs';
import { Injectable } from '@angular/core';
import { TodoList, Todo } from './todo';
import { TODOLISTS } from './mock-todos';

@Injectable({
  providedIn: 'root'
})
export class TodosService {

  constructor() { }

  getTodoLists(): Observable<TodoList[]> {
    return of(TODOLISTS);
  }
}
