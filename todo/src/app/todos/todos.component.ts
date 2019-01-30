import { Component, OnInit } from '@angular/core';
import { MatCardModule } from '@angular/material/card';

import { Todo, TodoList } from '../todo';
import { TODOLISTS } from '../mock-todos';
import { TodosService } from '../todos.service';

@Component({
  selector: 'app-todos',
  templateUrl: './todos.component.html',
  styleUrls: ['./todos.component.sass']
})
export class TodosComponent implements OnInit {
  todolists: TodoList[];

  constructor(private todosService: TodosService) { }

  ngOnInit() {
    this.getTodoLists();
  }

  getTodoLists(): void {
    console.log("getting the todolists");
    this.todosService.getTodoLists()
      .subscribe(todolists => {this.todolists = todolists; console.log(todolists);});
  }
}
