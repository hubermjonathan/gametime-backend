from flask import Blueprint, jsonify, request, abort
from jsonschema import validate
from ..db import groups as db
from . import schema
from flask_login import login_required

groupsbp = Blueprint('groupsbp', __name__)


@groupsbp.route('/group', methods=['GET', 'POST'])
@login_required
def create_fetch_group():
    # GET, Returns information about a group
    if request.method == 'GET':
        group_id = request.args.get('id')

        message, error, group_info = db.get_group(
            group_id)
        if error:
            return jsonify({'message': 'Failed to fetch group members'}), 400

        return jsonify(group_info), 200

    # POST, Creates a new group
    if request.method == 'POST':
        body = request.get_json()

        try:
            validate(body, schema=schema.fetch_group_schema)
        except Exception as e:
            return jsonify(str(e)), 400

        name, team_id, member_ids = body['name'], body['team_id'], body['member_ids']

        if not name:
            return jsonify({'message': 'Failed to create group'}), 400

        message, error, new_group_id = db.create_group(
            name, team_id)
        if error:
            return jsonify({'message': 'Failed to create group'}), 400

        for member_id in member_ids:
            message, error, data, = db.add_user_to_group(
                member_id, new_group_id['group_id'])
            if error:
                return jsonify({'message': 'Failed to create group'}), 400

        return jsonify({'message': 'Success'}), 200


@groupsbp.route('/group/addMembers', methods=['PUT'])
@login_required
def add_members():
    if request.method == 'PUT':
        body = request.get_json()

        try:
            validate(body, schema=schema.add_members_schema)
        except:
            return jsonify({'message': 'Failed to add member'}), 400

        group_id, member_ids = body['group_id'], body['new_members']

        for member_id in member_ids:
            message, error, data, = db.add_user_to_group(
                member_id, group_id)
            if error:
                return jsonify({'message': 'Failed to add member'}), 400

        return jsonify({'message': 'Success'}), 200


@groupsbp.route('/group/deleteMembers', methods=['DELETE'])
@login_required
def delete_members():
    if request.method == 'DELETE':
        body = request.get_json()

        try:
            validate(body, schema=schema.delete_members_schema)
        except:
            return jsonify({'message': 'Failed to delete members'}), 400

        group_id, member_ids = body['group_id'], body['remove_members']

        if group_id < 0:
            return jsonify({'message': 'Failed to delete members'}), 400

        for member_id in member_ids:
            if not isinstance(member_id, int) or member_id < 0:
                return jsonify({'message': 'Failed to delete members'}), 400

        for member_id in member_ids:
            message, error, data = db.remove_user_from_group(
                member_id, group_id)
            if error:
                return jsonify({'message': 'Failed to delete member'}), 400

        return jsonify({'message': 'Success'}), 200
