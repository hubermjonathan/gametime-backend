import os
from flask import Flask

from app.api.example import examplebp
from app.api.groups import groupsbp
from app.api.messages import messagesbp
from app.api.users import usersbp


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    # load the config
    if app.config['ENV'] == 'production':
        app.config.from_object('app.config.ProdConfig')
    else:
        app.config.from_object('app.config.DevConfig')

    # load blueprints
    app.register_blueprint(examplebp)
    app.register_blueprint(groupsbp)
    app.register_blueprint(messagesbp)
    app.register_blueprint(usersbp)

    return app
