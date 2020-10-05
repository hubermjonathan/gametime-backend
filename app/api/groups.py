from flask import Blueprint, jsonify, request, abort
from ..db import groups as db
from ..db import connect

groupsbp = Blueprint('groupsbp', __name__)
connection = None


@groupsbp.before_request
def connect_db():
    global connection
    connection = connect()


@groupsbp.after_request
def disconnect_db(response):
    global connection
    if connection:
        connection.close()
        connection = None
    return response


@groupsbp.route('/group', methods=['GET', 'POST'])
def create_fetch_group():
    # GET, Returns information about a group
    if request.method == 'GET':
        group_id = request.args.get('id')

        message, status, data = db.get_groups_members(connection, group_id)

        if status != 200:
            return 'Failed to fetch members of group, database error', status
        return jsonify(data), 200

    # POST, Creates a new group
    if request.method == 'POST':
        body = request.get_json()
        name, team_id, member_ids = body['name'], body['team_id'], body['member_ids']

        message, status, new_group_id = db.create_group(
            connection, name, team_id)

        for member_id in member_ids:
            message, status, data, = db.add_to_group(
                connection, member_id, new_group_id)

        if status != 200:
            return 'Failed to create new group, database error', status
        return jsonify(new_group_id), 200


@groupsbp.route('/group/addMembers', methods=['PUT'])
def add_members():
    if request.method == 'PUT':
        body = request.get_json()
        group_id, member_ids = body['group_id'], body['new_members']

        for member_id in member_ids:
            message, status, data, = db.add_to_group(
                connection, member_id, group_id)

        if status != 200:
            return 'Failed to add members to group, database error', status
        return jsonify(data), status


@groupsbp.route('/group/deleteMembers', methods=['DELETE'])
def delete_members():
    if request.method == 'DELETE':
        body = request.get_json()
        group_id, member_ids = body['group_id'], body['remove_members']

        for member_id in member_ids:
            message, status, data = db.remove_from_group(
                connection, member_id, group_id)

        if status != 200:
            return 'Failed to delete members from group, database error', status

        return jsonify(data), status
