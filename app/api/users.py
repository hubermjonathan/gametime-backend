from flask import Blueprint, jsonify, request
from jsonschema import validate
import requests
import json
import re
from flask_login import login_required, current_user
from ..db import users as db
from . import schema

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
