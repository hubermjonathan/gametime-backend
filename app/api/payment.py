from flask import Blueprint, jsonify, request, abort
from . import schema
from flask_login import login_required, current_user
from .. import auth
from os import environ

import boto3
import stripe

paymentsbp = Blueprint('paymentsbp', __name__)

stripe.api_key = environ.get('STRIPE_PRIVATE_KEY')


@paymentsbp.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
  session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
      'price_data': {
        'currency': 'usd',
        'product_data': {
          'name': 'T-shirt',
        },
        'unit_amount': 2000,
      },
      'quantity': 1,
    }],
    mode='payment',
    success_url='https://example.com/success',
    cancel_url='https://example.com/cancel',
  )

  return jsonify(id=session.id)