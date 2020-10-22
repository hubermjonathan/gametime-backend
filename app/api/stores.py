from flask import Blueprint, jsonify, request, abort
from jsonschema import validate
from flask_login import login_required
from ..db import store as store
from ..db import transactions as order
from . import schema
from .. import auth

storesbp = Blueprint('storesbp', __name__)


@storesbp.route('/store/items/', methods=['GET'])
# @login_required
def get_items():
    # GET, fetch items from DB
    if request.method == 'GET':
        team_id = request.args.get('teamid')

        # Call to fetch items from DB
        message, error, data = store.get_teams_store_items(team_id)

        if error:
            return jsonify({'message': 'Failed to fetch items'}), 400

        return jsonify(data), 200


@storesbp.route('/store/order', methods=['POST'])
# @login_required
def place_order():
    # POST, make an order
    if request.method == 'POST':
        body = request.get_json()

        try:
            validate(body, schema=schema.place_order_schema)
        except:
            return jsonify({'message': 'Bad Request'}), 400

        # TODO: associate item ids with transaction, figure out how to pull the team_id of the user from token

        # buyer_email, buyer_address, items = body['buyer_email'], body['buyer_address'], body['items']

        # Call to register a transaction
        # message, error, data = order.create_transaction(
            # team_id, buyer_email, buyer_address)
        # if error:
        #     return jsonify({'message': 'Failed to place order'}), 400

        return jsonify(), 200
