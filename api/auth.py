from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import IntegrityError

from api.database import get_db, User

bp = Blueprint('test', __name__)

@bp.route('/test')
def test():
    db = get_db()
    jeff = User('jeff', 'sessions')
    db.session.add(jeff)
    try:
        db.session.commit()
    except IntegrityError:
        return jsonify({'error': 'username not unique'})
    return ''


@bp.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    error = None

    if not username:
        error = 'Username is required.'
    elif not password:
        error = 'Password is required.'
    try:
        new_user = User(username, password)
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        error = 'Username is not unique'

    if not error:
        redirect('auth.login')
    else:
        jsonify({'error': error})
