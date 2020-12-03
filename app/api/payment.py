from flask import Blueprint, jsonify, request, abort
from . import schema
from flask_login import login_required, current_user
from .. import auth
from os import environ

from ..db import transactions as order
from ..db import store as store
from ..db import teams as team
from ..db import fundraising as fund

import boto3
import stripe

paymentsbp = Blueprint('paymentsbp', __name__)

stripe.api_key = environ.get('STRIPE_PRIVATE_KEY')


@paymentsbp.route('/createCheckoutSession', methods=['POST'])
def create_checkout_session():
  body = request.get_json()

  try:
    item_list = body['items']
  
    totalPrice = 0

    line_items = []
    for item in item_list:
      itemData = store.get_item(item['item_id'])[2]

      line_items.append(
        {
          'price_data': {
            'currency': 'usd',
            'product_data': {
              'name': itemData['name'],
            },
            'unit_amount_decimal': (int)(itemData['price'])*100, #convert to cents
          },
          'quantity': item['quantity'],
        })

      totalPrice += itemData['price']
  except KeyError:
    return "missing field in body", 400
  except Exception as e:
    return str(e), 500

  try:
    message, error, data = order.create_transaction(
            body['team_id'], body['email'], body['buyer_address'], body['items'], totalPrice, None)

    session = stripe.checkout.Session.create(
      payment_method_types=['card'],
      line_items=line_items,
      mode='payment',
      success_url=body['success_url'] + data['transaction_id'],
      cancel_url=body['cancel_url'],
      customer_email=body['email']
    )

    return jsonify(id=session.id), 200
  except stripe.error.InvalidRequestError as e:
    return ' '.join(str(e).split(' ')[2:]), 400
  except KeyError:
    return "missing field in body", 400
  except Exception as e:
    return str(e), 500

@paymentsbp.route('/createDonationSession', methods=['POST'])
def create_donation_session():
  body = request.get_json()

  try:
    message, error, data = order.create_transaction(
        body['team_id'], body['email'], None, [], body['donation_amount'], body['player_id'])

    print(data)

    if error:
        return error, 500

    session = stripe.checkout.Session.create(
      payment_method_types=['card'],
      line_items=[{
          'price_data': {
            'currency': 'usd',
            'product_data': {
              'name': 'Donation',
            },
            'unit_amount_decimal': (int)(body['donation_amount']) * 100, #convert to cents
          },
          'quantity': 1,
        }],
      mode='payment',
      success_url=body['success_url'] + data['transaction_id'],
      cancel_url=body['cancel_url'],
      customer_email=body['email']
    )

    return jsonify(id=session.id), 200
  except stripe.error.InvalidRequestError as e:
    return ' '.join(str(e).split(' ')[2:]), 400
  except KeyError as e:
    print(e)
    return "missing field in body", 400
  except Exception as e:
    return str(e), 500

@paymentsbp.route('/changeBankAccount', methods=['POST'])
@login_required
def change_bank_account():
  body = request.get_json()

  try:
    teamId = body["team_id"]
    accountNum = body["account_number"]
    routingNum = body["routing_number"]
  except:
      return "missing field", 400

  if not auth.isOwner(current_user.user_id, teamId):
    return "Not owner of team", 401

@paymentsbp.route('/confirmTransaction', methods=['POST'])
def confirmTransaction():
  body = request.get_json()
  
  try:
    transaction_id = body['transaction_id']
  except:
    return "missing field", 400

  message, error, data = order.get_transaction(transaction_id)

  if error:
    return "database error", 500

  message, Error, teamData = team.get_team_account(data['team_id'])

  if error:
    return "database error", 500

  payout = stripe.Payout.create(
    amount=data['amount'],
    currency='usd',
    method='instant',
    destination=teamData['bank_id'],
  )

  if data['player_id'] and data['address'] is None:
    message, error, data = fund.donate_to_user(data['team_id'], data['player_id'], data['amount'])
    if error:
      return "database error", 500  
  elif data['address'] is None:
    message, error, data = fund.donate_to_team(data['team_id'], data['amount'])
    if error:
      return "database error", 500

  message, error, data = order.edit_transactions_status(transaction_id, 1)

  if error:
    return "database error", 500

  return "success", 200
