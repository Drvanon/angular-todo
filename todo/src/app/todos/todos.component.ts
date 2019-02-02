import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';

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
  todolistForm = new FormGroup({
    newTitle: new FormControl('')
  });

  constructor(private todosService: TodosService) { }

  ngOnInit() {
    this.getTodoLists();
  }

  getTodoLists(): void {
    this.todosService.getTodoLists()
      .subscribe(todolists => this.todolists = todolists);
  }

  removeTodoList(todolist: TodoList): void {
    this.todolists = this.todolists.filter(tl => tl != todolist);
    this.todosService.removeTodoList(todolist);
  }

  addTodoListSubmit(): void {
    this.todosService.addTodoList(this.todolistForm.value.newTitle);
    // TODO: replace this when we have a server up
    // this.todosService.getTodoLists()
    //   .subscribe(todolists => this.todolists = todolists);
    this.todolists.push({ title: this.todolistForm.value.newTitle, todos: [] } as TodoList);
  }

 removeTodo(todolist: TodoList, todo: Todo): void {
    todolist.todos = todolist.todos.filter(t => t != todo);
    this.todosService.removeTodoList(todolist);
  }

  addTodo(todolist: TodoList): void {
    todolist.todos.push({id: 0, text: todolist.newTodo, finished: false});
    this.todosService.saveTodoList(todolist);
    todolist.newTodo = '';
  }
}
