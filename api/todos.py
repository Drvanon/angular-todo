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


@bp.route('/list/<int:list_id>', methods=["GET"])
@require_authorization
def get_todolist(list_id):
    todolist = db.session.query(TodoList).get(list_id)

    if not todolist:
        return jsonify({"message": "todo list not found"})
    if not todolist.user == g.user:
        return jsonify({"message": "todo list not owned by user"})

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


@bp.route('/item/add/<int:list_id>', methods=["POST"])
@require_authorization
def test(list_id):
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


@bp.route('/item/finish/<int:item_id>', methods=["PUT"])
@require_authorization
@get_todo
def finish_item(todo):
    todo.finished = True

    db.session.add(todo)
    db.session.commit()

    return jsonify({"message": "success"})


@bp.route('/item/un-finish/<int:item_id>', methods=["PUT"])
@require_authorization
@get_todo
def unfinish_item(todo):
    todo.finished = False

    db.session.add(todo)
    db.session.commit()

    return jsonify({"message": "success"})


@bp.route('/item/update/<int:item_id>/<new_text>', methods=["PUT"])
@require_authorization
@get_todo
def update_item(todo, new_text):
    print("test")
