from flask import Blueprint, jsonify, request, abort
from jsonschema import validate
from ..db import messages as db
from ..db import connect
from . import schema

messagesbp = Blueprint('messagesbp', __name__)
connection = None


@messagesbp.before_request
def connect_db():
    global connection
    connection = connect()


@messagesbp.after_request
def disconnect_db(response):
    global connection
    if connection:
        connection.close()
        connection = None
    return response


@messagesbp.route('/sendPlayerMessage', methods=['POST'])
def send_message():
    if request.method == 'POST':
        body = request.get_json()

        try:
            validate(body, schema=schema.send_message_schema)
        except Exception as e:
            return jsonify(str(e)), 400

        sender_id, recipient_id, contents = body['sender_id'], body['recipient_id'], body['message']

        # Store the message
        message, status, message_id = db.create_message(
            connection, recipient_id, sender_id, contents)
        if status != 200:
            return message, status

        # TODO: Send the message via SNS

        res = message_id
        return jsonify(res), 200


@messagesbp.route('/sendGroupMessage', methods=['POST'])
def send_to_group():
    if request.method == 'POST':
        body = request.get_json()

        try:
            validate(body, schema=schema.send_to_group_schema)
        except Exception as e:
            return jsonify(str(e)), 400

        sender_id, recipient_id, contents = body['sender_id'], body['group_id'], body['message']

        # Store the message
        message, status, message_id = db.create_group_message(
            connection, recipient_id, sender_id, contents)
        if status != 200:
            return message, status

        # TODO: Send the message via SNS

        res = message_id
        return jsonify(res), 200
