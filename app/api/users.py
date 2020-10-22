from flask import Blueprint, jsonify, request
from jsonschema import validate
import requests
import json
import re
from flask_login import login_required, current_user
import boto3
from os import environ, path
from dotenv import load_dotenv
import base64
from ..db import users as db
from . import schema


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '../.env'))

AWS = boto3.resource(
    's3',
    aws_access_key_id=environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key=environ.get('AWS_SECRET_ACCESS_KEY')
)

usersbp = Blueprint('usersbp', __name__)


@usersbp.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        try:
            body = request.get_json()
            validate(body, schema=schema.signup_schema)

            phone_number, email, password, first_name, last_name = body['phone'], body[
                'email'], body['password'], body['firstname'], body['lastname']
            email = email.lower()
        except Exception:
            return jsonify({'message': 'invalid body provided'}), 400

        if re.search(r'^\+1[0-9]{10}$', phone_number) is None:
            return jsonify({'message': 'invalid phone number provided'}), 400

        if re.search(r'^.+@.+\..+$', email) is None:
            return jsonify({'message': 'invalid email provided'}), 400

        cognito_request = requests.post(
            'https://1sz21h77li.execute-api.us-east-2.amazonaws.com/Dev/signup',
            data=json.dumps({
                'phone': phone_number,
                'email': email,
                'password': password,
                'firstname': first_name,
                'lastname': last_name
            })
        )

        if cognito_request.json()['error']:
            return cognito_request.json(), cognito_request.status_code

        db.create_user(
            cognito_request.json()['user']['UserSub'], first_name, last_name, email, phone_number)

        return cognito_request.json(), 200
    else:
        return jsonify({'message': 'method not allowed'}), 405


@usersbp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        try:
            body = request.get_json()
            validate(body, schema=schema.login_schema)

            email, password = body['email'], body['password']
            email = email.lower()
        except Exception:
            return jsonify({'message': 'invalid body provided'}), 400

        if re.search(r'^.+@.+\..+$', email) is None:
            return jsonify({'message': 'invalid email provided'}), 400

        cognito_request = requests.post(
            'https://1sz21h77li.execute-api.us-east-2.amazonaws.com/Dev/login',
            data=json.dumps({
                'email': email,
                'password': password
            })
        )

        if cognito_request.json()['error']:
            return cognito_request.json(), cognito_request.status_code

        return cognito_request.json(), 200
    else:
        return jsonify({'message': 'method not allowed'}), 405


@usersbp.route('/user', methods=['GET'])
@login_required
def get_user():
    if request.method == 'GET':
        message, error, data = db.get_user(current_user.user_id)

        if error:
            return jsonify({'message': message}), 500

        return jsonify(data), 200
    else:
        return jsonify({'message': 'method not allowed'}), 405


@usersbp.route('/user/addPhone', methods=['POST'])
@login_required
def add_phone():
    if request.method == 'POST':
        try:
            body = request.get_json()
            validate(body, schema=schema.addphone_schema)

            phone_number = body['phone']
        except Exception:
            return jsonify({'message': 'invalid body provided'}), 400

        if re.search(r'^\+1[0-9]{10}$', phone_number) is None:
            return jsonify({'message': 'invalid phone number provided'}), 400

        message, error, data = db.check_if_user_has_phone_number(
            current_user.user_id, phone_number)

        if error:
            return jsonify({'message': message}), 500

        if data['exists'] == 1:
            return jsonify({'message': 'user already has phone number'}), 400

        message, error, data = db.add_phone_number_to_user(
            phone_number, current_user.user_id)

        if error:
            return jsonify({'message': message}), 500

        return jsonify({'message': message}), 200
    else:
        return jsonify({'message': 'method not allowed'}), 405


@usersbp.route('/user/removePhone', methods=['POST'])
@login_required
def remove_phone():
    if request.method == 'POST':
        try:
            body = request.get_json()
            validate(body, schema=schema.removephone_schema)

            phone_number = body['phone']
        except Exception:
            return jsonify({'message': 'invalid body provided'}), 400

        if re.search(r'^\+1[0-9]{10}$', phone_number) is None:
            return jsonify({'message': 'invalid phone number provided'}), 400

        message, error, data = db.check_if_user_has_phone_number(
            current_user.user_id, phone_number)

        if error:
            return jsonify({'message': message}), 500

        if data['exists'] == 0:
            return jsonify({'message': 'user does not have phone number'}), 400

        message, error, data = db.remove_phone_number_from_user(
            phone_number, current_user.user_id)

        if error:
            return jsonify({'message': message}), 500

        return jsonify({'message': message}), 200
    else:
        return jsonify({'message': 'method not allowed'}), 405


@usersbp.route('/user/profilePicture', methods=['GET', 'POST', 'PUT'])
@login_required
def profile_picture():
    if request.method == 'GET':
        message, error, data = db.get_users_profile_picture(
            current_user.user_id)

        if error:
            return jsonify({'message': message}), 500

        if data is None:
            data = {
                'profile_picture': None
            }

        return jsonify(data), 200
    elif request.method == 'POST' or request.method == 'PUT':
        try:
            body = request.get_json()
            validate(body, schema=schema.profilepicture_schema)

            profile_picture = body['profile_picture']
        except Exception:
            return jsonify({'message': 'invalid body provided'}), 400

        if re.search(r'^data:image\/jpeg;base64,(?:[A-Za-z0-9+\/]{4})*(?:[A-Za-z0-9+\/]{2}==|[A-Za-z0-9+\/]{3}=)?$', profile_picture) is None:
            return jsonify({'message': 'invalid profile picture provided'}), 400

        profile_picture = profile_picture[23:]
        obj = AWS.Object('gametime-file-storage',
                         f'{current_user.user_id}.jpeg')
        obj.put(Body=base64.b64decode(profile_picture), ACL='public-read')
        image_url = f'https://gametime-file-storage.s3-us-east-2.amazonaws.com/{current_user.user_id}.jpeg'

        message, error, data = db.edit_users_profile_picture(
            current_user.user_id, image_url)

        if error:
            return jsonify({'message': message}), 500

        return jsonify({'message': message}), 200
    else:
        return jsonify({'message': 'method not allowed'}), 405
