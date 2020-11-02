from app.api.users import usersbp
from app.api.messages import messagesbp
from app.api.teams import teamsbp
from app.api.groups import groupsbp
from app.api.fundraising import fundraisingbp
from app.api.test import testbp
import os
import sys
from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager, current_user, login_required
from warrant import Cognito
import time
import app.auth as auth
from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class User:

    def __init__(self, username):
        self.user_id = username
        self.is_authenticated = True
        self.is_active = True


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    # Load in Cognito keys
    auth.decodeJWK()

    @login_manager.request_loader
    def load_user_from_request_header(request):
        try:
            access_token_enc = request.headers["Authorization"]
            access_token_dec = auth.decodeJWT(access_token_enc)

            if(access_token_dec['exp'] < time.time()):
                return None

            # id_token_enc = request.headers["ID"]
            # kid = jwt.get_unverified_header(id_token_enc)['kid']
            # key = public_keys[kid]
            # access_token_dec = jwt.decode(id_token_enc, public_keys[kid], algorithms='RS256')

            access_token = request.headers["Authorization"]
            cognito = Cognito(
                environ.get('COGNITO_REGION'), environ.get('COGNITO_ACCESS'), access_token=access_token, user_pool_region='us-east-2')

            username = cognito.get_user()._metadata.get("username")
            if username is None:
                return None

            return User(username)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(e)
            return None

    # load blueprints
    app.register_blueprint(testbp)
    app.register_blueprint(groupsbp)
    app.register_blueprint(teamsbp)
    app.register_blueprint(messagesbp)
    app.register_blueprint(usersbp)
    app.register_blueprint(fundraisingbp)

    return app
