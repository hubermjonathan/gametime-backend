from flask import Blueprint, request, jsonify
from .. import db

import requests
import json

from flask_login import login_required


testbp = Blueprint('testbp', __name__)


def create_user(phone, email, password, first_name, last_name):
    requests.post(
        'https://1sz21h77li.execute-api.us-east-2.amazonaws.com/Dev/signup',
        data=json.dumps({
            'phone': phone,
            'email': email,
            'password': password,
            'firstname': first_name,
            'lastname': last_name
        })
    )


@testbp.route('/test')
def test():
    result = db.teams.create_team(
        'test', '06d0725b-9130-45e4-958f-52fd959220ee')
    return jsonify(result), 200


@testbp.route('/create_data')
def create_test_data():
    db.schema.reset_tables(request.args.get('db'))

    coach1 = db.users.create_user(
        'coach1', 'coach1', 'coach1-email1@gmail.com', '+16613104788')
    coach2 = db.users.create_user(
        'coach2', 'coach2', 'coach2-email1@gmail.com', '+16613104788')

    player1 = db.users.create_user(
        'player1', 'player1', 'player1-email1@gmail.com', '+16613104788')
    db.users.add_phone_number_to_user(
        player1[2]['user_id'], '+16613104788')
    db.users.add_phone_number_to_user(
        player1[2]['user_id'], '+16613104788')

    player2 = db.users.create_user(
        'player2', 'player2', 'player2-email1@gmail.com', '+16613104788')
    db.users.add_phone_number_to_user(
        player2[2]['user_id'], '+16613104788')
    db.users.add_phone_number_to_user(
        player2[2]['user_id'], '+16613104788')

    player3 = db.users.create_user(
        'player3', 'player3', 'player3-email1@gmail.com', '+16613104788')
    db.users.add_phone_number_to_user(
        player3[2]['user_id'], '+16613104788')
    db.users.add_phone_number_to_user(
        player3[2]['user_id'], '+16613104788')

    player4 = db.users.create_user(
        'player4', 'player4', 'player4-email1@gmail.com', '+16613104788')
    db.users.add_phone_number_to_user(
        player4[2]['user_id'], '+16613104788')
    db.users.add_phone_number_to_user(
        player4[2]['user_id'], '+16613104788')

    player5 = db.users.create_user(
        'player5', 'player5', 'player5-email1@gmail.com', '+16613104788')
    db.users.add_phone_number_to_user(
        player5[2]['user_id'], '+16613104788')
    db.users.add_phone_number_to_user(
        player5[2]['user_id'], '+16613104788')

    player6 = db.users.create_user(
        'player6', 'player6', 'player6-email1@gmail.com', '+16613104788')
    db.users.add_phone_number_to_user(
        player6[2]['user_id'], '+16613104788')
    db.users.add_phone_number_to_user(
        player6[2]['user_id'], '+16613104788')

    player7 = db.users.create_user(
        'player7', 'player7', 'player7-email1@gmail.com', '+16613104788')
    db.users.add_phone_number_to_user(
        player7[2]['user_id'], '+16613104788')
    db.users.add_phone_number_to_user(
        player7[2]['user_id'], '+16613104788')

    player8 = db.users.create_user(
        'player8', 'player8', 'player8-email1@gmail.com', '+16613104788')
    db.users.add_phone_number_to_user(
        player8[2]['user_id'], '+16613104788')
    db.users.add_phone_number_to_user(
        player8[2]['user_id'], '+16613104788')

    player9 = db.users.create_user(
        'player9', 'player9', 'player9-email1@gmail.com', '+16613104788')
    db.users.add_phone_number_to_user(
        player9[2]['user_id'], '+16613104788')
    db.users.add_phone_number_to_user(
        player9[2]['user_id'], '+16613104788')

    player10 = db.users.create_user(
        'player10', 'player10', 'player10-email1@gmail.com', '+16613104788')
    db.users.add_phone_number_to_user(
        player10[2]['user_id'], '+16613104788')
    db.users.add_phone_number_to_user(
        player10[2]['user_id'], '+16613104788')

    team1 = db.teams.create_team('team1', coach1[2]['user_id'])
    team2 = db.teams.create_team('team2', coach2[2]['user_id'])

    db.teams.add_user_to_team(player1[2]['user_id'], team1[2]['team_id'])
    db.teams.add_user_to_team(player2[2]['user_id'], team1[2]['team_id'])
    db.teams.add_user_to_team(player3[2]['user_id'], team1[2]['team_id'])
    db.teams.add_user_to_team(player4[2]['user_id'], team1[2]['team_id'])
    db.teams.add_user_to_team(player5[2]['user_id'], team1[2]['team_id'])
    db.teams.add_user_to_team(player6[2]['user_id'], team1[2]['team_id'])
    db.teams.add_user_to_team(player7[2]['user_id'], team1[2]['team_id'])
    db.teams.add_user_to_team(player1[2]['user_id'], team2[2]['team_id'])
    db.teams.add_user_to_team(player2[2]['user_id'], team2[2]['team_id'])
    db.teams.add_user_to_team(player6[2]['user_id'], team2[2]['team_id'])
    db.teams.add_user_to_team(player7[2]['user_id'], team2[2]['team_id'])
    db.teams.add_user_to_team(player8[2]['user_id'], team2[2]['team_id'])
    db.teams.add_user_to_team(player9[2]['user_id'], team2[2]['team_id'])
    db.teams.add_user_to_team(player10[2]['user_id'], team2[2]['team_id'])

    db.teams.edit_users_permission_level_for_team(
        player4[2]['user_id'], team1[2]['team_id'], 1)
    db.teams.edit_users_permission_level_for_team(
        player5[2]['user_id'], team1[2]['team_id'], 1)
    db.teams.edit_users_permission_level_for_team(
        player10[2]['user_id'], team2[2]['team_id'], 1)

    group1 = db.groups.create_group('group1', team1[2]['team_id'])
    group2 = db.groups.create_group('group2', team2[2]['team_id'])

    db.groups.add_user_to_group(player3[2]['user_id'], group1[2]['group_id'])
    db.groups.add_user_to_group(player4[2]['user_id'], group1[2]['group_id'])
    db.groups.add_user_to_group(player5[2]['user_id'], group1[2]['group_id'])
    db.groups.add_user_to_group(player6[2]['user_id'], group1[2]['group_id'])

    db.groups.add_user_to_group(player1[2]['user_id'], group2[2]['group_id'])
    db.groups.add_user_to_group(player9[2]['user_id'], group2[2]['group_id'])
    db.groups.add_user_to_group(player10[2]['user_id'], group2[2]['group_id'])

    db.messages.create_group_message(
        group1[2]['group_id'], coach1[2]['user_id'], 'group1-team1-message1')
    db.messages.create_group_message(
        group1[2]['group_id'], coach1[2]['user_id'], 'group1-team1-message2')
    db.messages.create_group_message(
        group1[2]['group_id'], coach1[2]['user_id'], 'group1-team1-message3')

    db.messages.create_group_message(
        group2[2]['group_id'], coach2[2]['user_id'], 'group2-team2-message1')
    db.messages.create_group_message(
        group2[2]['group_id'], coach2[2]['user_id'], 'group2-team2-message2')
    db.messages.create_group_message(
        group2[2]['group_id'], coach2[2]['user_id'], 'group2-team2-message3')

    db.messages.create_direct_message(
        player1[2]['user_id'], coach1[2]['user_id'], 'player1-team1-message1')
    db.messages.create_direct_message(
        player2[2]['user_id'], coach1[2]['user_id'], 'player2-team1-message1')
    db.messages.create_direct_message(
        player3[2]['user_id'], coach1[2]['user_id'], 'player3-team1-message1')
    db.messages.create_direct_message(
        player4[2]['user_id'], coach1[2]['user_id'], 'player4-team1-message1')
    db.messages.create_direct_message(
        player5[2]['user_id'], coach1[2]['user_id'], 'player5-team1-message1')
    db.messages.create_direct_message(
        player6[2]['user_id'], coach1[2]['user_id'], 'player6-team1-message1')
    db.messages.create_direct_message(
        player7[2]['user_id'], coach1[2]['user_id'], 'player7-team1-message1')

    db.messages.create_direct_message(
        player1[2]['user_id'], coach2[2]['user_id'], 'player1-team2-message1')
    db.messages.create_direct_message(
        player2[2]['user_id'], coach2[2]['user_id'], 'player2-team2-message1')
    db.messages.create_direct_message(
        player6[2]['user_id'], coach2[2]['user_id'], 'player6-team2-message1')
    db.messages.create_direct_message(
        player7[2]['user_id'], coach2[2]['user_id'], 'player7-team2-message1')
    db.messages.create_direct_message(
        player8[2]['user_id'], coach2[2]['user_id'], 'player8-team2-message1')
    db.messages.create_direct_message(
        player9[2]['user_id'], coach2[2]['user_id'], 'player9-team2-message1')
    db.messages.create_direct_message(
        player10[2]['user_id'], coach2[2]['user_id'], 'player10-team2-message1')

    return 'successfully created data'
