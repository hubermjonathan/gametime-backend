import os
from flask import Flask

from flask_login import LoginManager, current_user, login_required
from warrant import Cognito

from app.api.example import examplebp
from app.api.groups import groupsbp
from app.api.messages import messagesbp

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
            print(access_token)
            cognito = Cognito('us-east-2_jaQKKpd5Q', '5hnntk0cimpssub89b2ge6n5s3', access_token=access_token)
            
            username = cognito.get_user()._metadata.get("username")
            if username is None:
                return None

            return User(username)

        except Exception as e:
            return None

    # load blueprints
    app.register_blueprint(examplebp)
    app.register_blueprint(groupsbp)
    app.register_blueprint(messagesbp)

    return app
