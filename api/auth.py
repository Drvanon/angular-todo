from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import MultipleResultsFound

from api.database import get_db, User

bp = Blueprint('auth', __name__)

@bp.route('/test')
def test():
    db = get_db()
    jeff = User('jeff', 'sessions')
    db.session.add(jeff)
    try:
        db.session.commit()
    except IntegrityError:
        return jsonify({'message': 'username not unique'})
    return ''


@bp.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
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
        return jsonify({'message': 'success'})
    else:
        return jsonify({'message': error})

@bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    db = get_db()

    if not password:
        return jsonify({'message': 'A password is required'})
    if not username:
        return jsonify({'message': 'A username is required'})

    try:
        user = User.query.filter_by(username=username).one_or_none()
    except MultipleResultsFound:
        return jsonify({'message': 'Multiple users for that username found'})

    if not user:
        return jsonify({'message': 'Username not found'})

    if check_password_hash(user.password, password):
        session.clear()
        session['user_id'] = user.id
        return jsonify({'message': 'success'})

    return jsonify({'message': 'Wrong password'})

@bp.route('/is-logged-in/<username>')
def isLoggedIn(username):
    print(g.user)
    print(session.get('user_id'))
    if g.user:
        if username == g.user.username:
            return jsonify({'message': 'user is logged in'})
    return jsonify({'message': 'user is not logged'})

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).one_or_none()

@bp.route('/logout', methods=["POST"])
def logout():
    session.clear()
    return jsonify({'message':'success'})

