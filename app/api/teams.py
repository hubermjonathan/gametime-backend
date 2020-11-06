from flask import Blueprint, jsonify, request, abort
from jsonschema import validate
from flask_login import login_required, current_user
from ..db import teams as db
from . import schema
from .. import auth

import json

teamsbp = Blueprint('teamsbp', __name__)


@teamsbp.route('/team/create', methods=['POST'])
@login_required
def createTeam():
    # POST, Creates a new team
    body = request.get_json()

    name, owner = body['name'], body['owner']

    message, error, data = db.create_team(name, owner)

    if error:
        return "", 500

    return jsonify(data), 200


@teamsbp.route('/team/edit', methods=['POST'])
@login_required
def editTeam():
    # POST, Edits team attributes
    body = request.get_json()

    team, name = body['team'], body['name']

    message, error, data = db.edit_teams_name(team, name)

    if error:
        return "", 500

    return jsonify(""), 200


@teamsbp.route('/team/remove', methods=['POST'])
@login_required
def removeFromTeam():
    # POST, Removes player from team
    body = request.get_json()

    team, user = body['team'], body['user']

    message, error, data = db.remove_user_from_team(user, team)

    if error:
        return "", 500

    return "", 200


@teamsbp.route('/team/view/data', methods=['POST'])
def viewTeam():
    # POST, gets Attributes of Team (TODO make GET)
    body = request.get_json()

    team = body['team']

    message, error, data = db.get_team(team)

    if error:
        return "", 500

    return jsonify(data), 200


@teamsbp.route('/team/view/all', methods=['GET'])
def viewAllTeams():
    message, error, data = db.get_all_teams()

    if error:
        return "", 500

    return jsonify(data), 200


@teamsbp.route('/team/permissions', methods=['POST'])
@login_required
def editPermissions():
    # POST, edits permissions of player
    body = request.get_json()

    user = body['user']
    team = body['team']
    priv = body['priv']

    message, error, data = db.edit_users_permission_level_for_team(
        user, team, priv)

    if error:
        return "", 500

    return jsonify(data), 200


@teamsbp.route('/team/join/<id>', methods=['GET'])
@login_required
def joinTeam(id):
    # GET, player joins team
    user = current_user.user_id

    message, error, data = db.add_user_to_team(user, id)

    if error:
        return "", 500

    return jsonify(data), 200


@teamsbp.route('/team/view/groups', methods=['GET'])
@login_required
def get_teams_groups():
    # GET, Gets groups from a team
    if request.method == 'GET':
        team_id = request.args.get('id')

        message, error, groups = db.get_teams_groups(team_id)
        if error:
            return message, 500

        return jsonify(groups), 200
