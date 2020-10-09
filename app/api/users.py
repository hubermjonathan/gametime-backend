from flask import Blueprint, jsonify, request, abort
from jsonschema import validate
import requests
import json
from flask_login import login_required
from ..db import users as db
from ..db import connect
from . import schema

usersbp = Blueprint('usersbp', __name__)
connection = None
connection_pool = None


@usersbp.before_request
def connect_db():
    global connection
    global connection_pool
    connection, connection_pool = connect()


@usersbp.after_request
def disconnect_db(response):
    global connection
    global connection_pool
    if connection:
        connection_pool.putconn(connection)
        connection = None
    return response


@usersbp.route('/signup', methods=['POST'])
def signup():
    # POST, Creates a new user
    if request.method == 'POST':
        body = request.get_json()

        try:
            validate(body, schema=schema.signup_schema)
        except Exception as e:
            return jsonify(str(e)), 400

        phone, email, password, first_name, last_name = body['phone'], body['email'], body['password'], body['firstname'], body['lastname']
        email.lower()

        r = requests.post(
            'https://1sz21h77li.execute-api.us-east-2.amazonaws.com/Dev/signup',
            data = json.dumps({
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

        new_user_id = db.create_user(connection, first_name + ' ' + last_name, email, phone)

        res = r.json()
        res['user_id'] = new_user_id[2]
        return jsonify(res), 200


@usersbp.route('/login', methods=['POST'])
def login():
    # POST, Logs a user in
    if request.method == 'POST':
        body = request.get_json()

        try:
            validate(body, schema=schema.login_schema)
        except Exception as e:
            return jsonify(str(e)), 400

        email, password = body['email'], body['password']
        email.lower()

        r = requests.post(
            'https://1sz21h77li.execute-api.us-east-2.amazonaws.com/Dev/login',
            data = json.dumps({
                'email': email,
                'password': password
            })
        )
    
        if (r.json()['error'] is not False):
            res = r.json()
            return res, r.status_code

        user_id = db.get_user_id(connection, email)

        res = r.json()
        res['user_id'] = user_id[2]
        return jsonify(res), 200


@login_required
@usersbp.route('/user', methods=['GET'])
def get_user():
    # GET, Gets info about a user
    if request.method == 'GET':
        user_id = request.args.get('id')

        message, status, user_info = db.get_user(connection, user_id)
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


@login_required
@usersbp.route('/user/phone/add', methods=['POST'])
def addPhone():
    # POST, Add Phone Number to User
    body = request.get_json()

    user_id = body['id']
    phone = body['phone']

    message, status, user_info = db.add_phone_number(connection, user_id, phone)

    return "", status


@login_required
@usersbp.route('/user/phone/remove', methods=['POST'])
def removePhone():
    # POST, Remove Phone Number from User
    body = request.get_json()

    user_id = body['id']
    phone = body['phone']

    message, status, user_info = db.remove_phone_number(connection, user_id, phone)

    return "", status


@login_required
@usersbp.route('/user/teams', methods=['GET'])
def getTeams():
    # GET, gets all teams user is on
    user_id = request.args.get('id')

    message, status, user_info = db.get_users_teams(connection, user_id)

    return jsonify(user_info), status
