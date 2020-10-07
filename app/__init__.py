import os
from flask import Flask

from app.api.example import examplebp
from app.api.groups import groupsbp
from app.api.messages import messagesbp


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    # load the config
    if app.config['ENV'] == 'production':
        app.config.from_object('app.config.ProdConfig')
    else:
        app.config.from_object('app.config.DevConfig')

    app.config['COGNITO_REGION'] = 'us-east-2'
    app.config['COGNITO_USERPOOL_ID'] = 'us-east-2_jaQKKpd5Q'
    app.config['COGNITO_APP_CLIENT_ID'] = '5hnntk0cimpssub89b2ge6n5s3'
    app.config['COGNITO_CHECK_TOKEN_EXPIRATION'] = False

    # initialize extension
    from flask_cognito import CognitoAuth
    cogauth = CognitoAuth(app)

    @cogauth.identity_handler
    def lookup_cognito_user(payload):
        """Look up user in our database from Cognito JWT payload."""
        return User.query.filter(User.cognito_username == payload['username']).one_or_none()

    # load blueprints
    app.register_blueprint(examplebp)
    app.register_blueprint(groupsbp)
    app.register_blueprint(messagesbp)

    return app
