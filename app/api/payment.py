from flask import Blueprint, jsonify, request, abort
from . import schema
from flask_login import login_required, current_user
from .. import auth
from os import environ

from ..db import store as store

import boto3
import stripe

paymentsbp = Blueprint('paymentsbp', __name__)

stripe.api_key = environ.get('STRIPE_PRIVATE_KEY')


@paymentsbp.route('/createCheckoutSession', methods=['POST'])
def create_checkout_session():
  body = request.get_json()

  try:
    item_list = body['item_ids']
  

    line_items = []
    for item in item_list:
      itemId = item[0]
      itemQ = item[1]

      itemData = store.get_item(itemId)[2]
      line_items.append(
        {
          'price_data': {
            'currency': 'usd',
            'product_data': {
              'name': itemData['name'],
            },
            'unit_amount_decimal': (int)(itemData['price']*100), #convert to cents
          },
          'quantity': itemQ,
        })
  except KeyError:
    return "missing field in body", 400
  except Exception as e:
    return str(e), 500

  try:
    session = stripe.checkout.Session.create(
      payment_method_types=['card'],
      line_items=line_items,
      mode='payment',
      success_url=body['success_url'],
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
    session = stripe.checkout.Session.create(
      payment_method_types=['card'],
      line_items=[{
          'price_data': {
            'currency': 'usd',
            'product_data': {
              'name': 'Donation',
            },
            'unit_amount_decimal': (int)(body['donation_amount']), #convert to cents
          },
          'quantity': 1,
        }],
      mode='payment',
      success_url='https://example.com/success',
      cancel_url='https://example.com/cancel',
      customer_email=body['email']
    )

    return jsonify(id=session.id), 200
  except stripe.error.InvalidRequestError as e:
    return ' '.join(str(e).split(' ')[2:]), 400
  except KeyError:
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