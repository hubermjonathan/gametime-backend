from flask import Blueprint, jsonify, request
from jsonschema import validate
import re
from flask_login import login_required, current_user
import boto3
from os import environ
import base64
from ..db import sponsors as db
from . import schema
from .. import auth


s3 = boto3.client(
    's3',
    aws_access_key_id=environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key=environ.get('AWS_SECRET_ACCESS_KEY')
)

sponsorsbp = Blueprint('sponsorsbp', __name__)


@sponsorsbp.route('/sponsors', methods=['GET'])
def sponsors_get():
    if request.method == 'GET':
        team_id = request.args.get('team_id')

        message, error, data = db.get_sponsors_for_team(
            team_id)

        if error:
            return jsonify({'message': message}), 500

        return jsonify(data), 200
    else:
        return jsonify({'message': 'method not allowed'}), 405


@sponsorsbp.route('/sponsors', methods=['POST', 'DELETE'])
@login_required
def sponsors():
    if request.method == 'POST':
        try:
            body = request.get_json()
            validate(body, schema=schema.sponsors_post_schema)

            team_id = body['team_id']
            name = body['name']
            picture = body['picture']
        except Exception:
            return jsonify({'message': 'invalid body provided'}), 400

        if re.search(r'^data:image\/jpeg;base64,(?:[A-Za-z0-9+\/]{4})*(?:[A-Za-z0-9+\/]{2}==|[A-Za-z0-9+\/]{3}=)?$', picture) is None:
            return jsonify({'message': 'invalid picture provided'}), 400

        if not auth.isOwner(current_user.user_id, team_id):
            return jsonify({'message': 'invalid permissions'}), 400

        message, error, data = db.create_sponsor(
            team_id, name, picture)

        if error:
            return jsonify({'message': message}), 500

        return jsonify(data), 200
    elif request.method == 'DELETE':
        try:
            body = request.get_json()
            validate(body, schema=schema.sponsors_delete_schema)

            team_id = body['team_id']
            sponsor_id = body['sponsor_id']
        except Exception:
            return jsonify({'message': 'invalid body provided'}), 400

        if not auth.isOwner(current_user.user_id, team_id):
            return jsonify({'message': 'invalid permissions'}), 400

        s3.delete_object(
            Bucket='gametime-file-storage',
            Key=f'{sponsor_id}.jpeg'
        )

        message, error, data = db.remove_sponsor(sponsor_id)

        if error:
            return jsonify({'message': message}), 500

        return jsonify(data), 200
    else:
        return jsonify({'message': 'method not allowed'}), 405
