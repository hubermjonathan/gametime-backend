from flask import Blueprint, jsonify, request, abort
from jsonschema import validate
from ..db import groups as db
from ..db import connect
from . import schema

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
        # TODO: param validation
        group_id = request.args.get('id')

        message, status, group_info = db.get_groups_members(
            connection, group_id)

        if status != 200:
            return message, status

        res = group_info
        return jsonify(res), 200

    # POST, Creates a new group
    if request.method == 'POST':
        body = request.get_json()

        try:
            validate(body, schema=schema.fetch_group_schema)
        except Exception as e:
            return jsonify(str(e)), 400

        name, team_id, member_ids = body['name'], body['team_id'], body['member_ids']

        message, status, new_group_id = db.create_group(
            connection, name, team_id)

        for member_id in member_ids:
            message, status, data, = db.add_to_group(
                connection, member_id, new_group_id)

        if status != 200:
            return message, status

        res = new_group_id
        return jsonify(res), 200


@groupsbp.route('/group/addMembers', methods=['PUT'])
def add_members():
    if request.method == 'PUT':
        body = request.get_json()

        try:
            validate(body, schema=schema.add_members_schema)
        except Exception as e:
            return jsonify(str(e)), 400

        group_id, member_ids = body['group_id'], body['new_members']

        for member_id in member_ids:
            message, status, data, = db.add_to_group(
                connection, member_id, group_id)

        if status != 200:
            return message, status

        res = f"Successfully added Members: {member_ids} to Group: {group_id}"
        return jsonify(res), status


@groupsbp.route('/group/deleteMembers', methods=['DELETE'])
def delete_members():
    if request.method == 'DELETE':
        body = request.get_json()

        try:
            validate(body, schema=schema.delete_members_schema)
        except Exception as e:
            return jsonify(str(e)), 400

        group_id, member_ids = body['group_id'], body['remove_members']

        for member_id in member_ids:
            message, status, data = db.remove_from_group(
                connection, member_id, group_id)

        if status != 200:
            return message, status

        res = f"Successfully deleted Members: {member_ids} from Group: {group_id}"
        return jsonify(res), status
