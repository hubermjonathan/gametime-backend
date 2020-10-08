from flask import Blueprint, jsonify, request, abort
from jsonschema import validate
import requests
import json
from ..db import users as db
from ..db import connect
from . import schema

usersbp = Blueprint('usersbp', __name__)
connection = None


@usersbp.before_request
def connect_db():
    global connection
    connection = connect()


@usersbp.after_request
def disconnect_db(response):
    global connection
    if connection:
        connection.close()
        connection = None
    return response


@usersbp.route('/signup', methods=['POST'])
def signup():
    # POST, Creates a new user
    if request.method == 'POST':
        body = request.get_json()

        try:
            validate(body, schema=schema.create_user_schema)
        except Exception as e:
            return jsonify(str(e)), 400

        phone, email, password, first_name, last_name = body['phone'], body['email'], body['password'], body['firstname'], body['lastname']

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

        res = new_user_id
        return jsonify(res), 200
