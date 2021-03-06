import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='12398fjnkcm,zxcjnd123n',
        SQLALCHEMY_DATABASE_URI='sqlite:///{}'.format(
            os.path.join(app.instance_path, 'api.sqlite')),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    '''
    NOTE: supports_credentials creates a CSRF security risk. This is only
    for development purposes. Simply setting the domain would greatly
    decrease the risk, but the best solution would be to host on the same site.
    '''
    CORS(app, supports_credentials=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    from . import database
    database.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import todos
    app.register_blueprint(todos.bp)

    return app
