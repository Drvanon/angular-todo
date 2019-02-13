from functools import wraps

from flask import (
    Blueprint, g, request, session, jsonify, abort
)
from werkzeug.security import check_password_hash
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import MultipleResultsFound

from api.database import User
from . import db

bp = Blueprint('auth', __name__)


@bp.route('/register', methods=['POST'])
def register():
    if not request.json:
        return jsonify({'message': 'no json data received'})

    username = request.json.get('username')
    password = request.json.get('password')
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


@bp.route('/username-available/<username>')
def username_available(username):
    if User.query.filter_by(username=username).one_or_none():
        return jsonify({'message': 'username taken'})
    return jsonify({'message': 'username available'})


@bp.route('/login', methods=['POST'])
def login():
    if not request.json:
        return jsonify({'message': 'no json data received'})

    username = request.json.get('username')
    password = request.json.get('password')

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
        g.user = db.session.query(User).get(user_id)


@bp.route('/logout', methods=["POST"])
def logout():
    session.clear()
    return jsonify({'message': 'success'})


def require_authorization(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if 'user' in g and g.user:
            return f(*args, **kwargs)
        abort(401)
    return decorator
