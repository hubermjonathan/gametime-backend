from flask import Blueprint, jsonify, request, abort
from jsonschema import validate
from flask_login import login_required
from ..db import teams as db
from ..db import connect
from . import schema

import json

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

    ret = db.create_team(connection, name, owner)

    res = {
        'team_id': ret[2]
    }

    return jsonify(res), ret[1]

@teamsbp.route('/team/edit', methods=['POST'])
def editTeam():
    # POST, Edits team attributes
    body = request.get_json()

    team, name = body['team'], body['name']

    ret = db.edit_team_name(connection, team, name)
    return jsonify(""), ret[1]

@teamsbp.route('/team/remove', methods=['POST'])
def removeFromTeam():
    # POST, Removes player from team
    body = request.get_json()

    team, player = body['team'], body['player']

    ret = db.remove_from_team(connection, player, team)
    return "", ret[1]

@teamsbp.route('/team/view/data', methods=['POST'])
def viewTeam():
    # POST, gets Attributes of Team (TODO make GET)
    body = request.get_json()

    team = body['team']

    ret = db.get_team(connection, team)
    team = ret[2][0]

    res = {
        'team_id': team[0],
        'name': team[1],
        'fund_goal': team[2],
        'fund_current': team[3],
        'fund_desc': team[4],
        'account_number': team[5],
        'routing_number': team[6],
        'owner': team[7]
    }

    return jsonify(res), ret[1]

@teamsbp.route('/team/view/members', methods=['POST'])
def viewMembers():
    # POST, gets Team Members (TODO make GET)
    body = request.get_json()

    team = body['team']
    
    ret = db.get_teams_members(connection, team)

    users = ret[2]

    usersRet = []
    for user in users:
        userRet = {
            'user_id': user[0],
            'name': user[1],
            'email': user[2],
            'phone_number': user[3],
            'profile_picture': user[4]
        }

        usersRet.append(userRet)

    return jsonify(usersRet), ret[1]

@teamsbp.route('/team/permissions', methods=['POST'])
def editPermissions():
    # POST, edits permissions of player
    body = request.get_json()

    user = body['user']
    team = body['team']
    priv = body['priv']

    ret = db.change_permission_level(connection, user, team, priv)
    return jsonify(ret[2]), ret[1]

@teamsbp.route('/team/join/<id>', methods=['POST'])
def joinTeam(id):
    # POST, player joins team
    body = request.get_json()

    user = body['user']

    ret = db.add_to_team(connection, user, id)
    return jsonify(ret[2]), ret[1]


@login_required
@teamsbp.route('/team/view/groups', methods=['GET'])
def get_teams_groups():
    # GET, Gets groups from a team
    if request.method == 'GET':
        team_id = request.args.get('id')

        message, status, groups = db.get_teams_groups(connection, team_id)
        if status != 200:
            return message, status

        res = {
            'groups': groups
        }
        return jsonify(res), 200
