'''
FUNCTIONS:
all functions return a tuple of the format (message string, error boolean, data object)
    groups:
        create_group(connection, name, parent_team_id) - returns group_id
        add_user_to_group(connection, user_id, group_id) - returns nothing
        remove_user_from_group(connection, user_id, group_id) - returns nothing
        get_group(connection, group_id) - returns the group info and its users
        get_groups_phone_numbers(connection, group_id) - returns an array of phone numbers
    messages:
        create_direct_message(connection, recipient_user_id, sender_user_id, message_content) - returns message_id
        create_group_message(connection, recipient_group_id, sender_user_id, message_content) - returns gmessage_id
        get_users_direct_messages(connection, user_id) - returns an array of messages
        get_groups_messages(connection, group_id) - returns an array of messages
    schema:
        reset_tables(connection, database) - returns nothing
    teams:
        create_team(connection, name, owner_user_id) - returns team_id
        add_user_to_team(connection, user_id, team_id) - returns nothing
        remove_user_from_team(connection, user_id, team_id) - returns nothing
        change_users_permission_level_for_team(connection, user_id, team_id, permission_level) - returns nothing
        edit_teams_name(connection, team_id, new_team_name) - returns nothing
        get_team(connection, team_id) - returns the team info and its users
        get_teams_phone_numbers(connection, team_id) - returns an array of phone numbers
        get_teams_groups(connection, team_id) - returns an array of groups and their users
    users:
        create_user(connection, name, email, phone_number) - returns user_id
        get_user_id(connection, email) - returns user_id
        check_if_user_has_phone_number(connection, user_id, phone_number) - returns exists (0 or 1)
        add_phone_number_to_user(connection, phone_number, user_id) - returns nothing
        remove_phone_number_from_user(connection, phone_number, user_id) - returns nothing
        get_user(connection, user_id) - returns the user info, their teams, and their groups
'''


from . import groups
from . import messages
from . import schema
from . import teams
from . import users
import psycopg2
import psycopg2.pool
from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '../.env'))

connection_pool = psycopg2.pool.ThreadedConnectionPool(
    5,
    20,
    user=environ.get('DB_USERNAME'),
    password=environ.get('DB_PASSWORD'),
    host=environ.get('DB_URL'),
    port='5432',
    database=environ.get('DB_NAME')
)


def connect():
    connection = connection_pool.getconn()
    connection.autocommit = True
    return connection, connection_pool
