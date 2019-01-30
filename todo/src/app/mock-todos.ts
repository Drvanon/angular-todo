import { TodoList, Todo } from './todo';

export const TODOLISTS: TodoList[] = [
    {
        id: 1,
        title: 'groceries',
        todos: [
            {
                id: 1,
                finished: false,
                text: 'Unions'
            },
            {
                id: 2,
                finished: false,
                text: 'Eggs'
            },
            {
                id: 3,
                finished: false,
                text: 'Butter'
            },
            {
                id: 4,
                finished: false,
                text: 'Milk'
            },
            {
                id: 5,
                finished: true,
                text: 'Liquorice'
            }
        ]
    },
    {
        id: 2,
        title: 'tasks',
        todos: [
            {
                id: 6,
                finished: false,
                text: 'Clean'
            },
            {
                id: 7,
                finished: false,
                text: 'Study'
            },
            {
                id: 8,
                finished: false,
                text: 'Run'
            },
            {
                id: 9,
                finished: false,
                text: 'Write a love letter'
            },
            {
                id: 10,
                finished: false,
                text: 'Tell my wife I love her'
            },
            {
                id: 11,
                finished: true,
                text: 'Show off'
            }
        ]
    }
];
