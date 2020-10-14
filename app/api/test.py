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
    result = db.users.edit_users_profile_picture(2, 'test')
    return jsonify(result), 200


@testbp.route('/create_data')
def create_test_data():
    db.schema.reset_tables(request.args.get('db'))

    db.users.create_user(
        'coach1', 'coach1', 'coach1-email1@gmail.com', 'coach1-phone1')  # user_id = 1
    db.users.create_user(
        'coach2', 'coach2', 'coach2-email1', 'coach2-phone1')  # user_id = 2

    db.users.create_user(
        'player1', 'player1', 'player1-email1@gmail.com', '12195751591')  # user_id = 3
    db.users.add_phone_number_to_user(
        3, 'player1-phone2')  # add phone to user 3
    db.users.add_phone_number_to_user(
        3, 'player1-phone3')  # add phone to user 3

    db.users.create_user(
        'player2', 'player2', 'player2-email1', 'player2-phone1')  # user_id = 4
    db.users.add_phone_number_to_user(
        4, 'player2-phone2')  # add phone to user 4
    db.users.add_phone_number_to_user(
        4, 'player2-phone3')  # add phone to user 4

    db.users.create_user(
        'player3', 'player3', 'player3-email1', 'player3-phone1')  # user_id = 5
    db.users.add_phone_number_to_user(
        5, 'player3-phone2')  # add phone to user 5
    db.users.add_phone_number_to_user(
        5, 'player3-phone3')  # add phone to user 5

    db.users.create_user(
        'player4', 'player4', 'player4-email1', 'player4-phone1')  # user_id = 6
    db.users.add_phone_number_to_user(
        6, 'player4-phone2')  # add phone to user 6
    db.users.add_phone_number_to_user(
        6, 'player4-phone3')  # add phone to user 6

    db.users.create_user(
        'player5', 'player5', 'player5-email1', 'player5-phone1')  # user_id = 7
    db.users.add_phone_number_to_user(
        7, 'player5-phone2')  # add phone to user 7
    db.users.add_phone_number_to_user(
        7, 'player5-phone3')  # add phone to user 7

    db.users.create_user(
        'player6', 'player6', 'player6-email1', 'player6-phone1')  # user_id = 8
    db.users.add_phone_number_to_user(
        8, 'player6-phone2')  # add phone to user 8
    db.users.add_phone_number_to_user(
        8, 'player6-phone3')  # add phone to user 8

    db.users.create_user(
        'player7', 'player7', 'player7-email1', 'player7-phone1')  # user_id = 9
    db.users.add_phone_number_to_user(
        9, 'player7-phone2')  # add phone to user 9
    db.users.add_phone_number_to_user(
        9, 'player7-phone3')  # add phone to user 9

    db.users.create_user(
        'player8', 'player8', 'player8-email1', 'player8-phone1')  # user_id = 10
    db.users.add_phone_number_to_user(
        10, 'player8-phone2')  # add phone to user 10
    db.users.add_phone_number_to_user(
        10, 'player8-phone3')  # add phone to user 10

    db.users.create_user(
        'player9', 'player9', 'player9-email1', '16613104788')  # user_id = 11
    db.users.add_phone_number_to_user(
        11, 'player9-phone2')  # add phone to user 11
    db.users.add_phone_number_to_user(
        11, 'player9-phone3')  # add phone to user 11

    db.users.create_user(
        'player10', 'player10', 'player10-email1', 'player10-phone1')  # user_id = 12
    db.users.add_phone_number_to_user(
        12, 'player10-phone2')  # add phone to user 12
    db.users.add_phone_number_to_user(
        12, 'player10-phone3')  # add phone to user 12

    db.teams.create_team('team1', 1)  # team_id = 1
    db.teams.create_team('team2', 2)  # team_id = 2

    db.teams.add_user_to_team(4, 1)  # add player 2 to team 1
    db.teams.add_user_to_team(5, 1)  # add player 3 to team 1
    db.teams.add_user_to_team(6, 1)  # add player 4 to team 1
    db.teams.add_user_to_team(7, 1)  # add player 5 to team 1
    db.teams.add_user_to_team(8, 1)  # add player 6 to team 1
    db.teams.add_user_to_team(9, 1)  # add player 7 to team 1
    db.teams.add_user_to_team(3, 2)  # add player 1 to team 2
    db.teams.add_user_to_team(4, 2)  # add player 2 to team 2
    db.teams.add_user_to_team(8, 2)  # add player 6 to team 2
    db.teams.add_user_to_team(9, 2)  # add player 7 to team 2
    db.teams.add_user_to_team(10, 2)  # add player 8 to team 2
    db.teams.add_user_to_team(11, 2)  # add player 9 to team 2
    db.teams.add_user_to_team(12, 2)  # add player 10 to team 2

    db.teams.edit_users_permission_level_for_team(
        6, 1, 1)  # make player 4 admin on team 1
    db.teams.edit_users_permission_level_for_team(
        7, 1, 1)  # make player 5 admin on team 1
    db.teams.edit_users_permission_level_for_team(
        12, 2, 1)  # make player 10 admin on team 2

    db.groups.create_group('group1', 1)  # group_id = 3
    db.groups.create_group('group2', 2)  # group_id = 4

    # add player 3 to group 1 on team 1
    db.groups.add_user_to_group(5, 3)
    # add player 4 to group 1 on team 1
    db.groups.add_user_to_group(6, 3)
    # add player 5 to group 1 on team 1
    db.groups.add_user_to_group(7, 3)
    # add player 6 to group 1 on team 1
    db.groups.add_user_to_group(8, 3)

    # add player 9 to group 2 on team 2
    db.groups.add_user_to_group(11, 4)
    # add player 10 to group 2 on team 2
    db.groups.add_user_to_group(12, 4)
    # add player 1 to group 2 on team 1
    db.groups.add_user_to_group(3, 4)

    db.messages.create_group_message(
        1, 1, 'all-members-team1-message1')  # send message to all players on team 1
    db.messages.create_group_message(
        1, 1, 'all-members-team1-message2')  # send message to all players on team 1
    db.messages.create_group_message(
        1, 1, 'all-members-team1-message3')  # send message to all players on team 1
    db.messages.create_group_message(
        2, 2, 'all-members-team2-message1')  # send message to all players on team 2
    db.messages.create_group_message(
        2, 2, 'all-members-team2-message2')  # send message to all players on team 2
    db.messages.create_group_message(
        2, 2, 'all-members-team2-message3')  # send message to all players on team 2

    db.messages.create_group_message(
        3, 1, 'group1-team1-message1')  # send message to group 1 on team 1
    db.messages.create_group_message(
        3, 1, 'group1-team1-message2')  # send message to group 1 on team 1
    db.messages.create_group_message(
        3, 1, 'group1-team1-message3')  # send message to group 1 on team 1

    db.messages.create_group_message(
        4, 2, 'group2-team2-message1')  # send message to group 2 on team 2
    db.messages.create_group_message(
        4, 2, 'group2-team2-message2')  # send message to group 2 on team 2
    db.messages.create_group_message(
        4, 2, 'group2-team2-message3')  # send message to group 2 on team 2

    # send message to player 3 on team 1
    db.messages.create_direct_message(
        5, 1, 'player3-team1-message1')
    # send message to player 3 on team 1
    db.messages.create_direct_message(
        5, 1, 'player3-team1-message2')
    # send message to player 3 on team 1
    db.messages.create_direct_message(
        5, 1, 'player3-team1-message3')
    # send message to player 4 on team 1
    db.messages.create_direct_message(
        6, 1, 'player4-team1-message1')
    # send message to player 4 on team 1
    db.messages.create_direct_message(
        6, 1, 'player4-team1-message2')
    # send message to player 4 on team 1
    db.messages.create_direct_message(
        6, 1, 'player4-team1-message3')
    # send message to player 5 on team 1
    db.messages.create_direct_message(
        7, 1, 'player5-team1-message1')
    # send message to player 5 on team 1
    db.messages.create_direct_message(
        7, 1, 'player5-team1-message2')
    # send message to player 5 on team 1
    db.messages.create_direct_message(
        7, 1, 'player5-team1-message3')
    # send message to player 6 on team 1
    db.messages.create_direct_message(
        8, 1, 'player6-team1-message1')
    # send message to player 6 on team 1
    db.messages.create_direct_message(
        8, 1, 'player6-team1-message2')
    # send message to player 6 on team 1
    db.messages.create_direct_message(
        8, 1, 'player6-team1-message3')

    # send message to player 9 on team 2
    db.messages.create_direct_message(
        11, 1, 'player3-team2-message1')
    # send message to player 9 on team 2
    db.messages.create_direct_message(
        11, 1, 'player3-team2-message2')
    # send message to player 9 on team 2
    db.messages.create_direct_message(
        11, 1, 'player3-team2-message3')
    # send message to player 10 on team 2
    db.messages.create_direct_message(
        12, 1, 'player4-team2-message1')
    # send message to player 10 on team 2
    db.messages.create_direct_message(
        12, 1, 'player4-team2-message2')
    # send message to player 10 on team 2
    db.messages.create_direct_message(
        12, 1, 'player4-team2-message3')
    # send message to player 1 on team 2
    db.messages.create_direct_message(
        3, 1, 'player5-team2-message1')
    # send message to player 1 on team 2
    db.messages.create_direct_message(
        3, 1, 'player5-team2-message2')
    # send message to player 1 on team 2
    db.messages.create_direct_message(
        3, 1, 'player5-team2-message3')
    # send message to player 8 on team 2
    db.messages.create_direct_message(
        10, 1, 'player8-team2-message1')
    # send message to player 8 on team 2
    db.messages.create_direct_message(
        10, 1, 'player8-team2-message2')
    # send message to player 8 on team 2
    db.messages.create_direct_message(
        10, 1, 'player8-team2-message3')

    return 'successfully created data'
