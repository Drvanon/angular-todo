export class Todo {
    id: number;
    text: string;
    finished: boolean;
}

export class TodoList {
    id: number;
    title: string;
    todos: Array<Todo>;
}
