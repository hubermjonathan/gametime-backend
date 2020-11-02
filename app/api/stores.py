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
    # POST, create an item
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


@storesbp.route('/store/delete', methods=['DELETE'])
# @login_required
def delete_item():
    # DELETE, remove an item
    if request.method == 'DELETE':
        body = request.get_json()

        # TODO: implement permissions and auth

        try:
            validate(body, schema=schema.delete_item_schema)
        except:
            return jsonify({'message': 'Bad Request'}), 400

        item_id = body['item_id']

        # Call to archive and retire item
        message, error, data = store.remove_store_item(item_id)
        if error:
            print(message)
            return jsonify({'message': 'Failed to delete item'}), 400

        return jsonify({'message': 'Succesfully deleted item'}), 200


@storesbp.route('/store/update', methods=['PUT'])
# @login_required
def edit_item():
    # PUT, remove an item
    if request.method == 'PUT':
        body = request.get_json()

        # TODO: implement permissions and auth

        try:
            validate(body, schema=schema.edit_item_schema)
        except:
            return jsonify({'message': 'Bad Request'}), 400

        item_id, name, types, picture, price, active = body['item_id'], body[
            'name'], body['types'], body['picture'], body['price'], body['active']

        # Call to update item details
        message, error, data = store.edit_store_item(
            item_id, name, price, active, types)
        if error:
            print(message)
            return jsonify({'message': 'Failed to update item'}), 400

        return jsonify({'message': 'Succesfully updated item'}), 200


@storesbp.route('/store/status/', methods=['POST', 'PUT'])
# @login_required
def orders():
    # POST, fetch orders from DB
    if request.method == 'POST':
        body = request.get_json()

        # TODO: implement permissions and auth

        try:
            validate(body, schema=schema.get_orders_schema)
        except:
            return jsonify({'message': 'Bad Request'}), 400

        team_id = body['team_id']

        # Call to fetch items from DB
        message, error, data = order.get_teams_transactions(team_id)

        if error:
            return jsonify({'message': 'Failed to fetch orders'}), 400

        return jsonify(data), 200

    # PUT, update order status
    if request.method == 'PUT':
        body = request.get_json()

        # TODO: implement permissions and auth

        try:
            validate(body, schema=schema.update_order_schema)
        except:
            return jsonify({'message': 'Bad Request'}), 400

        order_id, status = body['order_id'], body['status']

        # Call to fetch items from DB
        # TODO: Currently succeeds when updating a transaction that does not exist.
        message, error, data = order.edit_transactions_status(order_id, status)

        if error:
            print(message)
            return jsonify({'message': 'Failed to update order status'}), 400

        return jsonify({'message': 'Succesfully updated order status'}), 200