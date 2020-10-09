from flask import Blueprint, jsonify, request, abort
from jsonschema import validate
from ..db import messages
from ..db import users
from ..db import teams
from ..db import groups
from ..db import connect
from . import schema
import boto3
from flask_login import login_required
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


AWS = boto3.client(
    'sns',
    aws_access_key_id=environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key=environ.get('AWS_SECRET_ACCESS_KEY'),
    region_name='us-east-1'
)


def sendsms(phone_number, text):
    try:
        response = AWS.publish(
            PhoneNumber=phone_number,
            Message=text,
            MessageAttributes={
                'AWS.SNS.SMS.SenderID':
                {
                    'DataType': 'String',
                    'StringValue': 'GameTime'
                }
            }
        )
        return response, True
    except Exception as e:
        return str(e), False


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
@login_required
def send_message():
    if request.method == 'POST':
        body = request.get_json()

        try:
            validate(body, schema=schema.send_message_schema)
        except:
            return jsonify({'message': 'Bad Request'}), 400

        sender_id, recipient_id, contents = body['sender_id'], body['recipient_id'], body['message']

        # Store the message
        message, status, message_id = messages.create_message(
            connection, recipient_id, sender_id, contents)
        if status != 200:
            return message, status

        # Fetch the number
        message, status, phone_number = users.get_users_phone_number(
            connection, recipient_id)
        if status != 200:
            return message, status

        # Send to SNS
        res, success = sendsms(phone_number, contents)
        if not success:
            return jsonify({'message': 'Failed to send message'}), 400

        res = message_id
        return jsonify({'player_id': recipient_id, 'message': "Success"}), 200


@messagesbp.route('/sendGroupMessage', methods=['POST'])
# @login_required
def send_to_group():
    if request.method == 'POST':
        body = request.get_json()

        try:
            validate(body, schema=schema.send_to_group_schema)
        except:
            return jsonify({'message': 'Bad Request'}), 400

        sender_id, recipient_id, contents = body['sender_id'], body['group_id'], body['message']

        # Store the message
        message, status, message_id = messages.create_group_message(
            connection, recipient_id, sender_id, contents)
        if status != 200:
            return jsonify({'message': 'Failed to store message'}), status

        # Fetch the numbers
        message, status, phone_numbers = groups.get_groups_phone_numbers(
            connection, recipient_id)
        if status != 200:
            return jsonify({'message': 'Failed to fetch numbers'}), status

        for phone_number in phone_numbers:
            res, success = sendsms(phone_number, contents)
            if not success:
                return jsonify({'message': 'Failed to send text'}), 500

        return jsonify({'message': "Success"}), 200


@messagesbp.route('/sendTeamMessage', methods=['POST'])
@login_required
def send_to_team():
    if request.method == 'POST':
        body = request.get_json()

        try:
            validate(body, schema=schema.send_to_team_schema)
        except:
            return jsonify({'message': 'Bad Request'}), 400

        sender_id, recipient_id, contents = body['sender_id'], body['team_id'], body['message']

        # Store the message
        message, status, message_id = messages.create_group_message(
            connection, recipient_id, sender_id, contents)
        if status != 200:
            return jsonify({'message': 'Failed to store message'}), status

        # Fetch the numbers
        message, status, phone_numbers = teams.get_teams_phone_numbers(
            connection, recipient_id)
        if status != 200:
            return jsonify({'message': 'Failed to fetch numbers'}), status

        for phone_number in phone_numbers:
            res, success = sendsms(phone_number, contents)
            if not success:
                return jsonify({'message': 'Failed to send text'}), 500

        return jsonify({'message': "Success"}), 200
