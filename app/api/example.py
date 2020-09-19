from flask import Blueprint


example = Blueprint('example', __name__)

# an example route
@example.route('/ex')
def example():
    return 'Hello, World!'
