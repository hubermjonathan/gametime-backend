from flask import Blueprint, jsonify, request, abort
from .. import db

messagebp = Blueprint('messagebp', __name__)


@messagebp.route('/sendPlayerMessage', methods=['POST'])
def send_message():
    if request.method == 'POST':
        body = request.get_json()
        userid, message_to_send = body['id'], body['message']

        # send_message()
        # if status != 200:
        #     return 'Failed to delete members from group, database error', status

        # return jsonify(data), 500


@messagebp.route('/sendGroupMessage', methods=['POST'])
def send_to_group():
    if request.method == 'POST':
        body = request.get_json()
        groupid, message_to_send = body['id'], body['message']

        # send_message()
        # if status != 200:
        #     return 'Failed to delete members from group, database error', status

        # return jsonify(data), 500
