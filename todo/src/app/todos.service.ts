import { Observable, of } from 'rxjs';
import { Injectable } from '@angular/core';
import { TodoList, Todo } from './todo';
import { TODOLISTS } from './mock-todos';

// TODO: Good error handling. Right now void is returned, should
// the server return a fail.

@Injectable({
  providedIn: 'root'
})
export class TodosService {

  constructor() { }

  getTodoLists(): Observable<TodoList[]> {
    return of(TODOLISTS);
  }

  removeTodoList(todolist: TodoList) {
    // TODO: delete id to server
 }

  addTodoList(title: string): void {
    // TODO: post title to server
  }

  saveTodoList(todolist: TodoList): void {
    // TODO: post todo to server
  }
}
