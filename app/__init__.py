import os
from flask import Flask

import app.api as api


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    # load the config
    if app.config['ENV'] == 'production':
        app.config.from_object('config.ProdConfig')
    else:
        app.config.from_object('config.DevConfig')

    # load blueprints
    app.register_blueprint(api)

    return app
