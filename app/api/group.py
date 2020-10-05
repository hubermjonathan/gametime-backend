from flask import Blueprint, jsonify, request, abort
from .. import db

groupbp = Blueprint('groupbp', __name__)


@groupbp.route('/group', methods=['GET', 'POST'])
def create_group():
    if request.method == 'GET':
        groupid = request.args.get('id')
        message, status, data = db.get_group(groupid)
        if status != 200:
            return 'Failed to fetch members to group, database error', status

        return jsonify(data), 200

    if request.method == 'POST':
        body = request.get_json()
        name, email, phone_number = body['name'], body['email'], body['phone_number']

        message, status, data = db.create_group(name, email, phone_number)
        if status != 200:
            return 'Failed to delete members from group, database error', status

        return jsonify(data), 500


@groupbp.route('/group/addMembers', methods=['PUT'])
def add_members():
    if request.method == 'PUT':
        body = request.get_json()
        groupid, members = body['id'], body['new_members']

        message, status, data = db.add_group_members(groupid, members)
        if status != 200:
            return 'Failed to add members to group, database error', status

        return jsonify(data), status


@groupbp.route('/group/deleteMembers', methods=['DELETE'])
def delete_members():
    if request.method == 'DELETE':
        body = request.get_json()
        groupid, members = body['id'], body['remove_members']

        message, status, data = db.delete_group_members(groupid, members)
        if status != 200:
            return 'Failed to delete members from group, database error', status

        return jsonify(data), status
