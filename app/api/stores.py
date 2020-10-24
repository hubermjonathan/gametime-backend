from flask import Blueprint, jsonify, request, abort
from jsonschema import validate
from flask_login import login_required, current_user
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

        # TODO: implement permissions and auth

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

        # TODO: implement permissions and auth

        try:
            validate(body, schema=schema.place_order_schema)
        except:
            return jsonify({'message': 'Bad Request'}), 400

        team_id, buyer_email, buyer_address, items = body['team_id'], body[
            'buyer_email'], body['buyer_address'], body['items']

        # Call to register a transaction
        message, error, data = order.create_transaction(
            team_id, buyer_email, buyer_address, items)
        if error:
            return jsonify({'message': 'Failed to place order'}), 400

        return jsonify({'message': 'Succesfully placed order'}), 200


@storesbp.route('/store/create', methods=['POST'])
# @login_required
def create_item():
    # POST, make an order
    if request.method == 'POST':
        body = request.get_json()

        # TODO: implement permissions and auth

        try:
            validate(body, schema=schema.create_item_schema)
        except:
            return jsonify({'message': 'Bad Request'}), 400

        team_id, name, types, picture, price, active = body['team_id'], body[
            'name'], body['types'], body['picture'], body['price'], body['active']

        # Call to register a transaction
        message, error, data = store.create_store_item(
            team_id, name, price, active, types, picture)
        if error:
            return jsonify({'message': 'Failed to create item'}), 400

        return jsonify({'message': 'Succesfully created item'}), 200
