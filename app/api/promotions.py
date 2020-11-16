from flask import Blueprint, jsonify, request
from jsonschema import validate
import re
from flask_login import login_required, current_user
import boto3
from os import environ
import base64
from ..db import promotions as db
from . import schema
from .. import auth


s3 = boto3.client(
    's3',
    aws_access_key_id=environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key=environ.get('AWS_SECRET_ACCESS_KEY')
)

promotionsbp = Blueprint('promotionsbp', __name__)


@promotionsbp.route('/promotions', methods=['GET'])
def promotions_get():
    if request.method == 'GET':
        team_id = request.args.get('team_id')

        message, error, data = db.get_promotions_for_team(team_id)

        if error:
            return jsonify({'message': message}), 500

        return jsonify(data), 200
    else:
        return jsonify({'message': 'method not allowed'}), 405


@promotionsbp.route('/promotions', methods=['POST', 'DELETE'])
@login_required
def promotions():
    if request.method == 'POST':
        try:
            body = request.get_json()
            validate(body, schema=schema.promotions_post_schema)

            team_id = body['team_id']
            name = body['name']
            description = body['description']
            picture = body['picture']
            start_time = body['start_time']
            end_time = body['end_time']
        except Exception:
            return jsonify({'message': 'invalid body provided'}), 400

        if re.search(r'^data:image\/jpeg;base64,(?:[A-Za-z0-9+\/]{4})*(?:[A-Za-z0-9+\/]{2}==|[A-Za-z0-9+\/]{3}=)?$', picture) is None:
            return jsonify({'message': 'invalid picture provided'}), 400

        try:
            float(start_time)
            float(end_time)
        except Exception:
            return jsonify({'message': 'invalid time provided'}), 400

        if not auth.isOwner(current_user.user_id, team_id):
            return jsonify({'message': 'invalid permissions'}), 400

        message, error, data = db.create_promotion(
            team_id, name, description, picture, start_time, end_time)

        if error:
            return jsonify({'message': message}), 500

        return jsonify(data), 200
    elif request.method == 'DELETE':
        try:
            body = request.get_json()
            validate(body, schema=schema.promotions_delete_schema)

            team_id = body['team_id']
            promotion_id = body['promotion_id']
        except Exception:
            return jsonify({'message': 'invalid body provided'}), 400

        if not auth.isOwner(current_user.user_id, team_id):
            return jsonify({'message': 'invalid permissions'}), 400

        s3.delete_object(
            Bucket='gametime-file-storage',
            Key=f'{promotion_id}.jpeg'
        )

        message, error, data = db.remove_promotion(promotion_id)

        if error:
            return jsonify({'message': message}), 500

        return jsonify(data), 200
    else:
        return jsonify({'message': 'method not allowed'}), 405
