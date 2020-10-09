from flask import Blueprint
from .. import db

from flask_login import login_required

import json

examplebp = Blueprint('examplebp', __name__)

@examplebp.route('/test', methods=['POST'])
@login_required
def test():
    
    return 'Test', 200

@examplebp.route('/test1')
def test1():
    connection = db.connect()
    result = db.drop.drop_test_tables(connection)
    result = db.users.create_user(connection, 'coach1', 'coach1', 'coach1')
    result = db.users.create_user(connection, 'player1', 'player1', 'player1')
    result = db.users.create_user(connection, 'player2', 'player2', 'player2')
    result = db.teams.create_team(connection, 'team1', 1)
    result = db.teams.add_to_team(connection, 2, 1)
    result = db.teams.add_to_team(connection, 3, 1)
    result = db.groups.create_group(connection, 'group1', 1)
    result = db.groups.add_to_group(connection, 2, 2)
    result = db.groups.add_to_group(connection, 3, 2)
    connection.close()
    return result[0], result[1]


@examplebp.route('/test2')
def test2():
    connection = db.connect()
    result = db.groups.remove_from_group(connection, 2, 2)
    result = db.groups.remove_from_group(connection, 3, 2)
    connection.close()
    return result[0], result[1]


@examplebp.route('/cl')
def cl():
    connection = db.connect()
    result = db.drop.drop_test_tables(connection)
    connection.close()
    return result[0], result[1]
