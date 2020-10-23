from flask import Blueprint, jsonify, request, abort
from jsonschema import validate
from ..db import messages
from ..db import users
from ..db import teams
from ..db import groups
from . import schema
import boto3
from flask_login import login_required
from os import environ


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
        message, error, message_id = messages.create_direct_message(
            recipient_id, sender_id, contents)
        if error:
            return jsonify({'message': 'Failed to send message'}), 400

        # Fetch the number
        message, error, user = users.get_user(
            recipient_id)
        if error:
            return message, 500

        # Send to SNS
        res, success = sendsms(user['phone_number'], contents)
        if not success:
            print(res)
            return jsonify({'message': 'Failed to send message'}), 503

        res = message_id
        return jsonify({'player_id': recipient_id, 'message': "Success"}), 200


@messagesbp.route('/sendGroupMessage', methods=['POST'])
@login_required
def send_to_group():
    if request.method == 'POST':
        body = request.get_json()

        try:
            validate(body, schema=schema.send_to_group_schema)
        except:
            return jsonify({'message': 'Bad Request'}), 400

        sender_id, recipient_id, contents = body['sender_id'], body['group_id'], body['message']

        # Store the message
        message, error, message_id = messages.create_group_message(
            recipient_id, sender_id, contents)
        if error:
            return jsonify({'message': 'Failed to send message'}), 400

        # Fetch the numbers
        message, error, phone_numbers = groups.get_groups_phone_numbers(
            recipient_id)
        if error:
            return jsonify({'message': 'Failed to send message'}), 400

        failed = False
        number_failed = 0
        for phone_number in phone_numbers['phone_numbers']:
            res, success = sendsms(phone_number, contents)
            if not success:
                failed = True
                number_failed += 1

        if (failed):
            return jsonify({'message': f'Failed to send {number_failed} text(s)'}), 503

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
        message, error, message_id = messages.create_group_message(
            recipient_id, sender_id, contents)
        if error:
            return jsonify({'message': 'Failed to send message'}), 400

        # Fetch the numbers
        message, error, phone_numbers = teams.get_teams_phone_numbers(
            recipient_id)
        if error:
            return jsonify({'message': 'Failed to send message'}), 400

        failed = False
        number_failed = 0
        for phone_number in phone_numbers['phone_numbers']:
            res, success = sendsms(phone_number, contents)
            if not success:
                failed = True
                number_failed += 1

        if (failed):
            return jsonify({'message': f'Failed to send {number_failed} text(s)'}), 503

        return jsonify({'message': "Success"}), 200
