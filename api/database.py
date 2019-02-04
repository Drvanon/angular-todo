import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
from werkzeug.security import check_password_hash, generate_password_hash

from . import db

def get_db():
    with current_app.app_context():
        if 'db' not in g:
            g.db = db

        return g.db

def init_db():
    db = get_db()
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
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

