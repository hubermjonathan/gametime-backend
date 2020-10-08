from flask import Blueprint, jsonify, request, abort
from jsonschema import validate
from ..db import users as db
from ..db import connect
from . import schema

teamsbp = Blueprint('teamsbp', __name__)
connection = None


@teamsbp.before_request
def connect_db():
    global connection
    connection = connect()


@teamsbp.after_request
def disconnect_db(response):
    global connection
    if connection:
        connection.close()
        connection = None
    return response


@teamsbp.route('/team/create', methods=['POST'])
def createTeam():
    # POST, Creates a new team
    body = request.get_json()

    name, owner = body['name'], body['owner']

    new_team_id = db.create_user(connection, name, owner)

    res = new_team_id
    return jsonify(res), 200