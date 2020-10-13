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

        new_user_id = db.create_user(
            first_name + ' ' + last_name, email, phone)

        res = r.json()
        res['user_id'] = new_user_id[2]
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

            user_id = db.get_user_id(email)

            res = r.json()
            res['user_id'] = user_id[2]
            '''
            SELECT user_id
            FROM users
            WHERE email=%s;
            ''',
            (email,)
            print('USER ID\n\n', user_id)
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

        print('USER ID\n\n', user_id)

        try:
            message, status, user_info = db.get_user(user_id)
            if status != 200:
                return message, status

            res = {
                'user_id': user_info[0],
                'name': user_info[1],
                'email': user_info[2],
                'phone_number': user_info[3],
                'profile_picture': user_info[4],
                'extra_phone_numbers': user_info[5]
            }
            return jsonify(res), 200
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

    message, status, user_info = db.check_phone_number_exists(
        user_id, phone)

    if user_info:
        return jsonify({"reason": "user already has phone number"}), 400

    message, status, user_info = db.add_phone_number(
        user_id, phone)

    if status == 500:
        return jsonify({"reason": "internal server error"}), status

    if status == 200:
        return jsonify({"reason": "phone number added"}), status

    return jsonify({"reason": "unknown"}), status


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

    message, status, user_info = db.remove_phone_number(
        user_id, phone)

    if status == 500:
        return jsonify({"reason": "internal server error"}), status

    if status == 200:
        return jsonify({"reason": "phone number removed"}), status

    return jsonify({"reason": "unknown"}), status


@login_required
@usersbp.route('/user/teams', methods=['GET'])
def getTeams():
    # GET, gets all teams user is on
    user_id = request.args.get('id')

    message, status, teams = db.get_users_teams(user_id)

    res = {
        'teams': teams
    }
    return jsonify(res), 200
