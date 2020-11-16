from flask import Blueprint, jsonify, request
from jsonschema import validate
import requests
import json
import re
from flask_login import login_required, current_user
import boto3
from os import environ
import base64
from ..db import files as db
from . import schema


s3 = boto3.client(
    's3',
    aws_access_key_id=environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key=environ.get('AWS_SECRET_ACCESS_KEY')
)

filesbp = Blueprint('filesbp', __name__)


@filesbp.route('/files', methods=['GET', 'POST', 'DELETE'])
@login_required
def files():
    if request.method == 'GET':
        try:
            body = request.get_json()
            validate(body, schema=schema.files_get_schema)

            team_id = body['team_id']
        except Exception:
            return jsonify({'message': 'invalid body provided'}), 400

        message, error, data = db.get_files_for_user(
            team_id, current_user.user_id)

        if error:
            return jsonify({'message': message}), 500

        return jsonify(data), 200
    elif request.method == 'POST':
        try:
            body = request.get_json()
            validate(body, schema=schema.files_post_schema)

            team_id = body['team_id']
            file = body['file']
        except Exception:
            return jsonify({'message': 'invalid body provided'}), 400

        if re.search(r'^data:application\/pdf;base64,(?:[A-Za-z0-9+\/]{4})*(?:[A-Za-z0-9+\/]{2}==|[A-Za-z0-9+\/]{3}=)?$', file) is None:
            return jsonify({'message': 'invalid file provided'}), 400

        message, error, data = db.create_file(
            team_id, current_user.user_id, file)

        if error:
            return jsonify({'message': message}), 500

        return jsonify(data), 200
    elif request.method == 'DELETE':
        try:
            body = request.get_json()
            validate(body, schema=schema.files_delete_schema)

            file_id = body['file_id']
        except Exception:
            return jsonify({'message': 'invalid body provided'}), 400

        s3.delete_object(
            Bucket='gametime-file-storage',
            Key=f'{file_id}.pdf'
        )

        message, error, data = db.remove_file(file_id)

        if error:
            return jsonify({'message': message}), 500

        return jsonify(data), 200
    else:
        return jsonify({'message': 'method not allowed'}), 405
