from flask import Blueprint, jsonify, request, abort
from jsonschema import validate
import requests
import json
import re
from flask_login import login_required
from ..db import users as db
from . import schema

usersbp = Blueprint('usersbp', __name__)


@usersbp.route('/signup', methods=['POST'])
def signup():
    # POST, Creates a new user
    if request.method == 'POST':
        body = request.get_json()

        try:
            validate(body, schema=schema.signup_schema)
        except Exception as e:
            return jsonify(str(e)), 400

        phone, email, password, first_name, last_name = body['phone'], body[
            'email'], body['password'], body['firstname'], body['lastname']
        email = email.lower()

        r = requests.post(
            'https://1sz21h77li.execute-api.us-east-2.amazonaws.com/Dev/signup',
            data=json.dumps({
                'phone': phone,
                'email': email,
                'password': password,
                'firstname': first_name,
                'lastname': last_name
            })
        )

        if (r.json()['error'] is not False):
            res = r.json()
            return res, r.status_code

        message, error, data = db.create_user(
            first_name, last_name, email, phone)

        res = r.json()
        res.update(data)
        return jsonify(res), 200


@usersbp.route('/login', methods=['POST'])
def login():
    # POST, Logs a user in
    if request.method == 'POST':
        try:
            body = request.get_json()

            try:
                validate(body, schema=schema.login_schema)
            except Exception as e:
                return jsonify(str(e)), 400

            email, password = body['email'], body['password']
            email = email.lower()

            r = requests.post(
                'https://1sz21h77li.execute-api.us-east-2.amazonaws.com/Dev/login',
                data=json.dumps({
                    'email': email,
                    'password': password
                })
            )

            if (r.json()['error'] is not False):
                res = r.json()
                return res, r.status_code

            message, error, data = db.get_user_id(email)

            res = r.json()
            res.update(data)

            return jsonify(res), 200
        except Exception as e:
            print(str(e))
            return "", 500

        return "", 500


@login_required
@usersbp.route('/user', methods=['GET'])
def get_user():
    # GET, Gets info about a user
    if request.method == 'GET':
        user_id = request.args.get('id')

        try:
            message, error, user_info = db.get_user(user_id)
            if error:
                return message, 500

            return jsonify(user_info), 200
        except Exception as e:
            print(e)

        return "", 500


@login_required
@usersbp.route('/user/phone/add', methods=['POST'])
def addPhone():
    # POST, Add Phone Number to User
    body = request.get_json()

    user_id = body['id']
    phone = body['phone']

    # Pattern = re.compile("\1[0-9]{10}")
    # if not Pattern.match(phone):
    #     return jsonify({"reason": "phone number invalid"}), 400

    message, error, data = db.check_if_user_has_phone_number(
        user_id, phone)

    if data['exists'] == 1:
        return jsonify({"reason": "user already has phone number"}), 400

    message, error, data = db.add_phone_number_to_user(
        phone, user_id)

    if error:
        return jsonify({"reason": "internal server error"}), 500

    return jsonify({"reason": "phone number added"}), 200


@login_required
@usersbp.route('/user/phone/remove', methods=['POST'])
def removePhone():
    # POST, Remove Phone Number from User
    body = request.get_json()

    user_id = body['id']
    phone = body['phone']

    # Pattern = re.compile("\1[0-9]{10}")
    # if not Pattern.match(phone):
    #     return jsonify({"reason": "phone number invalid"}), 400

    message, error, data = db.remove_phone_number_from_user(phone, user_id)

    if error:
        return jsonify({"reason": "internal server error"}), 500

    return jsonify({"reason": "phone number removed"}), 200
