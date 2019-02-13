import click
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash

from api import db


def init_db():
    db.create_all()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the sqlalchemy database.')


def init_app(app):
    app.cli.add_command(init_db_command)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    todolists = db.relation("TodoList", back_populates="user")

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)


class TodoList(db.Model):
    __tablename__ = 'todolist'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    todos = db.relationship("Todo", back_populates="todolist")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship("User", back_populates="todolists")

    def __init__(self, user, title):
        self.user = user
        self.title = title


class Todo(db.Model):
    __tablename__ = 'todo'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50))
    finished = db.Column(db.Boolean, nullable=False)
    todolist_id = db.Column(
        db.Integer,
        db.ForeignKey('todolist.id'),
        nullable=False
    )
    todolist = db.relationship("TodoList", back_populates="todos")

    def __init__(self, todolist, text=None):
        if text:
            self.text = text
        self.todolist = todolist
        self.finished = False
