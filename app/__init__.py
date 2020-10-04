import os
from flask import Flask

from app.api.example import examplebp
from app.api.group import groupbp


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
    app.register_blueprint(groupbp)

    return app
