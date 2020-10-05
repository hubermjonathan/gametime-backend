'''
DOCUMENTATION:
all functions take in a connection object first
all functions return a tuple of the format (response message, response code, data)

    drop.py:
        drop_test_tables(connection):
            drops and creates all tables in the test database
            takes in no additional arguments
            returns nothing

        drop_prod_tables(connection):
            drops and creates all tables in the prod database
            takes in no additional arguments
            returns nothing

    groups.py:
        create_group(connection, name, team_id):
            creates a new group for a team
            takes in the name of the group and the team it will belong to
            returns the id of the new group

        add_to_group(connection, user_id, group_id):
            adds one or more members to a group
            takes in the user(s) being added and the group to add to
            returns nothing

        remove_from_group(connection, user_id, group_id):
            removes one or more members from a group
            takes in the user(s) being removed and the group to remove from
            returns nothing

    teams.py:
        create_team(connection, name, user_id):
            creates a new team
            takes in the name of the team and the owner of it
            returns nothing

        add_to_team(connection, user_id, team_id):
            adds a user to a team
            takes in the user to add and the team to add to
            returns nothing

        remove_from_team(connection, user_id, team_id):
            removes a user from a team
            takes in the user to remove and the team to remove from
            returns nothing

        change_permission_level(connection, user_id, team_id, privelege_level):
            changes the permission level for a user on a team
            takes in the user being modified, the team they are being modified for, and the new privelege level
            returns nothing

        edit_team_name(connection, team_id, name):
            edits the name of a team
            takes in the team being modified and the new name
            returns nothing

        get_teams_members(connection, team_id):
            retrieves the members of a team
            takes in the team to get members from
            returns an array of tuples of the format (user_id, name, email, phone_number, profile_picture)

    users.py:
        create_user(connection, name, email, phone_number):
            creates a user
            takes in the name, email, and phone number of the new user
            returns the id of the new user
        add_phone_number(connection, user_id, phone_number):
            adds a new phone number to a user
            takes in the user to add to and the new phone number to add
            returns nothing
        remove_phone_number(connection, user_id, phone_number):
            removes an extra phone number from a user
            takes in the user to remove from and the phone number to remove
            returns nothing

TODO:
    functions:
        general get functions
        all of the message storing and retrieving

    unit test:
        give admin privelege
        remove admin privelege
        join team
        leave team
        view teams
        create team
        edit team
        view and manage team
'''


from . import drop
from . import users
from . import teams
from . import groups
import psycopg2
from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


def connect():
    connection = psycopg2.connect(
        host=environ.get('DB_URL'),
        database=environ.get('DB_NAME'),
        user=environ.get('DB_USERNAME'),
        password=environ.get('DB_PASSWORD')
    )
    connection.autocommit = True

    return connection
