from flask import Blueprint


examplebp = Blueprint('examplebp', __name__)


@examplebp.route('/ex')
def example():
    return 'Hello, World!'
