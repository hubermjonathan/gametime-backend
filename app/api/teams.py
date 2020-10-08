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

    new_team_id = db.create_team(connection, name, owner)

    res = new_team_id
    return jsonify(res), 200

@teamsbp.route('/team/edit', methods=['POST'])
def editTeam():
    # POST, Creates a new team
    body = request.get_json()

    team, name = body['team'], body['name']

    return db.edit_team_name(connection, team, name)

    res = new_team_id
    return jsonify(res), 200

@teamsbp.route('/team/remove', methods=['POST'])
def removeFromTeam():
    # POST, Creates a new team
    body = request.get_json()

    team, player = body['team'], body['player']

    return db.edit_team_name(connection, team, player)

@teamsbp.route('/team/view', methods=['POST'])
def viewTeam():
    # POST, Creates a new team
    body = request.get_json()

    team = body['team']

    text, status, data = db.get_team(connection, team)
    text2, status2, data2 = db.get_teams_members(connection, team)

    print(data[0])
    print(data2[0])

    return ('successfully retrieved team data and members',200,[data[0], data2[0]])
