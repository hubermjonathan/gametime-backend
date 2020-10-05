from flask import Blueprint, jsonify, request, abort
from ..db import messages as db

messagesbp = Blueprint('messagesbp', __name__)


@messagesbp.route('/sendPlayerMessage', methods=['POST'])
def send_message():
    if request.method == 'POST':
        body = request.get_json()
        userid, message_to_send = body['id'], body['message']

        # send_message()
        # if status != 200:
        #     return 'Failed to delete members from group, database error', status

        # return jsonify(data), 500


@messagesbp.route('/sendGroupMessage', methods=['POST'])
def send_to_group():
    if request.method == 'POST':
        body = request.get_json()
        groupid, message_to_send = body['id'], body['message']

        # send_message()
        # if status != 200:
        #     return 'Failed to delete members from group, database error', status

        # return jsonify(data), 500
