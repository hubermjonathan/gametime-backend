from flask import Blueprint, jsonify, request, abort
from .. import db

groupbp = Blueprint('groupbp', __name__)


@groupbp.route('/group', methods=['GET', 'POST'])
def create_group():
    if request.method == 'GET':
        groupid = request.args.get('id')
        try:
            # db.get_group(groupid)
            res = {"TODO"}
        except:
            return 'Failed to fetch group, database error', 500
        return jsonify(res), 200

    if request.method == 'POST':
        body = request.get_json()
        name, email, phone_number = body['name'], body['email'], body['phone_number']
        try:
            # res = db.create_group(name, email, phone_number)
            res = "TODO"
        except:
            return 'Failed to create group, database error', 500

        return jsonify(res), 200
