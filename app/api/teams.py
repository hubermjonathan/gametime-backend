from flask import Blueprint, jsonify, request, abort
from jsonschema import validate
from ..db import teams as db
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
    print("Test\n\n\n", request)
    # POST, Creates a new team
    body = request.get_json()

    name, owner = body['name'], body['owner']

    ret = db.create_team(connection, name, owner)

    return jsonify(ret[2]), ret[1]

@teamsbp.route('/team/edit', methods=['POST'])
def editTeam():
    # POST, Creates a new team
    body = request.get_json()

    team, name = body['team'], body['name']

    ret = db.edit_team_name(connection, team, name)
    return jsonify(""), ret[1]

@teamsbp.route('/team/remove', methods=['POST'])
def removeFromTeam():
    # POST, Creates a new team
    body = request.get_json()

    team, player = body['team'], body['player']

    ret = db.remove_from_team(connection, player, team)
    return "", ret[1]

@teamsbp.route('/team/view/data', methods=['POST'])
def viewTeam():
    # POST, Creates a new team
    body = request.get_json()

    team = body['team']

    ret = db.get_team(connection, team)
    return jsonify(ret[2]), ret[1]

@teamsbp.route('/team/view/members', methods=['POST'])
def viewMembers():
    # POST, Creates a new team
    body = request.get_json()

    team = body['team']

    ret = db.get_teams_members(connection, team)
    return jsonify(ret[2]), ret[1]

@teamsbp.route('/team/join/<id>', methods=['POST'])
def joinTeam(id):
    # POST, Creates a new team
    body = request.get_json()

    user = body['user']

    ret = db.add_to_team(connection, user, id)
    return jsonify(ret[2]), ret[1]
