from app.api.users import usersbp
from app.api.messages import messagesbp
from app.api.groups import groupsbp
from app.api.example import examplebp
import os
from flask import Flask

from flask_login import LoginManager, current_user, login_required
from warrant import Cognito

from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

from app.api.example import examplebp
from app.api.groups import groupsbp
from app.api.teams import teamsbp
from app.api.messages import messagesbp
from app.api.users import usersbp

class User:

    def __init__(self, username):
        self.user = username
        self.is_authenticated = True
        self.is_active = True


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    # load the config
    if app.config['ENV'] == 'production':
        app.config.from_object('app.config.ProdConfig')
    else:
        app.config.from_object('app.config.DevConfig')

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.request_loader
    def load_user_from_request_header(request):
        try:
            access_token = request.headers["Authorization"]
            # print(access_token)
            cognito = Cognito(
                environ.get('COGNITO_REGION'), environ.get('COGNITO_ACCESS'), access_token=access_token, user_pool_region='us-east-2')

            username = cognito.get_user()._metadata.get("username")
            if username is None:
                return None

            return User(username)

        except Exception as e:
            return None

    # load blueprints
    app.register_blueprint(examplebp)
    app.register_blueprint(groupsbp)
    app.register_blueprint(teamsbp)
    app.register_blueprint(messagesbp)
    app.register_blueprint(usersbp)

    return app
