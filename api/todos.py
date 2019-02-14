from functools import wraps
from flask import (
        Blueprint, g, request, jsonify
        )

from api.database import Todo, TodoList
from api.auth import require_authorization
from api import db

bp = Blueprint('todos', __name__, url_prefix="/todos/")


def get_todo(f):
    @wraps(f)
    def todo_decorator(*args, **kwargs):
        todo = db.session.query(Todo).get(kwargs.get('item_id'))
        kwargs.pop('item_id')

        if not todo:
            def error_notFound(*args, **kwargs):
                return jsonify({"message": "todo item not found"})
            return error_notFound
        if not todo.todolist.user == g.user:
            def error_notOwned(*args, **kwargs):
                return jsonify({"message": "todo list not owned by user"})
            return error_notOwned

        return f(todo, *args, **kwargs)
    return todo_decorator


@bp.route('/lists', methods=["GET"])
@require_authorization
def get_todolists():
    ''' GET all todolists for this user.'''
    return jsonify({
        "message": "success",
        "todolists":
            [
                {
                    "title": todolist.title,
                    "id": todolist.id
                } for todolist in g.user.todolists
            ]
        }
    )


@bp.route('/list/', methods=["PUT"])
@require_authorization
def create_list():
    '''
    PUT this users' new todolist in the database.

    json-data: {"title":"<your title>"}
    '''
    if not request.json:
        return jsonify({"message": "no json data supplied"})
    if 'title' not in request.json:
        return jsonify({"message": "no title supplied"})

    print('title: "{}"'.format(request.json.get('title')))

    todolist = TodoList(g.user, request.json.get('title'))
    db.session.add(todolist)
    db.session.commit()

    return jsonify({"message": "success", "id": todolist.id})


@bp.route('/list/<int:list_id>', methods=["GET", "DELETE"])
@require_authorization
def get_todolist(list_id):
    ''' GET a todolist and all it's todo items or DELETE it '''
    todolist = db.session.query(TodoList).get(list_id)

    if not todolist:
        return jsonify({"message": "todo list not found"})
    if not todolist.user == g.user:
        return jsonify({"message": "todo list not owned by user"})

    if request.method == 'GET':
        return jsonify(
            {
                "message": "success",
                "todolist": {
                    "id": todolist.id,
                    "title": todolist.title,
                    "todos": [
                        {
                            "id": todo.id,
                            "text": todo.text,
                            "finished": todo.finished
                        } for todo in todolist.todos
                    ]
                }
            }
        )

    if request.method == 'DELETE':
        db.session.delete(todolist)
        db.session.commit()


@bp.route('/item/<int:list_id>', methods=["PUT"])
@require_authorization
def create_todo(list_id):
    ''' PUT a new todo to a list with list_id '''
    todolist = db.session.query(TodoList).get(list_id)

    if not todolist:
        return jsonify({"message": "todo list not found"})
    if not todolist.user == g.user:
        return jsonify({"message": "todo list not owned by user"})

    text = request.json.get('text')
    todo = Todo(todolist, text)
    db.session.add(todo)
    db.session.commit()

    return jsonify({"message": "success"})


@bp.route('/item/<int:item_id>', methods=["PUT", "DELETE"])
@require_authorization
@get_todo
def update_item(todo):
    ''' PUT an update the todo item with id <item_id> or DELETE it '''
    if request.method == 'PUT':
        if not request.json:
            return jsonify({"message": "no json data supplied"})
        if 'text' not in request.json:
            return jsonify({"message": "no text supplied"})

        todo.text = request.json.get('text')
        db.session.add(todo)
        db.commit()

        return jsonify({"message": "success"})
    if request.method == 'DELETE':
        db.session.delete(todo)
        db.session.commit()

        return jsonify({"message": "success"})


@bp.route('/item/finish/<int:item_id>', methods=["PUT"])
@require_authorization
@get_todo
def finish_item(todo):
    ''' PUT the item with id 'item_id' as finished '''
    todo.finished = True

    db.session.add(todo)
    db.session.commit()

    return jsonify({"message": "success"})


@bp.route('/item/un-finish/<int:item_id>', methods=["PUT"])
@require_authorization
@get_todo
def unfinish_item(todo):
    ''' PUT the item with id 'item_id' as not finished '''
    todo.finished = False
    todo.finished = True

    db.session.add(todo)
    db.session.commit()

    return jsonify({"message": "success"})
