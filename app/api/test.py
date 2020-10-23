import requests
import json
import os
from flask import Blueprint, request, jsonify
from flask_login import login_required
import boto3
from .. import db


testbp = Blueprint('testbp', __name__)
test_phone = '+16613104788'

AWS = boto3.client(
    'cognito-idp',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
    region_name='us-east-2'
)


def delete_all_cognito_users():
    users = AWS.list_users(
        UserPoolId=os.environ.get('AWS_COGNITO_POOL_ID'),
        AttributesToGet=[]
    )

    for user in users['Users']:
        AWS.admin_delete_user(
            UserPoolId=os.environ.get('AWS_COGNITO_POOL_ID'),
            Username=user['Username']
        )


def create_user(name):
    email = f'{name}@hubermjonathan.com'
    password = 'TestTest123123'

    cognito_request = requests.post(
        'https://1sz21h77li.execute-api.us-east-2.amazonaws.com/Dev/signup',
        data=json.dumps({
            'phone': test_phone,
            'email': email,
            'password': password,
            'firstname': name,
            'lastname': name
        })
    )

    user = db.users.create_user(
        cognito_request.json()['user']['UserSub'], name, name, email, test_phone)
    return user[2]['user_id']


@testbp.route('/test')
def test():
    # result = db.transactions.create_transaction('e1aae866-d1df-4e85-8fb8-0b01cf05eee6', 'test', 'test', [
    #     {
    #         'item_id': '6a1bccc3-4273-4fb2-a289-b259aa1827b2',
    #         'quantity': 1
    #     },
    #     {
    #         'item_id': 'e1127dbe-fa87-4d25-8304-b37b5bf36765',
    #         'quantity': 2
    #     }
    # ])
    # result = db.transactions.get_item(
    #     '6a1bccc3-4273-4fb2-a289-b259aa1827b2')
    return jsonify(result), 200


@testbp.route('/create_data')
def create_test_data():
    db.schema.reset_tables(request.args.get('db'))
    delete_all_cognito_users()

    coach1 = create_user('coach1')
    coach2 = create_user('coach2')

    player1 = create_user('player1')
    db.users.add_phone_number_to_user(player1, test_phone)
    db.users.add_phone_number_to_user(player1, test_phone)

    player2 = create_user('player2')
    db.users.add_phone_number_to_user(player2, test_phone)
    db.users.add_phone_number_to_user(player2, test_phone)

    player3 = create_user('player3')
    db.users.add_phone_number_to_user(player3, test_phone)
    db.users.add_phone_number_to_user(player3, test_phone)

    player4 = create_user('player4')
    db.users.add_phone_number_to_user(player4, test_phone)
    db.users.add_phone_number_to_user(player4, test_phone)

    player5 = create_user('player5')
    db.users.add_phone_number_to_user(player5, test_phone)
    db.users.add_phone_number_to_user(player5, test_phone)

    player6 = create_user('player6')
    db.users.add_phone_number_to_user(player6, test_phone)
    db.users.add_phone_number_to_user(player6, test_phone)

    player7 = create_user('player7')
    db.users.add_phone_number_to_user(player7, test_phone)
    db.users.add_phone_number_to_user(player7, test_phone)

    player8 = create_user('player8')
    db.users.add_phone_number_to_user(player8, test_phone)
    db.users.add_phone_number_to_user(player8, test_phone)

    player9 = create_user('player9')
    db.users.add_phone_number_to_user(player9, test_phone)
    db.users.add_phone_number_to_user(player9, test_phone)

    player10 = create_user('player10')
    db.users.add_phone_number_to_user(player10, test_phone)
    db.users.add_phone_number_to_user(player10, test_phone)

    team1 = db.teams.create_team('team1', coach1)
    team1 = team1[2]['team_id']
    team2 = db.teams.create_team('team2', coach2)
    team2 = team2[2]['team_id']

    db.teams.add_user_to_team(player1, team1)
    db.teams.add_user_to_team(player2, team1)
    db.teams.add_user_to_team(player3, team1)
    db.teams.add_user_to_team(player4, team1)
    db.teams.add_user_to_team(player5, team1)
    db.teams.add_user_to_team(player6, team1)
    db.teams.add_user_to_team(player7, team1)
    db.teams.add_user_to_team(player1, team2)
    db.teams.add_user_to_team(player2, team2)
    db.teams.add_user_to_team(player6, team2)
    db.teams.add_user_to_team(player7, team2)
    db.teams.add_user_to_team(player8, team2)
    db.teams.add_user_to_team(player9, team2)
    db.teams.add_user_to_team(player10, team2)

    db.teams.edit_users_permission_level_for_team(player4, team1, 1)
    db.teams.edit_users_permission_level_for_team(player5, team1, 1)
    db.teams.edit_users_permission_level_for_team(player10, team2, 1)

    group1 = db.groups.create_group('group1', team1)
    group1 = group1[2]['group_id']
    group2 = db.groups.create_group('group2', team2)
    group2 = group2[2]['group_id']

    db.groups.add_user_to_group(player3, group1)
    db.groups.add_user_to_group(player4, group1)
    db.groups.add_user_to_group(player5, group1)
    db.groups.add_user_to_group(player6, group1)

    db.groups.add_user_to_group(player1, group2)
    db.groups.add_user_to_group(player9, group2)
    db.groups.add_user_to_group(player10, group2)

    db.messages.create_group_message(group1, coach1, 'group1-team1-m1')
    db.messages.create_group_message(group1, coach1, 'group1-team1-m2')
    db.messages.create_group_message(group1, coach1, 'group1-team1-m3')

    db.messages.create_group_message(group2, coach2, 'group2-team2-m1')
    db.messages.create_group_message(group2, coach2, 'group2-team2-m2')
    db.messages.create_group_message(group2, coach2, 'group2-team2-m3')

    db.messages.create_direct_message(player1, coach1, 'player1-team1-m1')
    db.messages.create_direct_message(player2, coach1, 'player2-team1-m1')
    db.messages.create_direct_message(player3, coach1, 'player3-team1-m1')
    db.messages.create_direct_message(player4, coach1, 'player4-team1-m1')
    db.messages.create_direct_message(player5, coach1, 'player5-team1-m1')
    db.messages.create_direct_message(player6, coach1, 'player6-team1-m1')
    db.messages.create_direct_message(player7, coach1, 'player7-team1-m1')

    db.messages.create_direct_message(player1, coach2, 'player1-team2-m1')
    db.messages.create_direct_message(player2, coach2, 'player2-team2-m1')
    db.messages.create_direct_message(player6, coach2, 'player6-team2-m1')
    db.messages.create_direct_message(player7, coach2, 'player7-team2-m1')
    db.messages.create_direct_message(player8, coach2, 'player8-team2-m1')
    db.messages.create_direct_message(player9, coach2, 'player9-team2-m1')
    db.messages.create_direct_message(player10, coach2, 'player10-team2-m1')

    return 'successfully created data'
