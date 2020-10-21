from flask import Blueprint, jsonify, request, abort
from jsonschema import validate
from ..db import groups as db
from . import schema
from flask_login import login_required

storesbp = Blueprint('storesbp', __name__)


@storesbp.route('/store/items/', methods=['GET'])
@login_required
def get_items():
    # GET, fetch items from DB
    if request.method == 'GET':
        group_id = request.args.get('teamid')

        # Fetch items from DB
        # if error:
        #     return jsonify({'message': 'Failed to fetch items'}), 400

        return jsonify(), 200


@storesbp.route('/store/order', methods=['POST'])
@login_required
def place_order():
    # POST, make an order
    if request.method == 'POST':
        body = request.get_json()

        try:
            validate(body, schema=schema.place_order_schema)
        except Exception as e:
            return jsonify(str(e)), 400

        # Make transaction to DB
        # if error:
        #     return jsonify({'message': 'Failed to place order'}), 400

        return jsonify(), 200
